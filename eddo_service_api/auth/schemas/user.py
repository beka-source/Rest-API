from eddo_service_api.models import TblUsers, TblRole, TblTasks, TaskUserRole, TblComment
from eddo_service_api.extensions import ma, db


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TblRole
        sqla_session = db.session
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    # role_title = ma.Nested(RoleSchema, many=False)
    #id = ma.auto_field()

    class Meta:
        model = TblUsers
        sqla_session = db.session
        load_instance = True


class TaskSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TblTasks
        sqla_session = db.session
        load_instance = True


class TaskUserRoleSchema(ma.SQLAlchemyAutoSchema):
    user_id = ma.auto_field()
    task_id = ma.auto_field()
    role_id = ma.auto_field()

    # role_title = ma.Nested(RoleSchema, many=False)
    task = ma.Nested(TaskSchema, many=False)
    user = ma.Nested(UserSchema, many=False)
    role_title = ma.Nested(RoleSchema, many=False)

    class Meta:
        model = TaskUserRole
        sqla_session = db.session
        load_instance = True


class TblCommentSchema(ma.SQLAlchemyAutoSchema):
    task_id = ma.auto_field()
    user_id = ma.auto_field()

    class Meta:
        model = TblComment
        sqla_session = db.session
        load_instance = True


# class TaskSchema(ma.SQLAlchemyAutoSchema):
#     positions = ma.Nested(PositioinSchema, many=True)
#
#     class Meta:
#         model = TblTasks
#         sqla_session = db.session
#         load_instance = True
#
