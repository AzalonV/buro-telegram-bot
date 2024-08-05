import re
from datetime import datetime

class Validators:

    @staticmethod
    async def event_text(text):
        if len(text) > 1000:
            return False
        return True
    
    @staticmethod
    async def event_time(time):
        pattern = re.compile(r'^(2[0-3]|[01][0-9]):[0-5][0-9]$')
        result = pattern.match(time)
        return bool(result)
    
    @staticmethod
    async def event_date(date):
        try:
            datetime.strptime(date, '%m.%d')
            return True
        except ValueError:
            return False