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
        user_id_str = habit_logs['user_id']

        date = datetime.strptime(habit_logs['date'], '%Y-%m-%d')

        result = []
        for habit_id_str in habit_logs['habits']:
            # user_id & habit_id validation
            self.user_service.get_by_id(user_id_str)
            self.habit_service.get_by_id(habit_id_str)

            habit_log = {'user_id': ObjectId(user_id_str), 'habit_id': ObjectId(habit_id_str),
                         'date': date, 'check': False}
            result.append(habit_log)

        self.habit_log_model.add_list(result)

    def get_list(self, user_id: str, date: str):
        self.user_service.get_by_id(user_id)
        return self.habit_log_model.get_list(user_id, datetime.strptime(date, '%Y-%m-%d'))

    def set_check(self, log_id: str, user_id: str):
        self.user_service.get_by_id(user_id)
        return self.habit_log_model.set_check(log_id)
