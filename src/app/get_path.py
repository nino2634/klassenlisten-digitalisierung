import os

#puts together the absolute path of the a file file 
def create_path(path, file_name) -> str:
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(current_file))
    file = os.path.join(project_root, path, file_name)

    return file