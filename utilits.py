import enum


class DateType(enum.IntEnum):
    HOLIDAY = 1
    MESSAGE = 2

class DateDataFields(enum.Enum):
    date = 'date'
    message = 'message'
    type = 'type'