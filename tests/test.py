import os

from azdbr.identity import (
    AzCredential,
    IdentityBuilder,
    MissingInfoError,
    AuthenticationError,
    AuthType,
    UnsupportedAuthError,
)


from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
tenant_id = os.getenv("TENANT_ID")
client_secret = os.getenv("CLIENT_SECRET")

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def build_spn_creds():
    builder = IdentityBuilder()
    try:
        spn_credential: AzCredential = (
            builder.with_client_id(client_id=client_id)
            .with_tenant_id(tenant_id=tenant_id)
            .with_client_secret(secret=client_secret)
            .build()
        )
        spn_credential.info(f"credential: {type(spn_credential.credential)}")

        token = spn_credential.get_token("[Mail.Send]")
        print(f"token: {token}")
    except AuthenticationError as ae:
        print(f"AE: {ae}, {type(ae)}")
    except ValueError as ve:
        print(f"ve: {ve}")
    # except Exception as e:
    #     print(f"e: {e}")


def build_user_creds():
    builder = IdentityBuilder()
    try:
        user_credential: AzCredential = (
            builder.with_client_id(client_id=client_id)
            .with_tenant_id(tenant_id=tenant_id)
            .with_user_name(username=username)
            .with_password(password=password)
            .with_auth_type(authType=AuthType.AZ_USER_CREDS)
            .build()
        )
        print(f"credential: {type(user_credential)}")
        print(f"auth type: {user_credential.type}")

        token = user_credential.get_token("[Mail.Send]")
        print(f"token: {token}")
    except MissingInfoError as mie:
        builder.error(f"mie: {mie}")
    except AuthenticationError as ae:
        print(f"ae: {ae}")
    except Exception as e:
        print(f"exception: {e}")


def print_dashes(len: int = 75):
    print("-" * len)


def main():
    print("Hello from azdbr!")

    print("testing SPN credentials...")
    build_spn_creds()

    print_dashes()

    print("testing Username Password credentials...")
    build_user_creds()


if __name__ == "__main__":
    main()
