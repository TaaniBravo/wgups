import os


def get_project_root():
    """
    Return the absolute path of the project's root directory.
    Time complexity: O(n)
    Space complexity: O(1)
    """
    current_path = os.path.abspath(__file__)  # Get the absolute path of the current file
    root_path = os.path.dirname(current_path)  # Get the directory containing the current file

    # Traverse up the directory tree until we find a specific file or reach the root
    while not os.path.isfile(os.path.join(root_path, 'README.md')) and root_path != '/':
        root_path = os.path.dirname(root_path)

    return root_path
