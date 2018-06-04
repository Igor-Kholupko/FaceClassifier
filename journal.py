import sys
import time


monthname = [None,
             'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


def log_date_time_string():
    """Return the current time formatted for logging."""
    now = time.time()
    year, month, day, hh, mm, ss, x, y, z = time.localtime(now)
    s = "%02d/%3s/%04d %02d:%02d:%02d" % (
            day, monthname[month], year, hh, mm, ss)
    return s


def log_message(format, *args):
    sys.stderr.write(" - - [%s] %s\n" % (log_date_time_string(), format % args))
