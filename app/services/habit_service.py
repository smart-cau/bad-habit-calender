from bson import ObjectId


class HabitService:
    def __init__(self, habit_model, user_service):
        self.habit_model = habit_model
        self.user_service = user_service

    def add(self, habit_content, user_id):
        self.user_service.get_by_id(user_id)
        habit = {
            'content': habit_content,
            'user_id': user_id,
        }

        return self.habit_model.add(habit)

    def get_habits(self, user_id):
        return self.habit_model.get_habits(user_id)

    def get_by_id(self, habit_id):
        habit = self.habit_model.get_by_id(habit_id)

        return habit

    def delete(self, habit_id, user_id):
        return self.habit_model.delete(habit_id, user_id)
