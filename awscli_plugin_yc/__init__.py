import datetime
import json
import os

import botocore
import yandexcloud
from botocore.credentials import CredentialProvider
from botocore.credentials import RefreshableCredentials
from botocore.exceptions import BotoCoreError
from yandex.cloud.iam.v1.iam_token_service_pb2_grpc import IamTokenServiceStub

ENDPOINT_URL = 'endpoint_url'
YC_IAM_TOKEN_ENV = 'YC_IAM_TOKEN'


class UnsupportedCredentialsError(BotoCoreError):
    """
    No credentials could be found.
    """
    fmt = 'Unsupported credentials'


def add_token(self, request):
    if self.credentials.token and not self.credentials.token.startswith('t1.'):
        raise UnsupportedCredentialsError()
    request.headers['X-YaCloud-SubjectToken'] = self.credentials.token


# monkey patch
botocore.auth.SigV4Auth.add_auth = add_token


class EnvTokenCredentialProvider(botocore.credentials.CredentialProvider):
    METHOD = 'yc-env'
    CANONICAL_NAME = 'YcIamTokenFromEnv'

    def load(self):
        token = os.getenv(YC_IAM_TOKEN_ENV)
        if not token:
            return
        return botocore.credentials.Credentials(
            "", "",
            token, method=self.METHOD
        )


class YcSaCredentialProvider(CredentialProvider):
    METHOD = 'yc-sa'
    CANONICAL_NAME = 'YcIamToken'

    def __init__(self):
        super().__init__()
        service_account_key = os.getenv("SA_KEY")
        if service_account_key:
            service_account_key = json.loads(service_account_key)
        elif service_account_key_file := os.getenv("SA_KEY_FILE"):
            with open(service_account_key_file) as f:
                service_account_key = json.loads(f.read())
        else:
            service_account_key = None

        self._service_account_key = service_account_key

    def load(self):
        service_account_key = self._service_account_key
        if service_account_key is None:
            return

        creds_dict = self._retrieve_credentials_using(service_account_key)
        return RefreshableCredentials.create_from_metadata(
            creds_dict,
            lambda: self._retrieve_credentials_using(service_account_key),
            self.METHOD
        )

    def _retrieve_credentials_using(self, service_account_key):
        yc = yandexcloud.SDK(service_account_key=service_account_key)
        token = yc.client(IamTokenServiceStub).Create(yc._channels._token_requester.get_token_request())
        return {
            'access_key': '',
            'secret_key': '',
            'token': token.iam_token,
            'expiry_time': datetime.datetime.fromtimestamp(token.expires_at.seconds,
                                                           tz=datetime.timezone.utc).isoformat(),
        }


def get_endpoint_from_profile(profile, command):
    endpoint = None
    if command in profile:
        if ENDPOINT_URL in profile[command]:
            endpoint = profile[command][ENDPOINT_URL]
    return endpoint


def set_endpoint_from_profile(parsed_args, **kwargs):
    endpoint_url = parsed_args.endpoint_url
    command = parsed_args.command
    # If endpoint set on CLI option, use CLI endpoint
    if endpoint_url is None:
        session = kwargs['session']
        # Set profile to session so we can load profile from config
        if parsed_args.profile:
            session.set_config_variable('profile', parsed_args.profile)
        service_endpoint = get_endpoint_from_profile(session.get_scoped_config(), command)
        if service_endpoint is not None:
            parsed_args.endpoint_url = service_endpoint
        else:
            parsed_args.endpoint_url = 'https://storage.yandexcloud.net'


def add_credentials_provider(parsed_args, **kwargs):
    # If endpoint set on CLI option, use CLI endpoint
    session = kwargs['session']
    credential_provider = session.get_component('credential_provider')
    credential_provider.insert_before('env', EnvTokenCredentialProvider())
    credential_provider.insert_before('env', YcSaCredentialProvider())


def awscli_initialize(cli):
    cli.register('top-level-args-parsed', set_endpoint_from_profile)
    cli.register('top-level-args-parsed', add_credentials_provider)
