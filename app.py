"""routing file for msgapp app"""

from flask import Flask

from msgapp import views
from msgapp.models.user import db
from settings import FLASK_CONFIG, SQLALCHEMY_DATABASE_URI


#configuration
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config.update(FLASK_CONFIG)


#setup DB
db.app = app
db.init_app(app)
def init_db():
    db.create_all()
    db.session.commit()
init_db()
#db = SQLAlchemy(app)

#URL rules
app.add_url_rule(
    '/', view_func=views.index, methods=['GET', 'POST'])
app.add_url_rule(
    '/reminder', view_func=views.reminder, methods=['GET', 'POST'])
app.add_url_rule(
    '/reminder/info', view_func=views.info, methods=['GET', 'POST'])


if __name__ == '__main__':
    app.run()