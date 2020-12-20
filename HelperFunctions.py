
from datetime import date, time, timedelta, datetime as dt
import pytz
from random import randrange
def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    datet = start + timedelta(seconds=random_second)
    return dt(datet.year, datet.month, datet.day)

def subtract_period(date_, period):
	'''
	Given a datetime date object and period as a string of any of (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y),
	find the date object one period before the given date. (POSSIBLE EDGE CASE ON LEAP YEARS)
	'''
	answer = None
	if period[-1] == 'd':
		days = int(period[0])
		d = date_ - timedelta(days)
		answer = d
	elif period[-2:] == 'mo':
		months = int(period[:-2])
		current_months = date_.month
		new_months = current_months - months
		if new_months <= 0:
			new_year = date_.year - 1
			new_month = 12 + new_months
		else:
			new_year = date_.year
			new_month = new_months
		answer = date(new_year, new_month, date_.day)
	elif period[-1:] == 'y':
		year_change = int(period[:-1])
		answer = date(date_.year - year_change, date_.month, date_.day)
	return answer

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def get_weekdays(start_dt, end_dt):
	days = []
	weekdays = [6,7]
	for dt in daterange(start_dt, end_dt):
	    if dt.isoweekday() not in weekdays:
	        days.append(dt)
	return days

def valid_US_stock_minute(datetime):
	'''
	given a datetime object and valid exchange, return if the time is in trading hours
	'''
	ny_time = get_ny_datetime(datetime)
	eastern = pytz.timezone('US/Eastern')
	if ny_time.weekday() not in {5,6}:
		open_ = time(9,30, tzinfo = eastern)
		close = time(16, tzinfo = eastern)
		if ny_time.time() >= open_ and ny_time.time() < close:
			return True
	return False

def get_ny_datetime_string(datetime):
    '''
    get current NY time as string of form "%Y-%m-%d %H:%M:%S"
    '''
    eastern = pytz.timezone('US/Eastern')
    ny_dt = datetime.astimezone(eastern)
    fmt = '%Y-%m-%d  %H:%M'
    return ny_dt.strftime(fmt)

def get_datetime_string(datetime):
	fmt = '%Y-%m-%d  %H:%M'
	return datetime.strftime(fmt)

def get_ny_datetime(datetime):
    '''
    get current NY time as datetime object of form "%Y-%m-%d %H:%M:%S"
    '''
    eastern = pytz.timezone('US/Eastern')
    ny_dt = datetime.astimezone(eastern)
    return ny_dt

def get_as_datetime(date_string):
	'''
	given a date_string of form 'YYYY-MM-DD', gets the datetime object of form YYYY-MM-DD-HH-MM-SS UTC
	'''
	return dt(int(date_string[:4]), int(date_string[5:7]), int(date_string[-2:]), tzinfo = pytz.utc)

def get_iso_format(date):
	'''
	given date in the form "yyyy-mm-dd", return ISO 8601 format (ex. '2019-04-15T09:30:00-04:00)
	'''
	return '{}T00:00:00-00:00'.format(date)

def get_iso_format_from_datetime(datetime_):
	'''
	given date in the form "yyyy-mm-dd", return ISO 8601 format (ex. '2019-04-15T09:30:00-04:00)
	'''
	
	ret =  datetime_.strftime('%Y-%m-%dT00:00-00:00')
	return ret

def get_utc_from_timestamp(timestamp):
	'''
	given a unix seconds timestamp, get the utc datetime
	'''
	d = dt.fromtimestamp(timestamp)
	return dt(d.year, d.month, d.day, hour = d.hour, minute = d.minute, second = d.second, tzinfo = pytz.utc)

def get_string_day(timestamp):
	'''
	given a unix timestamp in seconds, return the YYYY-MM-DD day.
	'''
	dt_object = dt.fromtimestamp(timestamp)
	return dt_object.strftime('%Y-%m-%d')
def get_string_day_from_datetime(date_time):
	'''
	given datetime object, return string
	'''
	return date_time.strftime('%Y-%m-%d')


def get_comma_separated_string(l):
	'''
	given list of strings l, returns string of the contents of l separated by commas
	'''
	ret = ''
	for string in l:
		ret += '{},'.format(string) 
	return ret[:-1]

def get_timestep_as_timedelta(timestep):
	'''
	Given a timestep of the string form 'nm' or 'nd' where n is an integer, returns the corresponding
	timedelta object
	'''
	if timestep[-1] == 'm':
		return timedelta(minutes = int(timestep[:-1]))
	elif timestep[-1] == 'd':
		return timedelta(days = int(timestep[:-1]))
