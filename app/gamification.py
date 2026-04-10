from datetime import datetime


class GamificationManager:
    """Manage user gamification: points, badges, achievements."""

    BADGES = {
        "task_master": {"name": "Task Master", "icon": "🎯", "requirement": 10},
        "calendar_pro": {"name": "Calendar Pro", "icon": "📅", "requirement": 5},
        "speed_demon": {"name": "Speed Demon", "icon": "⚡", "requirement": 3},
        "organizer": {"name": "Organizer", "icon": "📋", "requirement": 50},
        "night_owl": {"name": "Night Owl", "icon": "🦉", "requirement": 10},
    }

    def __init__(self):
        self.users = {}
        self.leaderboard = {}

    def get_or_create_user(self, user_id):
        """Get or create a user profile."""
        if user_id not in self.users:
            self.users[user_id] = {
                "id": user_id,
                "username": f"Player_{user_id}",
                "avatar": "🤖",
                "points": 0,
                "level": 1,
                "badges": [],
                "tasks_completed": 0,
                "events_created": 0,
                "created_at": datetime.utcnow().isoformat(),
            }
        return self.users[user_id]

    def add_points(self, user_id, points, reason=""):
        """Add points to a user."""
        user = self.get_or_create_user(user_id)
        user["points"] += points
        user["level"] = max(1, user["points"] // 100 + 1)
        self._check_achievements(user_id)
        return user

    def add_badge(self, user_id, badge_key):
        """Add a badge to a user."""
        user = self.get_or_create_user(user_id)
        if badge_key not in user["badges"] and badge_key in self.BADGES:
            user["badges"].append(badge_key)
            return True
        return False

    def increment_task_count(self, user_id):
        """Increment task completion count."""
        user = self.get_or_create_user(user_id)
        user["tasks_completed"] += 1
        self.add_points(user_id, 10, "task_completed")
        self._check_achievements(user_id)

    def increment_event_count(self, user_id):
        """Increment event creation count."""
        user = self.get_or_create_user(user_id)
        user["events_created"] += 1
        self.add_points(user_id, 5, "event_created")

    def set_avatar(self, user_id, avatar):
        """Set user avatar."""
        user = self.get_or_create_user(user_id)
        user["avatar"] = avatar
        return user

    def set_username(self, user_id, username):
        """Set user username."""
        user = self.get_or_create_user(user_id)
        user["username"] = username
        return user

    def _check_achievements(self, user_id):
        """Check for new achievements."""
        user = self.get_or_create_user(user_id)

        if user["tasks_completed"] >= 10:
            self.add_badge(user_id, "task_master")
        if user["events_created"] >= 5:
            self.add_badge(user_id, "calendar_pro")
        if user["points"] >= 500:
            self.add_badge(user_id, "organizer")

    def get_leaderboard(self, limit=10):
        """Get top players by points."""
        sorted_users = sorted(
            self.users.values(),
            key=lambda u: u["points"],
            reverse=True,
        )
        return sorted_users[:limit]

    def get_user_stats(self, user_id):
        """Get user statistics and progress."""
        user = self.get_or_create_user(user_id)
        badges_earned = [self.BADGES[b] for b in user["badges"]]

        return {
            "user": user,
            "badges_earned": badges_earned,
            "total_badges": len(self.BADGES),
            "progress": {
                "task_master": min(
                    user["tasks_completed"] / self.BADGES["task_master"]["requirement"],
                    1.0,
                ),
                "calendar_pro": min(
                    user["events_created"] / self.BADGES["calendar_pro"]["requirement"],
                    1.0,
                ),
                "organizer": min(
                    user["points"] / self.BADGES["organizer"]["requirement"],
                    1.0,
                ),
            },
        }
