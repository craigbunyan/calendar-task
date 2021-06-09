from unittest import TestCase
from pkg_resources import resource_filename

from app.utils import file_utils


class TestFileUtils(TestCase):
    FILE_PATH = resource_filename(__name__, 'resources/test_data.json')

    def test_get_cal_data(self):
        actual_data = file_utils.get_json_data(self.FILE_PATH)
        self.assertEqual(len(actual_data), 3)
