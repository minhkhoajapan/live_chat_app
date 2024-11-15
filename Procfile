web: daphne backend.backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=backend.backend.settings -v2