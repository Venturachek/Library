from datetime import datetime, timedelta





def two_weeks_from_now():
    return datetime.now() + timedelta(days=14)

