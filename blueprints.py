from flask import Blueprint, jsonify, request
from sqlalchemy.sql.functions import current_user

from schemas import *
from models import *
from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth


blpr = Blueprint("music", __name__)

auth = HTTPBasicAuth()



@auth.verify_password
def verify_password(username, password):
    session = Session()
    user = session.query(User).filter_by(email=username).one()
    if check_password_hash(user.password, password):
        return user


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


@blpr.route("/user/<int:id>", methods = ["DELETE"])
@auth.login_required
def del_user(id):
    try:
        session = Session()
        user = auth.current_user()
        if user.id != id:
            return (jsonify({"code": 400, "error": "It is not your user"}))
        if session.query(User).filter_by(id=id).one() == None:
            return(jsonify({"code": 400 ,"error": "Wrong id"}))

        session.query(User).filter_by(id=id).delete()
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong id"}))
    return jsonify({"User deleted ": 200})


@blpr.route("/playlist", methods = ["POST"])
@auth.login_required
def add_playlist():
    try:
        playlist_data = NewPlayList().load(request.json)
        playlist_obj = PlayList(**playlist_data)

        session = Session()
        user = auth.current_user()
        playlist_obj.owner_id = user.id
        session.add(playlist_obj)
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist data"}))

    return(jsonify(PlayListInfo().dump(playlist_obj))), 200
    

@blpr.route("/playlist/<int:id>", methods = ["GET"])
@auth.login_required
def get_playlist(id):
    try:
        session = Session()
    
        playlist_obj = session.query(PlayList).filter_by(id = id).one()
        if playlist_obj.status == 'private':
            user = auth.current_user()
            if user.id != playlist_obj.owner_id:
                return(jsonify({"code": 400 ,"error": "You aren`t owner"}))

    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist id"}))

    return jsonify(PlayListInfo().dump(playlist_obj)), 200


@blpr.route("/playlist/<int:id>", methods = ["PUT"])
@auth.login_required
def put_playlist(id):
    try:
        session = Session()
    
        playlist_data = NewPlayList().load(request.json)
        orig_playlist_data = session.query(PlayList).filter_by(id = id).one()
        if orig_playlist_data.status == 'private':
            user = auth.current_user()
            if user.id != orig_playlist_data.owner_id:
                return(jsonify({"code": 400 ,"error": "You aren`t owner"}))
        for key, value in playlist_data.items():
            setattr(orig_playlist_data, key, value)
            
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist data"}))

    return jsonify(PlayListInfo().dump(orig_playlist_data)), 200


@blpr.route("/playlist/<int:id>", methods = ["DELETE"])
@auth.login_required
def del_playlist(id):
    try:
        session = Session()
        playlist_obj = session.query(PlayList).filter_by(id=id).one()
        if playlist_obj.status == 'private':
            user = auth.current_user()
            if user.id != playlist_obj.owner_id:
                return (jsonify({"code": 400, "error": "You aren`t owner"}))
        if session.query(PlayList).filter_by(id=id).one() == None:
            return(jsonify({"code": 400 ,"error": "Wrong playlist id"}))

        session.query(PlayList).filter_by(id=id).delete()
        session.commit()
    except Exception:
        return(jsonify({"code": 400 ,"error": "Wrong playlist id"}))

    return jsonify({"Playlist deleted ": 200})
