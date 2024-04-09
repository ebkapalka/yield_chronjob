import requests


def check_file_exists(server_url: str, path: str, username: str,
                      password: str, destination_name: str, **args) -> bool:
    """
    Save a file to a WebDAV server
    :param server_url: url of the server
    :param path: path to the destination folder
    :param username: username
    :param password: password
    :param destination_name: destination file name
    :return: None
    """
    file_url = f"{server_url.rstrip('/')}/{path.rstrip('/')}/{destination_name}"
    head_response = requests.head(file_url, auth=(username, password))
    if head_response.status_code == 200:
        # case when file already exists
        return True
    return False


def save_file_to_webdav(server_url: str, path: str, username: str, password: str,
                        destination_name: str, destination_content: bytes) -> None:
    """
    Save a file to a WebDAV server
    :param server_url: url of the server
    :param path: path to the destination folder
    :param username: username
    :param password: password
    :param destination_name: destination file name
    :param destination_content: destination file content
    :return: None
    """
    file_url = f"{server_url.rstrip('/')}/{path.rstrip('/')}/{destination_name}"
    response = requests.put(file_url, data=destination_content, auth=(username, password))
    if response.status_code in [200, 201]:
        print("File saved successfully.")
    else:
        print(f"Failed to save the file. Status code: {response.status_code}")
