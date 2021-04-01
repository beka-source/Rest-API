from eddo_service_api.models import TblUsers, TblRole


from eddo_service_api.extensions import db
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def roles_required(role):
    def _role(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user_id = get_jwt_identity()
            print(current_user_id)
            if not current_user_id:
                return {'error': 'no token'}
            user = db.session.query(TblUsers).filter(TblUsers.id == current_user_id).first()
            print(user)
            if not user.role_id:
                return {'msg': 'role id is null'}
            user_role = TblRole.query.get_or_404(user.role_id)
            if user_role.title == role:
                return func(*args, **kwargs)
            else:
                return {"Permission": "access denied"}
        return wrapper
    return _role