#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from dotenv import load_dotenv  # Pour les variables d'.env


# Prendre les variables d'environnement
load_dotenv()

if not os.getenv("DEPLOY_DEV_OR_PRODUCTION") in ("dev", "production"):
    raise ValueError("DEPLOY_DEV_OR_PRODUCTION %s doit etre dev ou production" % os.getenv("DEPLOY_DEV_OR_PRODUCTION"))


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lesgrandsvoisins.settings.dev")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
