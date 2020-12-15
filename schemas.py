from marshmallow import Schema, fields, post_load, validates

class UserLogInfo(Schema):
    email = fields.Email()
    password = fields.String(required = True)

class NewUser(Schema):
    username = fields.String(required = True)
    email = fields.Email(required = True)
    password = fields.String(required = True)


class UserInfo(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.Email()

class NewPlayList(Schema):
    name = fields.String(required = True)
    owner_id = fields.Integer(required = True)
    songs = fields.List(fields.String())
    status = fields.String(required = True)

    @validates('status')
    def validate_status(self, status):
        if status != 'public' and status != 'private':
            raise ValidationError('invalid status')
            
class PlayListInfo(Schema):
    id = fields.Integer()
    name = fields.String()
    owner_id = fields.Integer()
    songs = fields.List(fields.String())
    status = fields.String()
