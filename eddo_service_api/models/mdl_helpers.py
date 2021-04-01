from pytz import timezone
from datetime import datetime
UTC = timezone('Asia/Almaty')

def time_now():
    return datetime.now(UTC)