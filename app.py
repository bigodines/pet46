from flask import Flask, request, jsonify
from storage.database import init_db
from storage.repository import HabitRepository
import json
from sqlalchemy.orm import configure_mappers

app = Flask(__name__)

def load_config():
    try:
        with open('config.json', 'r') as config:
            return json.load(config)
    except Exception as e:
        print(f'Cannot load config file ./config.json: {e}')

@app.route('/healthcheck')
def get_healthcheck():
    '''
    healthcheck route
    '''
    return 'API is up and running!'

@app.route('/habit', methods=['POST'])
def post_habit():
    """
    Create a new habit.
    """
    data = request.json
    habit = habit_repo.add_habit(data['name'])
    return jsonify({'habit_id': habit.id, 'name': habit.name, 'checkin_count': habit.checkin_count})

@app.route('/checkin', methods=['POST'])
def post_checkin():
    """
    Main "checkin" endpoint for habit tracking.
    """
    data = request.json
    habit = habit_repo.add_checkin(data['habit_id'])
    return jsonify({'habit_id': habit.id, 'checkin_count': habit.checkin_count})

@app.route('/checkin', methods=['GET'])
def get_checkin():
    """
    Debugging "checkin" endpoint for habit tracking.
    """
    habit_id = request.args.get('habits_id')
    habit = habit_repo.get_habit(habit_id)
    if habit is None:
        return jsonify({'error': f'Habit with id {habit_id} does not exist'})
    return jsonify({'habit_id': habit.id, 'checkin_count': habit.checkin_count})

# Load configuration and initialize database
config = load_config()
db_session = init_db(config['db_path'])
configure_mappers()  # Ensure all mappers are configured
habit_repo = HabitRepository(db_session)

if __name__ == '__main__':
    app.run(debug=True)
