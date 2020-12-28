# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, create_access_token, current_user
from sqlalchemy.exc import IntegrityError
from marshmallow import fields
from sqlalchemy.orm import Session

from pybox.database import db
from pybox.exceptions import InvalidUsage
from .models import User
from .serializers import user_schema,users_schema

blueprint = Blueprint('user', __name__)


@blueprint.route('/api/users', methods=('POST',))
@use_kwargs(user_schema)
@marshal_with(user_schema)
def register_user(username, password, email, **kwargs):
    try:
        user = User(username, email, password=password, **kwargs).save()
        user.token = create_access_token(identity=user)
    except IntegrityError as e:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    except Exception as e:
        db.session.rollback()
        raise Exception("dsfks")
    return user


@blueprint.route('/api/users/login', methods=('POST',))
@jwt_optional
@use_kwargs(user_schema)
@marshal_with(user_schema)
def login_user(username, password, **kwargs):
    user = User.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/api/user', methods=('GET',))
@jwt_required
@marshal_with(user_schema)
def get_current_user():
    user = current_user
    # Not sure about this
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    return current_user

@blueprint.route('/api/users/<id>', methods=('DELETE',))
@jwt_optional
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        raise InvalidUsage.user_not_found()
    session = Session.object_session(user)
    session.delete(user)
    session.commit()
    return '', 200

@blueprint.route('/api/users/<id>', methods=('GET',))
@jwt_optional
@marshal_with(user_schema)
def get_user(id):
    user = User.query.filter_by(id=id).first()
    if not user:
        raise InvalidUsage.user_not_found()
    return user

@blueprint.route('/api/users', methods=('GET',))
@jwt_optional
@use_kwargs({'name': fields.Str()})
@marshal_with(users_schema)
def get_users(name=None, limit=20, offset=0):
    res = User.query
    return res.offset(offset).limit(limit).all()

@blueprint.route('/api/users/<id>', methods=('PUT',))
@jwt_required
@use_kwargs(user_schema)
@marshal_with(user_schema)
def update_user(id,**kwargs):
    user = current_user
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user