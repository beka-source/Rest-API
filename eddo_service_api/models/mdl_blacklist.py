"""Simple blacklist implementation using database

Using database may not be your prefered solution to handle blacklist in your
final application, but remember that's just a cookiecutter template. Feel free
to dump this code and adapt it for your needs.

For this reason, we don't include advanced tokens management in this
example (view all tokens for a user, revoke from api, etc.)

If we choose to use database to handle blacklist in this example, it's mainly
because it will allow you to run the example without needing to setup anything else
like a redis or a memcached server.

This example is heavily inspired by
https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/database_blacklist/
"""
from sqlalchemy.dialects.postgresql import UUID

from eddo_service_api.extensions import db
import uuid


class TokenBlacklist(db.Model):

    __tablename__ = 'ds_token_black_list'

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("tbl_auth_service_users.id"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "token_id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "user_identity": self.user_id,
            "revoked": self.revoked,
            "expires": self.expires,
        }
