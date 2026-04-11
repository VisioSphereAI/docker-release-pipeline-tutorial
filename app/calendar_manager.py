from datetime import datetime, timedelta
import calendar as cal


class EventCalendar:
    """Simple event calendar management."""

    def __init__(self, task_manager=None):
        self.events = {}
        self.task_manager = task_manager

    def add_event(self, date_str, event_name):
        """Add an event to a specific date."""
        if date_str not in self.events:
            self.events[date_str] = []
        self.events[date_str].append(event_name)

    def get_events(self, date_str):
        """Get events for a specific date."""
        return self.events.get(date_str, [])

    def get_tasks_for_date(self, date_str):
        """Get tasks for a specific date."""
        if not self.task_manager:
            return []

        # Parse the date string to get year, month, day
        try:
            year, month, day = map(int, date_str.split('-'))
            target_date = datetime(year, month, day).date()

            # Get all tasks and filter by due date
            all_tasks = self.task_manager.get_all_tasks()
            date_tasks = []

            for task in all_tasks:
                if hasattr(task, 'due_date') and task.due_date == target_date:
                    date_tasks.append(task)

            return date_tasks
        except (ValueError, AttributeError):
            return []

    def get_calendar_data(self, year, month):
        """Get calendar data for a specific month."""
        cal_data = []
        month_calendar = cal.monthcalendar(year, month)

        for week in month_calendar:
            week_data = []
            for day in week:
                if day == 0:
                    week_data.append({"day": None, "events": [], "tasks": []})
                else:
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    week_data.append({
                        "day": day,
                        "date": date_str,
                        "events": self.get_events(date_str),
                        "tasks": self.get_tasks_for_date(date_str),
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
