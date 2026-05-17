# lms_core/jinja.py
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse as django_reverse
from jinja2 import Environment


def url_reverse(*args, **kwargs):
    """Wrapper around Django's reverse function for use in Jinja2 templates."""
    try:
        return django_reverse(*args, **kwargs)
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise


def environment(**options):
    # ✅ Remove Django-specific options that jinja2.Environment doesn't accept
    options.pop("match_extension", None)
    options.pop("context_processors", None)

    # Initialize Jinja2 environment with cleaned options
    env = Environment(**options)

    # ✅ Inject Django helpers into Jinja2 global namespace
    env.globals.update(
        {
            "static": staticfiles_storage.url,
            "url": url_reverse,
        }
    )
    return env
