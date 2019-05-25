from flask import Flask
from gevent.pywsgi import WSGIServer
from healthcheck import HealthCheck, EnvironmentDump

app = Flask(__name__)

health = HealthCheck()

app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health.run())

http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()