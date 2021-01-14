from flask import Flask
from flask_httpauth import HTTPBasicAuth
from blueprints import blpr

app = Flask(__name__)
auth = HTTPBasicAuth()
app.register_blueprint(blpr, url_prefix="/music")


#app.register_error_handler(Exception, db_error)



if __name__ == '__main__':
    app.run(debug = True)

