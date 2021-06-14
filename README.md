# flacker

This is a dockerized Alpine Linux uWSGI server running a Flask app with a ready login blueprint module. This is meant to be a quick starting point for small or <strong>BIG</strong> Flask projects from development to production.

# Quick

Simply (after installing Docker naturally) you run:

`docker build -t flacker/latest`

`docker run -ti -p 8080:8080 -v $(pwd)/www:/app/www flacker/latest`

After all the setup is done, surf to `localhost:5000`

## About

The emphasis is on security, modularity and simplicity, both of which will get better as time goes on.

### Security

The docker container and the app itself will be built as secure as possible.

### Modularity

Easy removal and configurability of shipped modules and easily replaceable front end framework.

### Simplicity

Everything will be done in the most simple way without conflicting the previous points.

## Featuring

- [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) - as the web server
- [Blueprints](http://flask.pocoo.org/docs/0.11/blueprints/)- principal modularity
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/) - ORM
- [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - login and logout
- [Flask-WTF](https://flask-wtf.readthedocs.io/en/latest/) - forms
- [Jinja2](http://jinja.pocoo.org/docs/dev/) - templating
