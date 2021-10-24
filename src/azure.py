# -*- coding: utf-8 -*-
"""
    src.azure
    ~~~~~~~~~

"""


def setup_azure_ad(oauth):
    oauth.register(
        name="azure",
        access_token_url="https://login.microsoftonline.com/0e88cb87-5a0a-47af-b8a9-2c4223451541/oauth2/v2.0/token",
        authorize_url="https://login.microsoftonline.com/0e88cb87-5a0a-47af-b8a9-2c4223451541/oauth2/v2.0/authorize",
        api_base_url="https://graph.microsoft.com/v1.0/",
        server_metadata_url="https://login.microsoftonline.com/0e88cb87-5a0a-47af-b8a9-2c4223451541/v2.0/.well-known/openid-configuration",
        client_kwargs={
            "scope": "openid email profile"
        }
    )
