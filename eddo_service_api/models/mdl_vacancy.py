import uuid
from sqlalchemy.dialects.postgresql import UUID
from eddo_service_api.extensions import db


class TblVacancy(db.Model):
    """ Vacancy model """

    __tablename__ = 'tbl_vacancies'

    vacancy_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organizations_id = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    vacancy_title = db.Column(db.String(80), nullable=True)
    request_count = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.Date, unique=False, nullable=False)
    vacancy_info = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'Vacancy title: {self.vacancy_title}'
