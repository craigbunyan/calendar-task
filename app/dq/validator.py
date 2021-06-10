import logging
from cerberus import Validator

from app.utils import file_utils


class CalendarValidator:
    def __init__(self, schema_path: str):
        self.schema = file_utils.get_json_data(schema_path)
        self.validator = Validator(self.schema)
        self.logger = logging.getLogger(__name__)

    def validate_record(self, record: dict) -> None:
        """
        Validates a record against the given schema.
        Returns none and raises RuntimeError for invalid records.
        :param record: dict
        :return: None
        """
        self.logger.info('validating record: %s', record)
        if not self.validator.validate(record):
            error = {'record': record, 'errors': self.validator.errors}
            self.logger.error('invalid record: %s', error)
            raise RuntimeError(f"A record as been flagged as invalid: {error}")
