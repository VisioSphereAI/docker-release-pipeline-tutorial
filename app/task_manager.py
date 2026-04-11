from datetime import datetime, date


class Task:
    """Task object with due date support."""

    def __init__(self, task_id, title, description="", priority="medium", due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.utcnow().isoformat()
        self.due_date = due_date  # date object or None


class TaskManager:
    """Simple task/todo list management."""

    def __init__(self):
        self.tasks = {}
        self.task_id_counter = 1

    def add_task(self, title, description="", priority="medium", due_date=None):
        """Add a new task."""
        task_id = self.task_id_counter
        self.task_id_counter += 1

        # Parse due_date if it's a string
        if isinstance(due_date, str):
            try:
                due_date = datetime.fromisoformat(due_date).date()
            except ValueError:
                due_date = None

        task = Task(task_id, title, description, priority, due_date)
        self.tasks[task_id] = task

        return task_id

    def get_task(self, task_id):
        """Get a single task."""
        return self.tasks.get(task_id)

    def get_all_tasks(self):
        """Get all tasks sorted by priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}

        return sorted(
            self.tasks.values(),
            key=lambda t: (t.completed, priority_order.get(t.priority, 3)),
        )

    def update_task(self, task_id, **kwargs):
        """Update a task."""
        if task_id not in self.tasks:
            return False

        task = self.tasks[task_id]
        allowed_fields = {"title", "description", "priority", "completed", "due_date"}
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field == "due_date" and isinstance(value, str):
                    try:
                        value = datetime.fromisoformat(value).date()
                    except ValueError:
                        value = None
                setattr(task, field, value)

        return True

    def delete_task(self, task_id):
        """Delete a task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_stats(self):
        """Get task statistics."""
        completed = sum(1 for t in self.tasks.values() if t.completed)
        total = len(self.tasks)

        return {
            "total": total,
            "completed": completed,
            "pending": total - completed,
            "completion_rate": int((completed / total * 100) if total > 0 else 0),
        }
