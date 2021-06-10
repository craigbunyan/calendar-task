from unittest import TestCase
from pkg_resources import resource_filename
from datetime import datetime

from app.utils import file_utils
from app.meeting.meeting import Meeting


class TestMeeting(TestCase):

    FILE_PATH = resource_filename(__name__, 'resources/test_data.json')

    def setUp(self):
        test_data = file_utils.get_json_data(self.FILE_PATH)
        self.meetings = [Meeting(meeting) for meeting in test_data]

    def test_order_meeting_list(self):
        ordered_meetings = Meeting.order_meeting_list(self.meetings)
        ordered_names = [meeting.name for meeting in ordered_meetings]

        expected_output = ['test1', 'test2', 'test3']

        self.assertListEqual(expected_output, ordered_names)

    def test_order_meeting_list_empty(self):
        meetings = []
        ordered_meetings = Meeting.order_meeting_list(meetings)

        self.assertListEqual([], ordered_meetings)

    def test_group_meetings_by_date(self):
        ordered_meetings = Meeting.order_meeting_list(self.meetings)
        grouped_meetings = Meeting.group_meetings_by_date(ordered_meetings)
        grouped_dates = [date for date, meetings in grouped_meetings]

        expected_dates = [datetime(2021, 1, 1), datetime(2021, 1, 2)]

        self.assertListEqual(expected_dates, grouped_dates)

    def test_group_meetings_by_date_empty(self):
        meetings = []
        grouped_meetings = Meeting.group_meetings_by_date(meetings)

        self.assertListEqual([], list(grouped_meetings))

    def test_get_clashes(self):
        ordered_meetings = Meeting.order_meeting_list(self.meetings)
        clashes = Meeting.get_clashes(ordered_meetings)

        expected_clashes = [('test1', 'test2')]

        self.assertListEqual(expected_clashes, clashes)

    def test_get_clashes_empty(self):
        meetings =[]
        clashes = Meeting.get_clashes(meetings)

        self.assertListEqual([], clashes)
