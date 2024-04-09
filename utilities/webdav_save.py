from urllib.parse import quote
import requests


def check_file_exists(server_url: str, path: str, username: str,
                      password: str, destination_name: str, **args) -> bool:
    """
    Check if a file or its archived version exists on a WebDAV server.
    :param server_url: URL of the server.
    :param path: Path to the destination folder.
    :param username: Username for authentication.
    :param password: Password for authentication.
    :param destination_name: Name of the destination file.
    :return: True if the file or its archived version exists, False otherwise.
    """
    server_url = server_url.rstrip('/')
    path = quote(path.strip('/'), safe='/')
    destination_name = quote(destination_name, safe='/')
    file_urls = [
        f"{server_url}/{path}/{destination_name}",
        f"{server_url}/{path}/archive/{destination_name}"
    ]

    with requests.Session() as session:
        session.auth = (username, password)
        for url in file_urls:
            try:
                if session.head(url).status_code == 200:
                    return True
            except requests.RequestException as e:
                print(f"Error checking URL {url}: {e}")
                continue
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
