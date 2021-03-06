from dateutil.parser import parse as date_parse


class Birthday(object):
    """
    Birthday object to handle various Graph return formats
    """

    def __init__(self, datestring):
        """
            Parses Graph birthday format to set indication flags,
            possible values:

            MM/DD/YYYY
            MM/DD
            YYYY
        """
        parts = datestring.split('/')

        self.has_year = len(parts) == 3 or len(parts) == 1
        self.has_date = len(parts) == 3 or len(parts) == 2

        self.datetime = date_parse(datestring)

    def format(self, format):
        return self.datetime.strftime(format)
