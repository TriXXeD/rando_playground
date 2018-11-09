from flask import Flask, url_for, request, json, Response, jsonify
from flask import request, jsonify
from functools import wraps

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Hello World!'


@app.route('/series')
def api_series_list():
    return 'List of ' + url_for('api_series_list')


@app.route('/series/<series_id>')
def api_series(series_id):
    return 'You are viewing ' + series_id


@app.route('/hello')
def hello():
    if 'name' in request.args:
        return 'Hello ' + request.args['name']
    else:
        return "Hello Anon, member of the Legion"


@app.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET \n"
    elif request.method == 'POST':
        return "ECHO: POST \n"
    elif request.method == 'PUT':
        return "ECHO: PUT \n"
    elif request.method == 'DELETE':
        return "ECHO: DELETE \n"
    elif request.method == 'PATCH':
        return "ECHO: PATCH \n"


@app.route('/message', methods=['POST'])
def api_message():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text msg: " + request.data
    elif request.headers['Content-Type'] == 'application/json':
        return "JSON msg: " + json.dumps(request.json)
    elif request.headers['Content-Type'] == 'application/octet-stream':
        with open('./binary', 'wb') as f:
            f.write(request.data)
        return "Binary msg"
    else:
        return "415: Media not supported"


@app.route('/response', methods=['GET'])
def response():
    data = {
        'hello': 'world',
        'number': 3,
    }
    # js = json.dumps(data)
    # resp = Response(js, status=200, mimetype='application/json')
    resp = jsonify(data)
    resp.status_code = 200
    resp.headers['Link'] = 'http://dead_link.com'

    return resp


@app.errorhandler(404)
def not_found(error=None):
    msg = {
        'status': 404,
        'message': 'Not Found, 404: ' + request.url,
    }
    resp = jsonify(msg)
    resp.status_code = 404
    return resp


@app.route('/users/<userid>', methods=['GET'])
def api_users(userid):
    users = {'1': 'John',
             '2': 'Steve',
             '3': 'Bill',
             }
    if userid in users:
        return jsonify({userid: users[userid]})
    else:
        return not_found()


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def authenticate():
    msg = {'message': "Authenticate."}
    resp = jsonify(msg)
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()
        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/secrets')
@requires_auth
def secrets():
    return "Thanos did nothing wrong"


if __name__ == '__main__':
    app.run(debug=True)
