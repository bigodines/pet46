from flask import Flask, request, jsonify
from storage.sqlite import SQLiteStorage
import json

app = Flask(__name__)

def load_config():
    try:
        with open('config.json', 'r') as config:
            return json.load(config)
    except:
        print('Cannot load config file ./config.json')

@app.route('/checkin', methods=['POST'])
def api_checkin():
    '''
    This is the main "I'm doing what I should" method. More on this in a future README.md update.
    '''
    data = request.json

    return jsonify({'result': data['num'] + 1})


config = load_config()
    
db = SQLiteStorage(config)
app.run(debug=True)

