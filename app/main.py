import logging
from pkg_resources import resource_filename

from app.utils import file_utils
from app.dq.validator import CalendarValidator
from app.meeting.meeting import Meeting


DATA_PATH = resource_filename(__name__, 'data/sample_data.json')
SCHEMA_PATH = resource_filename(__name__, 'dq/resources/meeting_schema.json')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def run():

    logger.info("Retrieving data")
    cal_data = file_utils.get_json_data(DATA_PATH)

    validator = CalendarValidator(SCHEMA_PATH)
    for record in cal_data:
        validator.validate_record(record)
    logging.info("All records validated")

    logging.info("Ordering and grouping data")
    meeting_data = [Meeting(record) for record in cal_data]
    ordered_meetings = Meeting.order_meeting_list(meeting_data)
    grouped_meetings = Meeting.group_meetings_by_date(ordered_meetings)

    logger.info("Calculating clashes")
    clashes = [{date: Meeting.get_clashes(meetings)} for date, meetings in grouped_meetings]

    print('No clashes' if not clashes else clashes)


if __name__ == '__main__':
    run()
