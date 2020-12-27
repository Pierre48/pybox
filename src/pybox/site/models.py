# -*- coding: utf-8 -*-
"""Site models."""
import datetime as dt

from pybox.database import Column, Model, SurrogatePK, db
from pybox.extensions import bcrypt


class Site(SurrogatePK, Model):

    __tablename__ = 'sites'
    name = Column(db.String(80), unique=True, nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    token: str = ''

    def __init__(self, name, **kwargs):
        """Create instance."""
        db.Model.__init__(self, name=name,  **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Site({name!r})>'.format(name=self.name)