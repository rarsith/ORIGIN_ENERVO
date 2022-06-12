from datetime import datetime

class DateTime(object):
    def __init__(self):
        self.time_now = datetime.now()

    @property
    def return_time(self):
        return self.time_now.strftime("%H:%M")

    @property
    def return_date(self):
        return self.time_now.strftime("%Y-%m-%d")

