"""
URLs for static_template_view app
"""


from django.conf import settings
from django.urls import path, re_path

from lms.djangoapps.static_template_view import views

urlpatterns = []

# Only enable URLs for those marketing links actually enabled in the
# settings. Disable URLs by marking them as None.
for key, value in settings.MKTG_URL_LINK_MAP.items():
    # Skip disabled URLs
    if value is None:
        continue

    # These urls are enabled separately
    if key == "ROOT" or key == "COURSES":  # lint-amnesty, pylint: disable=consider-using-in
        continue

    # The MKTG_URL_LINK_MAP key specifies the template filename
    template = key.lower()
    if '.' not in template:
        # Append STATIC_TEMPLATE_VIEW_DEFAULT_FILE_EXTENSION if
        # no file extension was specified in the key
        template = f"{template}.{settings.STATIC_TEMPLATE_VIEW_DEFAULT_FILE_EXTENSION}"

    # Make the assumption that the URL we want is the lowercased
    # version of the map key
    urlpatterns.append(re_path(r'^%s$' % key.lower(), views.render, {'template': template}, name=value))
