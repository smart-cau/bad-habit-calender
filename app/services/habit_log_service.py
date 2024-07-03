from typing import Dict

from bson import ObjectId
from datetime import datetime


class HabitLogService:
    def __init__(self, habit_log_model, user_service, habit_service):
        self.habit_log_model = habit_log_model
        self.user_service = user_service
        self.habit_service = habit_service

    # 특정 날짜에 기록할 습관들 선택
    # habit_logs = {'user_id': 'user_id1', 'date': '2024-07-04', 'habits': ['habit_id1', 'habit_id2']
    def add_list(self, habit_logs: Dict[str, str | Dict]):
        user_id_str = habit_logs["user_id"]

        date = datetime.strptime(habit_logs["date"], "%Y-%m-%d")

        result = []
        for habit_id_str in habit_logs["habits"]:
            # user_id & habit_id validation
            self.user_service.get_by_id(user_id_str)
            self.habit_service.get_by_id(habit_id_str)

            habit_log = {
                "user_id": ObjectId(user_id_str),
                "habit_id": ObjectId(habit_id_str),
                "date": date,
                "check": True,
            }
            result.append(habit_log)

        self.habit_log_model.add_list(result)

    def get_list(self, user_id: str, date: str):
        self.user_service.get_by_id(user_id)
        logs = self.habit_log_model.get_list(
            user_id, datetime.strptime(date, "%Y-%m-%d")
        )

        habits = self.habit_service.get_habits(user_id)

        results = []
        for habit in habits:
            habit_id = str(habit["_id"])
            check = False
            for log in logs:
                if str(log["habit_id"]) == habit_id:
                    check = log["check"]
                    break
            results.append(
                {"_id": habit_id, "content": habit["content"], "check": check}
            )

        return results

    def set_check(self, user_id: str, date: str, habit_id):
        self.user_service.get_by_id(user_id)
        self.habit_service.get_by_id(habit_id)
        return self.habit_log_model.set_check(user_id, date, habit_id)

    def get_date_logs(self, user_id: str, date: str):
        self.user_service.get_by_id(user_id)
        logs = self.habit_log_model.get_list(
            user_id, datetime.strptime(date, "%Y-%m-%d")
        )

        habits = self.habit_service.get_habits(user_id)

        results = []
        for habit in habits:
            habit_id = str(habit["_id"])
            for log in logs:
                if str(log["habit_id"]) == habit_id:
                    if log["check"]:
                        results.append(
                            {
                                "_id": habit_id,
                                "content": habit["content"],
                                "check": log["check"],
                            }
                        )
                    break

        return results
