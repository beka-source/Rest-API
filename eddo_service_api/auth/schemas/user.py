from eddo_service_api.models import TblUsers, TblRole, TblTasks
from eddo_service_api.extensions import ma, db


class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TblRole
        sqla_session = db.session
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    role = ma.Nested(RoleSchema, many=False)

    class Meta:
        model = TblUsers
        sqla_session = db.session
        load_instance = True


class TaskSchema(ma.SQLAlchemyAutoSchema):
    from_user_id = ma.auto_field()
    to_user_id = ma.auto_field()
    user1 = ma.Nested(UserSchema, many=False)
    user2 = ma.Nested(UserSchema, many=False)


    class Meta:
        model = TblTasks
        sqla_session = db.session
        load_instance = True

