from typing import Dict
from datetime import datetime
from bson import ObjectId


class HabitLog:
    def __init__(self, db):
        self.collection = db["habit_logs"]

    def add_list(self, habit_logs: Dict[str, str | Dict]):
        self.collection.insert_many(habit_logs)

    def get_list(self, user_id_str, date):
        logs = self.collection.find({"user_id": ObjectId(user_id_str), "date": date})

        result = []
        for log in logs:
            result.append(
                {
                    "_id": str(log["_id"]),
                    "date": log["date"],
                    "habit_id": str(log["habit_id"]),
                    "check": log["check"],
                }
            )

        return result

    def set_check(self, user_id: str, date: str, habit_id: str):
        habit_log = self.collection.find_one(
            {
                "user_id": ObjectId(user_id),
                "date": datetime.strptime(date, "%Y-%m-%d"),
                "habit_id": ObjectId(habit_id),
            }
        )
        if habit_log is None:
            self.collection.insert_one(
                {
                    "user_id": ObjectId(user_id),
                    "date": datetime.strptime(date, "%Y-%m-%d"),
                    "habit_id": ObjectId(habit_id),
                    "check": True,
                }
            )
            return True
        result = self.collection.update_one(
            {"_id": habit_log["_id"]}, {"$set": {"check": not habit_log["check"]}}
        )

        if result.modified_count == 0:
            raise ValueError(f"Error occurred during setting check value")

        return True
