from flask import Flask
from blueprints import blpr


def db_error():
    return jsonify(
        {
            "code": 500,
            "type": "DATABASE_ERROR",
        }
    )

app = Flask(__name__)

app.register_blueprint(blpr, url_prefix="/music")

app.register_error_handler(Exception, db_error)

@app.route('/')
def hello_world():
    return 'Home Page'


if __name__ == '__main__':
    app.run(debug = True)

