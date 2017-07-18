from datetime import datetime


class Birthday(object):
    """
    Birthday object to handle various Graph return formats
    """
    def __init__(self, datestring):
        """
            Parses Graph birthday format to set indication flags, possible values:

            MM/DD/YYYY
            MM/DD
            YYYY
        """
        parts = datestring.split('/')

        self.has_year = len(parts) == 3 or len(parts) == 1
        self.has_date = len(parts) == 3 or len(parts) == 2

        if len(parts) == 3:
            format = '%m/%d/%Y'
        elif len(parts) == 2:
            format = '%m/%d'
        else:
            format = '%Y'

        self.date = datetime.strptime(datestring, format).date()

    def format(self, format):
        return self.date.strftime(format)
