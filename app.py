from config import *

from controllers.note_controller import *
from controllers.user_controller import *

db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World'



if __name__ == '__main__':
    app.run(debug = True)
