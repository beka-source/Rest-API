FLASK_ENV=development
FLASK_APP=eddo_service_api.app:create_app
SECRET_KEY=changeme
DATABASE_URI=postgres://postgres:rbj13@localhost:5432/server8
CELERY_BROKER_URL=amqp://guest:guest@localhost/
CELERY_RESULT_BACKEND_URL=rpc://
