from flask import Flask

from demo.routes import api


app = Flask(__name__)
app.register_blueprint(api, url_prefix="/api")


if __name__ == "__main__":
    # Local demo server only. Do not expose this application to the network.
    app.run(host="127.0.0.1", port=5000, debug=False)
