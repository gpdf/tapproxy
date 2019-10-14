# Main program (application factory) for TAPProxy
import os
from urllib.parse import urlparse
from flask import Flask

def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.jinja_env.line_statement_prefix = '#'

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev"
        # store the database in the instance folder
        # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

        # allow override of the target
        app.config.update(
            TAP_URL=os.environ.get('TAPPROXY_TARGET_URL') )
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # leave the "hello world" endpoint in for now
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # perform basic validation on the target URL
    url = app.config['TAP_URL']
    if url == None:
        raise ValueError('Missing target URL')

    o = urlparse( url )
    urlok = ( o.scheme == 'http' or o.scheme == 'https' ) and \
        o.netloc != '' and o.params == '' and o.query == '' and o.fragment == ''
    if not urlok:
        raise ValueError('Invalid target URL: ' + url )


    # apply the blueprints to the app
    from tapproxy import vosi_bp # , scap, tapwrap

    vosi_bp.init_app(app)

    app.register_blueprint(vosi_bp.bp)
    # app.register_blueprint(scap.bp)
    # app.register_blueprint(tapwrap.bp)

    return app
