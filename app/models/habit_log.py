from typing import Dict

from bson import ObjectId


class HabitLog:
    def __init__(self, db):
        self.collection = db['habit_logs']

    def add_list(self, habit_logs: Dict[str, str | Dict]):
        self.collection.insert_many(habit_logs)

    def get_list(self, user_id_str, date):
        logs = self.collection.find({'user_id': ObjectId(user_id_str), 'date': date})

        result = []
        for log in logs:
            result.append({'_id': log['_id'], 'date': log['date'],
                           'habit_id': log['habit_id'], 'check': log['check']})

        return result

    def set_check(self, log_id: str):
        habit_log = self.collection.find_one({'_id': ObjectId(log_id)})
        if habit_log is None:
            raise ValueError(f'habit_log {log_id} not found')

        result = self.collection.update_one({'_id': ObjectId(log_id)}, {'$set': {'check': not habit_log['check']}})
        if result.modified_count == 0:
            raise ValueError(f'habit_log {log_id} not found')

        return True
