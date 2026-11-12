#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')
    try:
        if (
            len(sys.argv) > 1
            and sys.argv[1] == 'runserver'
            and os.environ.get('RUN_MAIN') != 'true'
            and '--help' not in sys.argv
            and '-h' not in sys.argv
        ):
            import django
            from django.core.management import call_command

            django.setup()
            call_command('migrate', interactive=False)

            from poblar import poblar_productos

            poblar_productos()

        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
