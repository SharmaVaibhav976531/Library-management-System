from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse as django_reverse
from jinja2 import Environment


def url_reverse(*args, **kwargs):
    """Wrapper around Django's reverse function for use in Jinja2 templates."""
    try:
        result = django_reverse(*args, **kwargs)
        return result
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": url_reverse,
        }
    )
    return env
