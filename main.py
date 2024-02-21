from flask import Flask, request, jsonify
from db_manager import DBManager
from uuid import uuid4
import json

app = Flask(__name__)
app.config['db_manager'] = DBManager(app, 'GRE_3333.db')

@app.get("/")
def hello_world():
    """
    Returns a JSON response with a greeting message.
    """
    return jsonify({"message": "Hello, World!"})

@app.route("/db/execute", methods=['POST'])
def db_execute_query():
    """
    Execute a database query.

    Args:
        execute_query_payload (DBRequestPayload): The payload containing the query to execute.
        app_request (Request): The FastAPI request object.

    Returns:
        jsonify: The result of the query execution.
    """
    data = json.loads(request.data.decode('utf-8'))
    action_uuid = str(uuid4().hex)
    if app.config['db_manager'].update_action_id(action_uuid):
        result = app.config['db_manager'].db_execute(data['query'], action_uuid)
    return jsonify(result)

@app.route("/db/format", methods=['GET'])
def db_get_format():
    """
    Get the format of the database.

    Args:
        app_request (Request): The FastAPI request object.

    Returns:
        jsonify: The format of the database.
    """
    all_result = []

    action_uuid = str(uuid4().hex)
    if app.config['db_manager'].update_action_id(action_uuid):
        result = app.config['db_manager'].db_execute("PRAGMA table_info(Vocabulary)", action_uuid)
        all_result.append(result)

    action_uuid = str(uuid4().hex)
    if app.config['db_manager'].update_action_id(action_uuid):
        result = app.config['db_manager'].db_execute("PRAGMA table_info(Meaning)", action_uuid)
        all_result.append(result)

    return jsonify(all_result)


if __name__ == '__main__':
    app.run(debug=True)
