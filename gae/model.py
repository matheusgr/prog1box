#coding: utf-8
from google.appengine.ext import ndb


def get_default_script(addr):
    return ExecScript.query(ExecScript.name == 'default').get().code


def get_user_networks(email):
    return [result.network.get() for result in AllowedUser.query(AllowedUser.email == email)]


class ExecScript(ndb.Model):
    code = ndb.TextProperty(required=True)
    name = ndb.StringProperty(required=True)


class Network(ndb.Model):
    name = ndb.StringProperty(required=True)
    addr = ndb.StringProperty(required=True)


class AllowedUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)