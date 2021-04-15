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
    #role_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    full_name = db.Column(db.String(255), nullable=False)
    iin = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    _password = db.Column("password", db.String(255), nullable=False)
    create_time = db.Column(db.DateTime(timezone=True), default=time_now)
    update_time = db.Column(db.DateTime(timezone=True), default=time_now, onupdate=time_now)
    is_resident = db.Column(db.Boolean, nullable=True)

    # role = db.relationship('TblRole', backref='tbl_auth_service_users', uselist=False)
    # role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_role.id'))
    # status = db.Column(db.String, nullable=True)

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

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    task_status = db.Column(db.String, nullable=False, default='New')
    task_text = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime(timezone=True), default=time_now)
    update_time = db.Column(db.DateTime(timezone=True), default=time_now, onupdate=time_now)
    deadline = db.Column(db.Date, index=True)
    positions = db.relationship('TblPosition', backref='tbl_tasks', uselist=True)

    # from_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'))
    # to_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'))

    # user1 = db.relationship("TblUsers", foreign_keys=[from_user_id, ])
    # user2 = db.relationship("TblUsers", foreign_keys=[to_user_id, ])


class TaskUserRole(db.Model):
    tablename = 'tbl_task_user_role'

    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_tasks.id'), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'), primary_key=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_role.id'), primary_key=True)
    task = db.relationship('TblTasks', backref=backref("tbl_position", cascade="all, delete-orphan"))
    user = db.relationship('TblUsers', backref='tbl_position', uselist=False)
    role_title = db.relationship('TblRole', backref='tbl_position', uselist=False)


class TblComment(db.Model):

    tablename = 'tbl_comment'

    comment_id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4())
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'))
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_tasks.id'))
    comment = db.Column(db.String(255), nullable=False)
    reply_to = db.Column(UUID(as_uuid=True), nullable=True)
    create_time = db.Column(db.DateTime(timezone=True), default=time_now)
    update_time = db.Column(db.DateTime(timezone=True), default=time_now, onupdate=time_now)


class TblRek(db.Model):

    __tablename__ = 'tbl_rek'

    rek_id = db.column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4())
    module_id = db.column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4())
    title = db.Column(db.String(100), unique=False)
    category = db.Column(db.String(150), unique=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_auth_service_users.id'))
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tbl_tasks.id'))
