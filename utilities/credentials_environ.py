import os


def request_credentials(service_name: str, user=None) -> tuple[str, str]:
    """
    Request credentials from the user and store them in environment variables.
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
    Store the credentials in environment variables.
    :param service_name: name of the service for which the credentials are stored
    :param user: username to store
    :param pwd: password to store
    :return: None
    """
    os.system(f'setx {service_name.upper()}_USER "{user.strip()}"')
    os.system(f'setx {service_name.upper()}_PWD "{pwd.strip()}"')
    print(f"Stored credentials for {service_name.strip()} in environment variables")


def retrieve_credentials(service_name: str, user=None) -> tuple[str, str]:
    """
    Retrieve the credentials from environment variables. If the credentials are not found, request them from the user.
    :param service_name: name of the service for which the credentials are retrieved
    :param user: username to retrieve
    :return: tuple of username and password
    """
    user_env_var = f"{service_name.upper()}_USER"
    pwd_env_var = f"{service_name.upper()}_PWD"

    user = user or os.getenv(user_env_var)
    pwd = os.getenv(pwd_env_var)
    if not pwd or not user:
        user, pwd = request_credentials(service_name, user)
        store_credentials(service_name, user, pwd)

    return user.strip(), pwd.strip()


def delete_credentials(service_name: str) -> None:
    """
    Delete the credentials from environment variables.
    :param service_name: name of the service for which the credentials are deleted
    :return: None
    """
    user_env_var = f"{service_name.upper()}_USER"
    pwd_env_var = f"{service_name.upper()}_PWD"

    os.system(rf'reg delete HKCU\Environment /F /V {user_env_var}')
    os.system(rf'reg delete HKCU\Environment /F /V {pwd_env_var}')

    print(f"Deleted credentials for {service_name} from environment variables")
