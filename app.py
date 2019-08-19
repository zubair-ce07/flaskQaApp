from flask import Flask, jsonify, render_template
import json
import os
import sys
from flask_cors import CORS, cross_origin

# global variables
num = 0
last_choice = 'empty'
questionnaire_key = ''
user_choice = []
data = {}

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
with open('static/data_qa.json') as f:
    data = json.load(f)
    print(data, file=sys.stdout)

@app.route('/')
@cross_origin()
def appStart():
    return render_template('index.html')

@app.route('/<int:index>/Start')
@cross_origin()
def selectQuestionnare(index):
    global num, last_choice, questionnaire_key, user_choice
    num = 0
    last_choice = 'empty'
    user_choice.clear()
    questionnaire_key = 'questionnaire_' + str(index)

    user_choice.append(data[questionnaire_key][0]['question'])
    print(user_choice, file=sys.stdout)
    return jsonify(data[questionnaire_key][0])


@app.route('/<int:index>/<string:option>')
@cross_origin()
def GetQuestion(index, option):
    global num, last_choice, questionnaire_key
    num = num + 1
    response = {}
    option = option.title()
    user_choice.append(option)
    if last_choice != 'empty':
        # if option not in data[questionnaire_key][num][last_choice]:
        #     response = "The Option entered is invalid "
        #     return jsonify(response)
        response = data[questionnaire_key][num][last_choice][option]
    else:
        if option != 'Yes' and option != 'No':
            last_choice = option

        response = data[questionnaire_key][num][option]

    if option == 'No' or num == len(data[questionnaire_key]) - 1:
        for elem in user_choice:
            print(elem, file=sys.stdout)

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
