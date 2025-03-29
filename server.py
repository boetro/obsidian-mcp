from mcp.server.fastmcp import FastMCP

import os
import requests
from markdownify import markdownify as md

from obsidian.schemas import Vault

mcp = FastMCP("obsidian")


vaults = {
    "personal": Vault(
        name="personal",
        directory="/Users/calebvandyke/Google Drive/My Drive/journal/personal",
        description="This vaults contains personal journal entries. It includes things like my daily journal entries, my notes on books I've read, and recipes.",
    )
}


for vault in vaults.values():

    @mcp.resource(f"vault://{vault.name}")
    def get_value():
        return vault


@mcp.tool(description="Returns a list of files in a given vault path")
def list_vault_files(vault_name: str, path: str, recursive: bool = False):
    vault = vaults[vault_name]
    return vault.get_valut_files(path, recursive)


@mcp.tool(description="Get the contents of a file contained in a vault")
def get_vault_file(vault_name: str, file_relative_path: str):
    vault = vaults[vault_name]
    with open(os.path.join(vault.directory, file_relative_path), "r") as f:
        return f.read()


@mcp.tool(description="Write the contents of a file in a vault")
def write_vault_file(vault_name: str, file_relative_path: str, content: str):
    vault = vaults[vault_name]
    with open(os.path.join(vault.directory, file_relative_path), "w") as f:
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
def add_recipe(recipe_url: str, vault_name: str):
    response = requests.get(recipe_url, headers=headers)
    html_content = response.text

    return f"""\
Below is the content of a website containing a recipe that I want you to copy to my vault: `{vault_name}. Please follow the same format that is used as other recipes in that directory.

It is very important that you make no mistakes when saving the recipe. Ensure that all ingredients, quantity, and instructions match exactly what is contained on the website.

Please confirm with me what you will save before commiting it.

Recipe Website Content:

{md(html_content)}

"""
