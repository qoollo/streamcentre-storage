# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from storageapp.app import app, init_app
from storageapp.database import init_db

init_app()
manager = Manager(app)

@manager.command
def initdb():
    """
    Drop and create database
    
    """
    
    init_db()


if __name__ == "__main__":
    manager.run()
