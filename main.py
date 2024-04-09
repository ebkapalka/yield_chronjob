from utilities.sftp_retrieve import (create_sftp_client, get_newest_file_name,
                                     download_file_object)
from utilities.webdav_save import save_file_to_webdav, check_file_exists
from utilities.credentials import retrieve_credentials

import yaml


class Config:
    """
    Class to parse the configuration file
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = self._parse_config()
        self.sftp_dir = self.config["source"]["sftp_directory"]

    def _parse_config(self):
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)

    def get_sftp_config(self) -> dict:
        """
        Get the SFTP configuration
        :return: dictionary with SFTP configuration
        """
        creds = retrieve_credentials(
            self.config["source"]["service"],
            self.config["source"]["username"]
        )
        return {
            "hostname": self.config["source"]["hostname"],
            "port": self.config["source"]["port"],
            "username": self.config["source"]["username"],
            "password": creds[1]
        }

    def get_webdav_config(self):
        """
        Get the WebDAV configuration
        :return: dictionary with WebDAV configuration
        """
        creds = retrieve_credentials(
            self.config["destination"]["service"],
            self.config["destination"]["username"]
        )
        return {
            "server_url": self.config["destination"]["server_url"],
            "path": self.config["destination"]["folder_path"],
            "username": self.config["destination"]["username"],
            "password": creds[1]
        }


def transfer_newest_file(sftp_config, webdav_config, sftp_directory):
    """
    Transfer the newest file from an SFTP server to a WebDAV server
    :param sftp_config:
    :param webdav_config:
    :param sftp_directory:
    :return:
    """
    sftp_client = create_sftp_client(**sftp_config)
    file_name = get_newest_file_name(sftp_client, sftp_directory)
    print(f"Newest Yield file: {file_name}")
    webdav_config_full = {**webdav_config, "destination_name": file_name}
    if not check_file_exists(**webdav_config_full):
        file_content = download_file_object(sftp_client, sftp_directory, file_name)
        save_file_to_webdav(**webdav_config_full, destination_content=file_content)
    else:
        print(f"File {file_name} already exists")
    sftp_client.close()


if __name__ == '__main__':
    cfg_path = "config.yml"
    cfg = Config(cfg_path)
    sftp_cfg = cfg.get_sftp_config()
    webdav_cfg = cfg.get_webdav_config()
    sftp_dir = cfg.sftp_dir
    transfer_newest_file(sftp_config=sftp_cfg,
                         webdav_config=webdav_cfg,
                         sftp_directory=sftp_dir)
