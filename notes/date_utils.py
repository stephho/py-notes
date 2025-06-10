"""
Helper functions for working with dates, such as date formats and file dates
"""

import os
from datetime import datetime
import subprocess

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


def get_file_created_date(filename: str, format: bool=True) -> str | datetime:
    """
    Get a file's created date, according to the operating system

    Note: This has only been tested on macOS

    Arguments:
        filename: The file to get the created date of
        format: If `True`, the file's created date is returned as a string in 
            `YYYY-MM-DD` format (i.e., `%Y-%m-%d` in python `datetime` format 
            code). If `False`, the file's created date is returned as a 
            `datetime` object
    
    Returns:
        The file's created date, as either a string or datetime object
    """
    # on macOS, os.path.getctime is not accurate, use st_birthtime instead
    file_created_time = os.stat(filename).st_birthtime
    file_created_time = datetime.fromtimestamp(file_created_time)
    
    file_created_date = file_created_time
    if format: 
        file_created_date = file_created_time.strftime('%Y-%m-%d')
    
    return file_created_date


def change_file_created_date(filename: str, new_created_date: str | datetime):
    """
    Update a file's created date in the operating system

    Note: This has only been tested on macOS

    Arguments:
        filename: The file to change the created date of
        new_created_date: The date to change the file's created date to. This
            may be provided as either a string in `YYYY-MM-DD` format (i.e., 
            `%Y-%m-%d` in python `datetime` format code; in which case, 
            timestamp is ignored) or a `datetime` object
    """
    if type(new_created_date) == str:
        try: 
            new_created_date = datetime.strptime(new_created_date, '%Y-%m-%d')
        except ValueError: 
            print('cannot convert date {}, did not change file created date'
                .format(new_created_date))
            return

    created_dt = new_created_date.strftime('%m/%d/%Y %H:%M:%S')

    try: 
        command = 'SetFile -d "{}" "{}"'.format(created_dt, filename)
        subprocess.run(command, shell=True, check=True, timeout=15, 
            capture_output=True)
        print('file created date successfully changed to {}'
            .format(new_created_date))
    except subprocess.CalledProcessError as e:
        print(e)
