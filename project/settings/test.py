from .base import *  # noqa

DEBUG = False

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": env.str("SOCIALAPP_CLIENT_ID"),  # noqa
            "secret": env.str("SOCIALAPP_SECRET"),  # noqa
            "key": "",
        },
    }
}
