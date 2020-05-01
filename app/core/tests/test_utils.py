from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTest(TestCase):

    @patch('time.sleep', return_value=True)
    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db(self, getitem, ts):
        getitem.side_effect = [OperationalError] * 5 + [True]
        call_command('wait_for_db')
        self.assertEqual(getitem.call_count, 6)

    @patch('django.db.utils.ConnectionHandler.__getitem__')
    def test_wait_for_db_ready(self, getitem):
        """Test waiting for db when db is available"""

        getitem.return_value = True
        call_command('wait_for_db')
        self.assertEqual(getitem.call_count, 1)
