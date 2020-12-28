# coding: utf-8

from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()
    email = fields.Email()
    password = fields.Str(load_only=True)
    firstName = fields.Str()
    lastName = fields.Str()
    bio = fields.Str()
    image = fields.Url()
    token = fields.Str(dump_only=True)
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')

    # @pre_load
    # def make_user(self, data, **kwargs):
    #     #  data = data['user']
    #     # some of the frontends send this like an empty string and some send
    #     # null
    #     if not data.get('email', True):
    #         del data['email']
    #     if not data.get('image', True):
    #         del data['image']
    #     return data
    #
    # @post_dump
    # def dump_user(self, data, **kwargs):
    #     return {'user': data}

    class Meta:
        strict = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)