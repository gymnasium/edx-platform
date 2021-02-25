"""
Utils to be used by third_party_auth app.

This helps to reduce merge conflicts.
"""
import re
from random import randrange

from django.conf import settings


def clean_username(suggested_username):
    """
    Cleans the username if APPSEMBLER_FEATURES.ENABLE_THIRD_PARTY_AUTH_CLEAN_USERNAMES is set.

    if the FEATURE flag ENABLE_THIRD_PARTY_AUTH_CLEAN_USERNAMES is set to
    True we clean all special chars from the username, this feature is
    configurable by this three env settings with this default:
    TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART: false
    TPA_CLEAN_USERNAMES_REPLACER_CHAR: ""
    TPA_CLEAN_USERNAMES_ADD_RANDOM_INT: false
    You can override this three in your settings.
    """
    if settings.APPSEMBLER_FEATURES.get("ENABLE_THIRD_PARTY_AUTH_CLEAN_USERNAMES"):
        if not settings.TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART:
            if len(
                    re.findall(r'[^@]+@[^@]+\.[^@]+', suggested_username)
            ) > 0:
                suggested_username = suggested_username.split('@')[0]

        suggested_username = re.sub(
            r'[^a-zA-Z0-9]',
            settings.TPA_CLEAN_USERNAMES_REPLACER_CHAR,
            suggested_username
        )

        if settings.TPA_CLEAN_USERNAMES_ADD_RANDOM_INT:
            suggested_username = suggested_username[:27] if len(suggested_username) > 27 else suggested_username
            suggested_username += str(randrange(100, 999))
        else:
            suggested_username = suggested_username[:30] if len(suggested_username) > 30 else suggested_username

    return suggested_username


def get_fullname(details, default_fullname):
    """
    Merges first and last name with a space if APPSEMBLER_FEATURES.ENABLE_THIRD_PARTY_AUTH_MERGE_FIRST_LAST_NAME
    is true.
    """
    suggester_personal_name = default_fullname

    if settings.APPSEMBLER_FEATURES.get('ENABLE_THIRD_PARTY_AUTH_MERGE_FIRST_LAST_NAME', False):
        suggester_personal_name = "%s %s" % (details.get('first_name', ''), details.get('last_name', ''))

    return suggester_personal_name
