from app.app import app
port = app.config.get('FLASK_PORT')
app.run(host='0.0.0.0', port=port)
