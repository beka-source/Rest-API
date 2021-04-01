import uuid
import enum
from eddo_service_api.extensions import db
from sqlalchemy.dialects.postgresql import UUID, ENUM
from eddo_service_api.models.mdl_helpers import time_now


class SendTypeEnum(enum.Enum):
    send_type1 = "register"
    send_type2 = "forget"
    send_type3 = "other"


send_type_enum = ENUM(SendTypeEnum, name="send_type_enum")


class TblVerifyCode(db.Model):

    __tablename__ = 'tbl_auth_service_verify_code'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    mobile = db.Column(db.String(10), nullable=False)
    code = db.Column(db.String, nullable=False)  # Было integer
    sum_ = db.Column(db.Integer, default=1)
    # send_type = db.Column(send_type_enum)
    create_time = db.Column(db.DateTime(timezone=True, ), default=time_now)

    def repr(self):
        return "<verify_code %s>" % self.id