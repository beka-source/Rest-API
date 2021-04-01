import uuid
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from eddo_service_api.extensions import db, pwd_context
from eddo_service_api.models.mdl_helpers import time_now
from sqlalchemy.orm import backref


class TblUsers(db.Model):

    __tablename__ = 'tbl_auth_service_users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    full_name = db.Column(db.String(255), nullable=False)
    bin = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime(timezone=True), default=time_now)
    update_time = db.Column(db.DateTime(timezone=True), default=time_now, onupdate=time_now)
    role = db.relationship('TblRole', backref='tbl_auth_service_users', uselist=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_role.id'))
    is_resident = db.Column(db.Boolean, nullable=True)
    status = db.Column(db.String, nullable=True)

    @hybrid_property
    def password(self):
        return self._password

    # @hybrid_property
    # def role_id(self):
    #     return self.role_id

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    # @role_id.setter
    # def role_id(self, *args, **kwargs):
    #     role = TblRole.query.filter_by(title='user').first()
    #     self.role_id = role.id

    def __repr__(self):
        return "<Users %s>" % self.username


class TblRole(db.Model):

    __tablename__ = 'tbl_role'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    title = db.Column(db.String(100), unique=False)


# дата, текст задачи, исполнитель, исполняющий, статус, айди
class TblTasks(db.Model):

    __tablename__ = 'tbl_tasks'

    task_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    task_status = db.Column(db.String, nullable=True)
    task_owner = db.Column(db.String(50), nullable=False)
    task_executor = db.Column(db.String(50), nullable=False)
    task_text = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime(timezone=True), default=time_now)
    update_time = db.Column(db.DateTime(timezone=True), default=time_now, onupdate=time_now)

    from_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'),)
    to_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'))

    user1 = db.relationship("TblUsers", foreign_keys=[from_user_id, ])
    user2 = db.relationship("TblUsers", foreign_keys=[to_user_id, ])
