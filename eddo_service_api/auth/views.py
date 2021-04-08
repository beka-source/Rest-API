import dateutil
from eddo_service_api.auth.resources import (
    UserResource,
    RoleResource,
    TaskResource,
    PositionResource)
import pytz
from flask import request, jsonify, Blueprint, current_app as app
from flask_restful import Api
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from eddo_service_api.models.mdl_helpers import time_now
from datetime import datetime, timedelta
from eddo_service_api.auth.utils.sms import sen_mobile
from eddo_service_api.models import TblUsers
from eddo_service_api.models.mdl_verify_code import TblVerifyCode
from eddo_service_api.extensions import pwd_context, jwt, apispec
from eddo_service_api.auth.helpers import revoke_token, is_token_revoked, add_token_to_database
from eddo_service_api.extensions import db
from eddo_service_api.auth.language import (
    UESR_NOT_FIND,
    REQUIRED_MOBILE_AND_SEND_TYPE,
    NOT_JSON,
    BLOCK_PHONE_NUMBER,
    SUCCESSFUL_SMS,
    FAILED_SEND_SMS,
    REQUIRED_MOBILE_AND_PASSWORD,
    LOGIN_FAILED,
    VERIFICATION_CODE_ERROR,
    VERIFICATION_CODE_EXPIRED,
    REQUIRED_VERIFICATION_CODE,
    REQUIRED_FORM_DATA,
    USER_IS_REGISTRED,
    CREATE_NEW_USER,
    PASSWORD_NOT_SAME,
    PASSWORD_UPDATE
)


blueprint = Blueprint("auth", __name__, url_prefix="/auth")
auth = Api(blueprint)
auth.add_resource(UserResource, "/users", endpoint="user_by_id")
auth.add_resource(RoleResource, "/roles", endpoint="role_by_id")
auth.add_resource(TaskResource, "/tasks", endpoint="task_by_id")
auth.add_resource(PositionResource, "/posit", endpoint="position_by_id")


@blueprint.route("/sms", methods=["POST"])
def send_sms():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    mobile = request.json.get("mobile", None)
    send_type = request.json.get("send_type", None)

    if not mobile or not send_type:
        return jsonify(REQUIRED_MOBILE_AND_SEND_TYPE), 400

    user = TblUsers.query.filter_by(mobile=mobile).first()

    if send_type == 'send_type1':
        if user is not None:
            return jsonify(UESR_NOT_FIND), 400
    elif send_type == 'send_type2':
        if user is None:
            return jsonify(UESR_NOT_FIND), 400
    else:
        return jsonify(UESR_NOT_FIND), 400

    verify_code = TblVerifyCode.query.filter_by(mobile=mobile, send_type=send_type).order_by(
        TblVerifyCode.id.desc()).first()
    if verify_code:
        if verify_code.sum_ > 3:
            return jsonify(BLOCK_PHONE_NUMBER), 400

    send_status = sen_mobile(mobile=mobile, send_type=send_type)
    if send_status:
        ret = {
            "mobile": mobile,
            "send_type": send_type,
            "msg": SUCCESSFUL_SMS
        }
        return jsonify(ret), 200
    else:
        return jsonify(FAILED_SEND_SMS), 400


@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    username = request.json.get("iin", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify(REQUIRED_MOBILE_AND_PASSWORD), 400
    user = TblUsers.query.filter_by(iin=username).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify(LOGIN_FAILED), 400
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    return jsonify(ret), 200


@blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    full_name = request.json.get("full_name", None)
    mobile = request.json.get("mobile", None)
    iin = request.json.get("iin", None)
    username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    is_resident = request.json.get("is_resident")

    # org_id = request.json.get("org_id", None)

    mobile = (mobile[::-1][0:10])[::-1]

    user = TblUsers.query.filter(
        (TblUsers.username == username) | (TblUsers.email == email)).first()
    if user:
        return jsonify(USER_IS_REGISTRED), 400

    obj_user = TblUsers(
        full_name=full_name,
        username=username,
        email=email,
        mobile=mobile,
        iin=iin,
        is_resident=is_resident,
    )

    obj_user.password = password
    db.session.add(obj_user)
    db.session.commit()
    ret = {
        "status": "success",
        "mobile": mobile,
        "msg": CREATE_NEW_USER,
    }
    return jsonify(ret), 201


@blueprint.route("/reset-password", methods=["POST"])
def reset_password():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    mobile = request.json.get("mobile", None)
    code = request.json.get("code", None)
    password1 = request.json.get("password1", None)
    password2 = request.json.get("password2", None)

    if not mobile or not password1 or not password2 or not code:
        return jsonify(REQUIRED_MOBILE_AND_PASSWORD), 400

    user = TblUsers.query.filter_by(mobile=mobile).first()
    if user is None:
        return jsonify(UESR_NOT_FIND), 400

    if password1 != password2:
        return jsonify(PASSWORD_NOT_SAME), 400

    if code is not None:
        verify_records = TblVerifyCode.query.filter(
            (TblVerifyCode.mobile == mobile) & (TblVerifyCode.code == code) & (TblVerifyCode.send_type == "send_type2")
        ).order_by(TblVerifyCode.create_time.desc()).first()

        if verify_records is None:
            return jsonify(VERIFICATION_CODE_ERROR), 400
        else:
            five_minutes_ago = time_now() - timedelta(hours=1, minutes=3, seconds=0)
            if five_minutes_ago > verify_records.create_time.replace(tzinfo=pytz.timezone('Etc/GMT-6')):
                return jsonify(VERIFICATION_CODE_EXPIRED), 400
    else:
        return jsonify(REQUIRED_VERIFICATION_CODE), 400

    obj_user = TblUsers.query.filter_by(mobile=mobile).first()
    obj_user.password = password1
    db.session.commit()

    ret = {
        "status": "success",
        "mobile": mobile,
        "msg": PASSWORD_UPDATE
    }
    return jsonify(ret), 200


@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return TblUsers.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=send_sms, app=app)
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=reset_password, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
