# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request,jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, jwt_optional, create_access_token, current_user
from sqlalchemy.exc import IntegrityError
from marshmallow import fields

from pybox.database import db
from pybox.exceptions import InvalidUsage
from pybox.profile.models import UserProfile
from .models import Site
from .serializers import site_schema,sites_schema

blueprint = Blueprint('site', __name__)

@blueprint.route('/api/sites', methods=('GET',))
@jwt_optional
@use_kwargs({'name': fields.Str()})
@marshal_with(sites_schema)
def get_sites(name=None, limit=20, offset=0):
    res = Site.query
    return res.offset(offset).limit(limit).all()


@blueprint.route('/api/sites', methods=('POST',))
@jwt_optional
@use_kwargs(site_schema)
@marshal_with(site_schema)
def make_site(body, title, description, tagList=None):
    site = site(title=title, description=description, body=body,
                      author=current_user.profile)
    if tagList is not None:
        for tag in tagList:
            mtag = Tags.query.filter_by(tagname=tag).first()
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            site.add_tag(mtag)
    site.save()
    return site


@blueprint.route('/api/sites/<id>', methods=('PUT',))
@jwt_optional
@use_kwargs(site_schema)
@marshal_with(site_schema)
def update_site(id, **kwargs):
    site = Site.query.filter_by(id=id, author_id=current_user.profile.id).first()
    if not site:
        raise InvalidUsage.site_not_found()
    site.update(updatedAt=dt.datetime.utcnow(), **kwargs)
    site.save()
    return site


@blueprint.route('/api/sites/<id>', methods=('DELETE',))
@jwt_optional
def delete_site(id):
    site = Site.query.filter_by(id=id, author_id=current_user.profile.id).first()
    site.delete()
    return '', 200


@blueprint.route('/api/sites/<id>', methods=('GET',))
@jwt_optional
@marshal_with(site_schema)
def get_site(id):
    site = Site.query.filter_by(id=id).first()
    if not site:
        raise InvalidUsage.site_not_found()
    return site
