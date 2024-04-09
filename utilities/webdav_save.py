import requests


def save_file_to_webdav(server_url: str, path: str, username: str, password: str,
                        file_name: str, file_content: bytes) -> None:
    """
    Save a file to a WebDAV server
    :param server_url: url of the server
    :param path: path to the destination folder
    :param username: username
    :param password: password
    :param file_name: destination file name
    :param file_content: destination file content
    :return: None
    """
    file_url = f"{server_url.rstrip('/')}/{path.rstrip('/')}/{file_name}"
    response = requests.put(file_url, data=file_content, auth=(username, password))
    if response.status_code in [200, 201]:
        print("File saved successfully.")
    else:
        print(f"Failed to save the file. Status code: {response.status_code}")
