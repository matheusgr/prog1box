from google.appengine.ext import ndb

import netaddr


def _get_entities(entity, networks):
    result = {}
    for network in networks:
        result[network.key] = [x for x in entity.query(entity.network == network.key)]
    return result


def get_exec_scripts(networks):
    return _get_entities(ExecScript, networks)


def get_remote_files(networks):
    return _get_entities(RemoteFile, networks)


def get_default_files(addr):  # TODO cache
    addr_ = netaddr.IPAddress(addr)
    result = ""
    for network in Network.query():
        if addr_ in network.netaddr:
            for remotefile in RemoteFile.query(RemoteFile.network == network.key):
                result += '\necho "'
                result += remotefile.content
                result += '" >> "' + remotefile.path + '"'
    return result


def get_default_script(addr):  # TODO cache
    addr_ = netaddr.IPAddress(addr)
    result = "unset http_proxy\nunset https_proxy\n"  # unset proxies for root
    for network in Network.query():
        if addr_ in network.netaddr:
            result += '\n'.join([x.code for x in ExecScript.query(ExecScript.network == network.key)])
    return result


def get_user_networks(email, is_admin=False):
    if is_admin:
        return [result for result in Network.query()]
    return [result.network.get() for result in AllowedUser.query(AllowedUser.email == email)]


class Network(ndb.Model):
    name = ndb.StringProperty(required=True)
    addr = ndb.StringProperty(required=True)

    def __getattr__(self, attr):
        if attr == 'netaddr':
            return netaddr.IPNetwork(self.addr)


class ExecScript(ndb.Model):
    code = ndb.TextProperty(required=True)
    name = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)


class RemoteFile(ndb.Model):
    content = ndb.TextProperty(required=True)
    path = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)


class AllowedUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)
