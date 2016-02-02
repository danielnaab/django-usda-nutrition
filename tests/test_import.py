from django.core.management import call_command
from django.test import TestCase


class TestImportCommand(TestCase):
    def test_load_commands(self):
        """
        A very dumb test that just confirms that the import succeeds without
        unhandled exceptions raised.
        TODO: Don't be so stupid.
        """
        call_command('import_db')
