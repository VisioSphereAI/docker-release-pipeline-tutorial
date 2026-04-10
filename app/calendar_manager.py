from datetime import datetime, timedelta
import calendar as cal


class EventCalendar:
    """Simple event calendar management."""

    def __init__(self):
        self.events = {}

    def add_event(self, date_str, event_name):
        """Add an event to a specific date."""
        if date_str not in self.events:
            self.events[date_str] = []
        self.events[date_str].append(event_name)

    def get_events(self, date_str):
        """Get events for a specific date."""
        return self.events.get(date_str, [])

    def get_calendar_data(self, year, month):
        """Get calendar data for a specific month."""
        cal_data = []
        month_calendar = cal.monthcalendar(year, month)

        for week in month_calendar:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append({"day": None, "events": []})
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    week_data.append({
                        "day": day,
                        "date": date_str,
                        "events": self.get_events(date_str),
                        "is_today": self._is_today(year, month, day),
                    })
            cal_data.append(week_data)

        return cal_data

    @staticmethod
    def _is_today(year, month, day):
        today = datetime.utcnow().date()
        return today == datetime(year, month, day).date()

    @staticmethod
    def get_months_years(offset=0):
        """Get year and month with offset."""
        today = datetime.utcnow()
        target = today + timedelta(days=30 * offset)
        return target.year, target.month

    @staticmethod
    def get_month_name(month):
        """Get the name of the month."""
        return cal.month_name[month]
