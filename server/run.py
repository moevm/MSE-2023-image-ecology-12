import waitress

from app import app
port = app.config.get('FLASK_PORT')

if app.config.get('DEBUG'):
    app.run(host='0.0.0.0', port=port)

else:
    waitress.serve(app, host='0.0.0.0', port=port)