from .models import Habit, Checkin

class HabitRepository:
    '''
    Encapsulates database operations for the Habit and Checkin entities.
    '''
    def __init__(self, session):
        self.session = session

    def add_checkin(self, habit_id):
        habit = self.session.query(Habit).filter_by(id=habit_id).first()
        if habit:
            habit.checkin_count += 1
            self.session.add(Checkin(habit_id=habit_id))
            self.session.commit()
            return habit
        else:
            raise ValueError(f'Habit with id {habit_id} does not exist')

    def get_habit(self, habit_id):
        return self.session.query(Habit).filter_by(id=habit_id).first()