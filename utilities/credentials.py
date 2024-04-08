import keyring


def request_credentials(service_name: str, user=None) -> tuple[str, str]:
    """
    Request credentials from the user and store them in the keyring
    :param service_name: name of the service for which the credentials are requested
    :param user: username to request if need-be
    :return: tuple of username and password
    """
    word = "password" if user else "credentials"
    print(f"Please enter your {word} for {service_name}")
    while True:
        if not user:
            user = input("New Username: ").strip()
        pwd = input("New Password: ").strip()
        if user and pwd:
            return user, pwd
        else:
            print(f"Please enter non-empty {word}")


def store_credentials(service_name: str, user: str, pwd: str) -> None:
    """
    Store the credentials in the keyring
    :param service_name: name of the service for which the credentials are stored
    :param user: username to store
    :param pwd: password to store
    :return: None
    """
    keyring.set_password(service_name.strip(), user.strip(), pwd.strip())
    print(f"Stored credentials for {service_name.strip()} in the keyring")


def retrieve_credentials(service_name: str, user=None) -> tuple[str, str]:
    """
    Retrieve the credentials from the keyring. If the credentials are not found, request them from the user
    :param service_name: name of the service for which the credentials are retrieved
    :param user: username to retrieve
    :return:
    """
    pwd = keyring.get_password(service_name, user)
    if not pwd or not user:
        user, pwd = request_credentials(service_name, user)
        store_credentials(service_name, user, pwd)
    return user.strip(), pwd.strip()


def delete_credentials(service_name: str, user: str) -> None:
    """
    Delete the credentials from the keyring
    :param service_name: name of the service for which the credentials are deleted
    :param user: username to delete
    :return: None
    """
    keyring.delete_password(service_name.strip(), user.strip())
    print(f"Deleted credentials for {service_name} from the keyring")
