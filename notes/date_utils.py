"""
Helper functions for working with dates, such as date formats and file dates
"""

from datetime import datetime

def convert_date_format(orig_date: str, 
    check_formats: list[str]=['%y%m%d', '%Y/%m/%d', '%m/%d/%Y'], 
    new_format: str='%Y-%m-%d') -> str: 
    """
    Convert a date string into a desired date format, checking the date string
    against several different date formats it may originally be in

    Arguments:
        orig_date: The date to convert the format of, as a string
        check_formats: The date formats that `orig_date` might be in and can 
            be converted from, in python `datetime` format codes. The default 
            date formats checked for are
            - `%y%m%d` = `YYMMDD`, e.g. 250531
            - `%Y/%m/%d` = `YYYY/MM/DD`, e.g. 2025/05/31
            - `%m/%d/%Y` = `MM/DD/YYYY`, e.g. 05/31/2025
        new_format: The date format to convert the `orig_date` to. Dates in 
            properties should always be in `YYYY-MM-DD` format (`%Y-%m-%d` in
            python `datetime` format code)
    
    Returns:
        A date in the desired date format, as a string. If the date could not 
        be converted, the original date string is returned
    """
    orig_date = str(orig_date).strip()

    is_converted = False
    new_date = orig_date
    for f in check_formats:
        if not is_converted: 
            try: 
                dt = datetime.strptime(orig_date, f)
                new_date = datetime.strftime(dt, new_format)
                is_converted = True
            except ValueError: 
                pass
    
    if not is_converted: 
        print('could not convert date: {}'.format(orig_date))
    
    return new_date