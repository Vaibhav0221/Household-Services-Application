import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{os.path.join(basedir, '../db_directory/sql.db')}"

