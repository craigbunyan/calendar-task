import logging
import itertools
from datetime import datetime, timedelta


class Meeting:

    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M'

    def __init__(self, cal_record: dict):
        self.name = cal_record.get('meeting_name')
        self.date = datetime.strptime(cal_record.get('date'), self.DATE_FORMAT)
        self.start_time = datetime.strptime(cal_record.get('start_time'), self.TIME_FORMAT).time()
        self.duration = cal_record.get('duration')
        self.start = self.date + timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        self.end = self.start + timedelta(minutes=self.duration)
        self.logger = logging.getLogger(__name__)

    @classmethod
    def order_meeting_list(cls, meet_list: list) -> list:
        """
        Returns list of Meetings ordered by the start datetime.
        Ordering is required for grouping and comparing clashes.
        :param meet_list: list
        :return: list
        """
        return sorted(meet_list, key=lambda x: x.start)

    @classmethod
    def group_meetings_by_date(cls, meet_list: list) -> itertools:
        """
        Returns iterable of tuples (date, Meeting) grouped by date datetime.
        Requires input to be sorted to output distinct groups.
        This will open functionality to only compare for required dates reducing compute when needed.
        :param meet_list: list
        :return: iterable
        """
        return itertools.groupby(meet_list, key=lambda x: x.date)

    @classmethod
    def get_clashes(cls, meet_list: list) -> list:
        """
        Compares a sorted list of Meetings and returns a list of Meeting names that conflict with the Meeting before it.
        Requires input list to be sorted by start datetime.
        :param meet_list: list
        :return: list
        """
        clashes = []
        previous_meeting_end = datetime.min
        for meeting in meet_list:
            if meeting.start < previous_meeting_end:
                clash = (previous_meeting_name, meeting.name)
                clashes.append(clash)
                meeting.logger.info("Clash detected for: %s", clash)
            previous_meeting_end = meeting.end
            previous_meeting_name = meeting.name
        return clashes
