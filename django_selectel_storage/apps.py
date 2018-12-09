from django import apps
from django.conf import settings
from django.core.checks import Tags, Warning, register

HINT = (
    "Since 1.0, to improve the experience of multiple containers in the "
    "same project using, the settings format has been changed. For now, "
    "you should not use SELECTEL_USERNAME, SELECTEL_PASSWORD, "
    "SELECTEL_CONTAINER_NAME etc. settings. Consider using "
    "a SELECTEL_STORAGE  dictionary instead, like DATABASES or CACHES ones. "
)


class DjangoSelectelStorageAppConfig(apps.AppConfig):
    name = 'django_selectel_storage'


@register(Tags.compatibility)
def settings_compat_check(app_configs, **kwargs):

    if any((
        hasattr(settings, 'SELECTEL_USERNAME'),
        hasattr(settings, 'SELECTEL_PASSWORD'),
        hasattr(settings, 'SELECTEL_CONTAINER_NAME'),
    )):
        return [
            Warning(
                msg='Obsolete config format',
                hint=HINT,
                id='django_selectel_storage.W001',
            )
        ]
    return []
