from flask import Flask, url_for, render_template, request, redirect, session
from sqlalchemy import Column, String, Integer, create_engine, Enum, VARCHAR
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
import enum
from enum import Enum


import json

db = SQLAlchemy()

database_name = "jobtracker"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = "postgres://xmrppvwylzgypk:6f1365264f57757e7a066384a7f9726989f9405ce51f0338c2cb41fd9ba66d93" \
                          "@ec2-52-2-82-109.compute-1.amazonaws.com:5432/dff49pg3f10oi2 "

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


# def db_setup(app, database_path=database_path):
#     app.config["SQLALCHEMY_DATABASE_URI"] = database_path
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     app.secret_key = 'super secret key'
#     app.config['SESSION_TYPE'] = 'filesystem'
#     db.app = app
#     db.init_app(app)
#     db.create_all()


# TODO: connect to a local postgresql database
def db_setup(app,  database_path=SQLALCHEMY_DATABASE_URI ):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class User(UserMixin, db.Model):
    """ Create user table"""
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    job = db.relationship('Job', backref="User", lazy=True)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
        }


class JobStatus(enum.Enum):
    applied = 'Applied'
    rejected = 'Rejected'
    no_response = 'No response'
    interview = 'interview'
    accepted = 'Accepted'
    pending = 'Wishlist'


class Job(db.Model):
    __tablename__ = 'Job'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.VARCHAR(240))
    url = db.Column(db.String)
    company = db.Column(db.String)
    position = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    job_status = db.Column(db.Enum(JobStatus), nullable=False)

    def __init__(self, description, url, company, position, user_id, job_status):
        self.description = description
        self.url = url
        self.company = company
        self.position = position
        self.user_id = user_id
        self.job_status = job_status

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'url': self.url,
            'company': self.company,
            'position': self.position,
            'user_id': self.user_id,
            'job_status': self.job_status
        }


