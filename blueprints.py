from flask import Blueprint, jsonify, request
from schemas import *
from models import *


blpr = Blueprint("music", __name__)


@blpr.route("/user", methods = ["POST"])
def add_user():
    try:
        user_data = NewUser().load(request.json)
        user_obj = User(**user_data)

        session = Session()
        session.add(user_obj)
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "wrong user data"}))

    return(jsonify(UserInfo().dump(user_obj))), 200


@blpr.route("/user/login", methods = ["GET"])
def login_user():
    user_data = UserLogInfo().load(request.json)
    return("Successful login"), 200


@blpr.route("/user/logout", methods = ["GET"])
def logout_user():
    return("Successful logout"), 200


@blpr.route("/user/<int:id>", methods = ["DELETE"])
def del_user(id):
    try:
        session = Session()
        session.query(User).filter_by(id=id).delete()
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong id"}))
    return jsonify({"User deleted ": 200})


@blpr.route("/playlist", methods = ["POST"])
def add_playlist():
    try:
        playlist_data = NewPlayList().load(request.json)
        playlist_obj = PlayList(**playlist_data)

        session = Session()
        session.add(playlist_obj)
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist data"}))

    return(jsonify(PlayListInfo().dump(playlist_obj))), 200
    

@blpr.route("/playlist/<int:id>", methods = ["GET"])
def get_playlist(id):
    try:
        session = Session()
    
        playlist_obj = session.query(PlayList).filter_by(id = id).one()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist id"}))

    return jsonify(PlayListInfo().dump(playlist_obj)), 200


@blpr.route("/playlist/<int:id>", methods = ["PUT"])
def put_playlist(id):
    try:
        session = Session()
    
        playlist_data = NewPlayList().load(request.json)
        orig_playlist_data = session.query(PlayList).filter_by(id = id).one()

        for key, value in playlist_data.items():
            setattr(orig_playlist_data, key, value)
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist data"}))

    return jsonify(PlayListInfo().dump(orig_playlist_data)), 200


@blpr.route("/playlist/<int:id>", methods = ["DELETE"])
def del_playlist(id):
    try:
        session = Session()
        session.query(PlayList).filter_by(id=id).delete()
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist id"}))

    return jsonify({"Playlist deleted ": 200})
