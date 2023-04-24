import waitress
from app import app
from app.tasks import delete_all_data_in_db_and_fs

# Раскоментируй эту строчку, если хочешь очистить базу данных при запуске сервера (тестовый режим).
# delete_all_data_in_db_and_fs.delay()

port = app.config.get('FLASK_PORT')

if app.config.get('DEBUG'):
    app.run(host='0.0.0.0', port=port)
else:
    waitress.serve(app, host='0.0.0.0', port=port)
