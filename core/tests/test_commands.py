from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for db when db is available"""
        patched_check.return_value = True
        call_command('wait_for_db')
        
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep', return_value=True)
    # patched arguments get added from the inside out i.e patched_sleep, patched_check and so on
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for db when db is not available"""

        # The first two calls to check() will raise Psycopg2Error
        # The next three calls will raise OperationalError
        # The last call will return True
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        
        call_command('wait_for_db')
        
        self.assertEqual(patched_check.call_count, 6)

        patched_check.assert_called_with(databases=['default'])

