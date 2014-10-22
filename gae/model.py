#coding: utf-8
from google.appengine.ext import db


class ExecScript(db.Model):
    code = db.TextProperty(required=True)
    name = db.StringProperty(required=True)


class AllowedUser(db.Model):
    email = db.StringProperty(required=True)
