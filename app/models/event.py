from datetime import datetime
import re

def format_date(date_str: str) -> str:
    """
    Converts a date string like 'January 5th, 2025' or 'Jan 5th, 2025' to 'MM/DD/YYYY'.
    Returns the original string if parsing fails.
    """
    if not date_str:
        return ""
    # Remove ordinal suffixes (st, nd, rd, th)
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%m/%d/%Y")
        except Exception:
            continue
    return date_str

class Event:
    def __init__(
        self,
        title: str,
        start_date: str,
        end_date: str,
        start_time: str,
        end_time: str,
        location: str,
        event_link: str,
        description: str,
        brackets: list
    ):
        self.title = title
        self.start_date = format_date(start_date)
        self.end_date = format_date(end_date)
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.event_link = event_link
        self.description = description
        self.brackets = brackets  # List of dicts: [{'name': ..., 'format': ...}, ...]

    def to_dict(self):
        return {
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "event_link": self.event_link,
            "description": self.description,
            "brackets": self.brackets,
        }