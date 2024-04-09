from utilities.sftp_retrieve import (create_sftp_client, get_newest_yield,
                                     download_file_object, download_file_object_pieces)
from utilities.credentials import retrieve_credentials

import yaml

from utilities.webdav_save import save_file_to_webdav


def download_file(config: dict) -> tuple[str, bytes]:
    """
    Download the newest file from the source
    :param config: configuration dictionary
    :return: tuple of file name and file content
    """
    sftp_config = {
        "hostname": config["source"]["hostname"],
        "port": config["source"]["port"],
        "username": config["source"]["username"],
        "password": retrieve_credentials(
            config["source"]["service"],
            config["source"]["username"])[1]
    }
    sftp = create_sftp_client(**sftp_config)
    newest_file_name = get_newest_yield(
        sftp, config["source"]["sftp_directory"])
    newest_file_content = download_file_object_pieces(
        sftp, config["source"]["sftp_directory"], newest_file_name)
    sftp.close()
    return newest_file_name, newest_file_content


def save_file(config: dict, file_name: str, file_content: bytes) -> None:
    """
    Save a file to the destination
    :param config: configuration dictionary
    :param file_name: name of the file to save
    :param file_content:
    :return:
    """
    webdav_config = {
        "server_url": config["destination"]["server_url"],
        "path": config["destination"]["folder_path"],
        "username": config["destination"]["username"],
        "password": retrieve_credentials(
            config["destination"]["service"],
            config["destination"]["username"])[1],
        "destination_name": file_name,
        "destination_content": file_content
    }
    save_file_to_webdav(**webdav_config)


if __name__ == '__main__':
    with open("config.yml", "r") as file:
        cfg = yaml.safe_load(file)
    n, c = download_file(cfg)
    save_file(cfg, n, c)
