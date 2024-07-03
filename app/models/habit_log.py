from typing import Dict

from bson import ObjectId


class HabitLog:
    def __init__(self, db, user_model, habit_model):
        self.collection = db["habit_logs"]
        self.user_model = user_model
        self.habit_model = habit_model

    # 특정 날짜에 기록할 습관들 선택
    # habit_logs = {'user_id': 'user_id1', 'date': '2024-07-04', 'habits': ['habit_id1', 'habit_id2']
    def add_list(self, habit_logs: Dict[str, str | Dict]):
        user_id_str = habit_logs["user_id"]
        from datetime import datetime

        date = datetime.strptime(habit_logs["date"], "%Y-%m-%d")

        for habit_id_str in habit_logs["habits"]:
            # user_id & habit_id validation
            self.user_model.get_by_id(user_id_str)
            self.habit_model.get_by_id(habit_id_str)

            habit_log = {
                "user_id": ObjectId(user_id_str),
                "habit_id": ObjectId(habit_id_str),
                "date": date,
                "check": False,
            }
            self.collection.insert_one(habit_log)

    def list(self, user_id_str, date):
        self.user_model.get_by_id(user_id_str)
        logs = self.collection.find({"user_id": ObjectId(user_id_str), "date": date})

        result = []
        for log in logs:
            result.append(
                {
                    "log_id": log["_id"],
                    "date": log["date"],
                    "habit_id": log["habit_id"],
                    "check": log["check"],
                }
            )

        return result

    def set_check(self, log_id: str, user_id: str, check: bool):
        habit_log = self.collection.find_one({"_id": ObjectId(log_id)})
        if habit_log is None:
            raise ValueError(f"habit_log {log_id} not found")

        self.user_model.get_by_id(user_id)

        result = self.collection.update_one(
            {"_id": ObjectId(log_id)}, {"$set": {"check": check}}
        )
        if result.modified_count == 0:
            raise ValueError(f"habit_log {log_id} not found")

        return True
