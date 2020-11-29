from flask import Flask
from wsgiref.simple_server import make_server
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api/v1/hello-world-25')
def start():
    return 'Hello World 25'


with make_server('', 5000, app) as server:
    print("Server is running")

    server.serve_forever()

# if __name__ == '__main__':
#     app.run()
