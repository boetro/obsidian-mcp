from pydantic import BaseModel

import os


class Workspace(BaseModel):
    name: str
    directory: str
    description: str

    def get_workspace_files(self, path: str, recursive: bool):
        files: list[File] = []
        if path.startswith("/"):
            path = path[1:]
        full_path = os.path.join(self.directory, path)

        if os.path.isdir(full_path):
            for item in os.listdir(full_path):
                item_path = os.path.join(path, item)
                abs_item_path = os.path.join(self.directory, item_path)

                if os.path.isfile(abs_item_path):
                    # Skip non-markdown files
                    if not item.lower().endswith(".md"):
                        continue
                    files.append(File(relative_path=item_path, is_dir=False))
                elif os.path.isdir(abs_item_path):
                    if recursive:
                        sub_files = self.get_workspace_files(item_path, recursive)
                        files.extend(sub_files)
                    else:
                        files.append(File(relative_path=item_path, is_dir=True))

        return files


class File(BaseModel):
    relative_path: str
    is_dir: bool
