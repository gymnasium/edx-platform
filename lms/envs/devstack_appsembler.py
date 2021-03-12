# devstack_appsembler.py

import os
from .devstack_docker import *
from .appsembler import *

ENV_APPSEMBLER_FEATURES = ENV_TOKENS.get('APPSEMBLER_FEATURES', {})
for feature, value in ENV_APPSEMBLER_FEATURES.items():
    APPSEMBLER_FEATURES[feature] = value

# disable caching in dev environment
for cache_key in CACHES.keys():
    CACHES[cache_key]['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

INSTALLED_APPS += (
    'appsembler',
    'appsembler_api'
)

DEFAULT_TEMPLATE_ENGINE['OPTIONS']['context_processors'] += ('appsembler.context_processors.intercom',)

CUSTOM_LOGOUT_REDIRECT_URL = ENV_TOKENS.get('CUSTOM_LOGOUT_REDIRECT_URL', '/')

TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_KEEP_DOMAIN_PART', False)
TPA_CLEAN_USERNAMES_REPLACER_CHAR = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_REPLACER_CHAR', "")
TPA_CLEAN_USERNAMES_ADD_RANDOM_INT = ENV_TOKENS.get('TPA_CLEAN_USERNAMES_ADD_RANDOM_INT', False)

if APPSEMBLER_FEATURES.get('ENABLE_EXTERNAL_COURSES', False):
    INSTALLED_APPS += (
        'openedx.core.djangoapps.appsembler.external_courses',
    )

EDX_ORG_COURSE_API_URL = ENV_TOKENS.get('EDX_ORG_COURSE_API_URL', False)
EDX_ORG_COURSE_API_TOKEN_URL = AUTH_TOKENS.get('EDX_ORG_COURSE_API_TOKEN_URL', False)
EDX_ORG_COURSE_API_CLIENT_ID = AUTH_TOKENS.get('EDX_ORG_COURSE_API_CLIENT_ID', False)
EDX_ORG_COURSE_API_CLIENT_SECRET = AUTH_TOKENS.get('EDX_ORG_COURSE_API_CLIENT_SECRET', False)
EDX_ORG_COURSE_API_TOKEN_TYPE = AUTH_TOKENS.get('EDX_ORG_COURSE_API_TOKEN_TYPE', False)
EDX_ORG_COURSE_API_CATALOG_IDS = ENV_TOKENS.get('EDX_ORG_COURSE_API_CATALOG_IDS', False)

if APPSEMBLER_FEATURES.get('ENABLE_EXTERNAL_COURSES', False):
    if ENV_TOKENS.get('EXTERNAL_COURSES_FETCH_PERIOD_HOURS', 24) is not None:
        CELERYBEAT_SCHEDULE['fetch-external-courses'] = {
            'task': 'openedx.core.djangoapps.appsembler.external_courses.tasks.fetch_courses',
            'schedule': datetime.timedelta(
                hours=ENV_TOKENS.get('EXTERNAL_COURSES_FETCH_PERIOD_HOURS', 24)
            ),
        }

# to allow to run python-saml with custom port
SP_SAML_RESTRICT_MODE = False

#configure auth backends
if 'LMS_AUTHENTICATION_BACKENDS' in APPSEMBLER_FEATURES.keys():
    #default behavior is to replace the existing backends with those in APPSEMBLER_FEATURES
    AUTHENTICATION_BACKENDS = tuple(APPSEMBLER_FEATURES['LMS_AUTHENTICATION_BACKENDS'])

EXCLUSIVE_SSO_LOGISTRATION_URL_MAP = ENV_TOKENS.get('EXCLUSIVE_SSO_LOGISTRATION_URL_MAP', {})

#attempt to import model from our custom fork of edx-organizations
# if it works, then also add the middleware
try:
    from organizations.models import UserOrganizationMapping
    MIDDLEWARE_CLASSES += (
        'organizations.middleware.OrganizationMiddleware',
    )
except ImportError:
    pass

# override devstack.py automatic enabling of courseware discovery
FEATURES['ENABLE_COURSE_DISCOVERY'] = ENV_TOKENS['FEATURES'].get('ENABLE_COURSE_DISCOVERY', FEATURES['ENABLE_COURSE_DISCOVERY'])

# Enable Figures if it is included
if 'figures' in INSTALLED_APPS:
    import figures
    figures.update_settings(
        WEBPACK_LOADER,
        CELERYBEAT_SCHEDULE,
        ENV_TOKENS.get('FIGURES', {}))

# use configured course mode defaults as for aws, not standard devstack's
COURSE_MODE_DEFAULTS.update(ENV_TOKENS.get('COURSE_MODE_DEFAULTS', COURSE_MODE_DEFAULTS))
