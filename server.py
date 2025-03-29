from mcp.server.fastmcp import FastMCP

import os
import requests
from markdownify import markdownify as md

from obsidian.schemas import Workspace

mcp = FastMCP("obsidian")


workspaces = {
    "personal": Workspace(
        name="personal",
        directory="/Users/calebvandyke/Google Drive/My Drive/journal/personal",
        description="This workspace contains personal journal entries. It includes things like my daily journal entries, my notes on books I've read, and recipes.",
    )
}


for workspace in workspaces.values():

    @mcp.resource(f"workspace://{workspace.name}")
    def get_workspace():
        return workspace


@mcp.tool(description="Returns a list of files in a given workspace path")
def list_workspace_files(workspace_name: str, path: str, recursive: bool = False):
    workspace = workspaces[workspace_name]
    return workspace.get_workspace_files(path, recursive)


@mcp.tool(description="Get the contents of a file contained in a workspace")
def get_workspace_file(workspace_name: str, file_relative_path: str):
    workspace = workspaces[workspace_name]
    with open(os.path.join(workspace.directory, file_relative_path), "r") as f:
        return f.read()


@mcp.tool(description="Write the contents of a file in a workspace")
def write_workspace_file(workspace_name: str, file_relative_path: str, content: str):
    workspace = workspaces[workspace_name]
    with open(os.path.join(workspace.directory, file_relative_path), "w") as f:
        _ = f.write(content)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
}


@mcp.prompt()
def add_recipe(recipe_url: str, workspace_name: str):
    response = requests.get(recipe_url, headers=headers)
    html_content = response.text

    return f"""\
Below is the content of a website containing a recipe that I want you to copy to my workspace: `{workspace_name}. Please follow the same format that is used as other recipes in that directory.

It is very important that you make no mistakes when saving the recipe. Ensure that all ingredients, quantity, and instructions match exactly what is contained on the website.

Please confirm with me what you will save before commiting it.

Recipe Website Content:

{md(html_content)}

"""
