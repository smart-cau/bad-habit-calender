from bson import ObjectId


class Habit:
    def __init__(self, db):
        self.collection = db.habits

    def add(self, habit):
        return self.collection.insert_one(habit).inserted_id

    def get_habits(self, user_id):
        return list(self.collection.find({"user_id": user_id}))

    def delete(self, habit_id, user_id):
        habit = self.get_by_id(ObjectId(habit_id))

        if str(habit["user_id"]) != user_id:
            raise PermissionError("unauthenticated user")
        result = self.collection.delete_one({"_id": ObjectId(habit["_id"])})
        if result.deleted_count == 0:
            raise ValueError("habit deleted")
        return True

    def get_by_id(self, habit_id):
        habit = self.collection.find_one({"_id": ObjectId(habit_id)})
        if habit is None:
            raise ValueError(f"habit_id {habit_id} not found")

        return habit
