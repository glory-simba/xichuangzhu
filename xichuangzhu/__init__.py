#-*- coding: UTF-8 -*-
import sys

sys.path.append('/var/www/flaskconfig/xichuangzhu')
import config
from flask import Flask, request, url_for, session, g, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

# convert python's encoding to utf8
reload(sys)
sys.setdefaultencoding('utf8')

# app
app = Flask(__name__)
app.config.from_object(config)

# Debug toolbar
if app.debug:
    toolbar = DebugToolbarExtension(app)

# SQLAlchemy
db = SQLAlchemy(app)

# inject vars into template context
@app.context_processor
def inject_vars():
    return dict(
        douban_login_url=config.DOUBAN_LOGIN_URL,
        admin_id=config.ADMIN_ID,
    )


# url generator for pagination
def url_for_other_page(page):
    view_args = request.view_args.copy()
    args = request.args.copy().to_dict()
    args['page'] = page
    view_args.update(args)
    return url_for(request.endpoint, **view_args)


app.jinja_env.globals['url_for_other_page'] = url_for_other_page


# before every request
@app.before_request
def before_request():
    g.user_id = session['user_id'] if 'user_id' in session else None


def register_logger(app):
    """Send error log to admin by smtp"""
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        credentials = (config.SMTP_USER, config.SMTP_PASSWORD)
        mail_handler = SMTPHandler((config.SMTP_SERVER, config.SMTP_PORT), config.SMTP_FROM, config.SMTP_ADMIN, 'xcz-log',
                                   credentials)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

import models


def register_routes(app):
    from .controllers import account, admin, author, dynasty, topic, site, user, work

    app.register_blueprint(site.bp, url_prefix='')
    app.register_blueprint(account.bp, url_prefix='/account')
    app.register_blueprint(admin.bp, url_prefix='/admin')
    app.register_blueprint(topic.bp, url_prefix='/topic')
    app.register_blueprint(dynasty.bp, url_prefix='/dynasty')
    app.register_blueprint(author.bp, url_prefix='/author')
    app.register_blueprint(work.bp, url_prefix='/work')
    app.register_blueprint(user.bp, url_prefix='/user')


def register_error_handle(app):
    @app.errorhandler(403)
    def page_403(error):
        return render_template('site/403.html'), 403

    @app.errorhandler(404)
    def page_404(error):
        return render_template('site/404.html'), 404

    @app.errorhandler(500)
    def page_500(error):
        return render_template('site/500.html'), 500


register_routes(app)
register_error_handle(app)
register_logger(app)

