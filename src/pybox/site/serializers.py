# coding: utf-8

from marshmallow import Schema, fields, pre_load, post_dump


class SiteSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    createdAt = fields.DateTime(attribute='created_at', dump_only=True)
    updatedAt = fields.DateTime(attribute='updated_at')

    # @pre_load
    # def make_site(self, data, **kwargs):
    #     print(data)
    #     # some of the frontends send this like an empty string and some send
    #     # null
    #     if not data.get('name', True):
    #         del data['name']
    #     return data
    #
    # @post_dump
    # def dump_site(self, data, **kwargs):
    #     return {'site': data}

    class Meta:
        strict = True


site_schema = SiteSchema()
sites_schema = SiteSchema(many=True)