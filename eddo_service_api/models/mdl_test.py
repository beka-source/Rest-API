from eddo_service_api.extensions import db


class Parent(db.Model):
    __tablename__ = 'parent'

    id = db.Column(db.Integer, primary_key=True)
    children = db.relationship('Child')


class Child(db.Model):
    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'))
    name = db.Column(db.String, nullable=True)
