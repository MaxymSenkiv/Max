from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api/v1/hello-world-25')
def start():
    return 'Hello World 25'

if __name__ == '__main__':
    app.run()
