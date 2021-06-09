from unittest import TestCase
from pkg_resources import resource_filename

from app.utils import file_utils
from app.dq.validator import CalendarValidator


class TestValidator(TestCase):

    DATA_PATH = resource_filename(__name__, 'resources/test_data.json')
    SCHEMA_PATH = resource_filename(__name__, 'resources/test_schema.json')

    def setUp(self):
        self.meetings = file_utils.get_json_data(self.DATA_PATH)
        self.validator = CalendarValidator(self.SCHEMA_PATH)

    def test_validate_meeting(self):
        for meeting in self.meetings:
            self.assertIsNone(self.validator.validate_record(meeting))

    def test_validate_meeting_fail(self):
        self.meetings.append({"meeting_name": "123", "start_time": "09:00", "unexpected_field": "doodoo"})

        with self.assertRaises(RuntimeError):
            for meeting in self.meetings:
                self.validator.validate_record(meeting)
