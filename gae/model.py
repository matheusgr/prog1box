from google.appengine.api import memcache
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


def _get_default_entity(entity, start_result, process_result, set_namespace, addr):
    result = start_result
    namespace = memcache.get(set_namespace + addr)

    if namespace is not None:
        for network_key in namespace.split(" / "):
            network_result = memcache.get("N" + set_namespace + network_key)
            if network_result is None:
                network_result = ""
                key = ndb.Key(urlsafe=network_key)
                for x in entity.query(entity.network == key):
                    network_result += process_result(x) + '\n'
                memcache.add("N" + set_namespace + network_key, network_result)
            result += network_result
        return result

    namespace = ""
    addr_ = netaddr.IPAddress(addr)

    for network in Network.query().order(Network.addr):
        if addr_ in network.netaddr:
            namespace += network.key.urlsafe() + " / "
            network_result = ""
            for x in entity.query(entity.network == network.key):
                network_result += process_result(x) + '\n'
            result += network_result
            memcache.add("N" + set_namespace + network.key.urlsafe(), network_result)
    if namespace != "":
        memcache.set(set_namespace + addr, namespace[:-3])  # remove final ' / '
    return result


def get_default_files(addr):
    return _get_default_entity(RemoteFile, "", lambda x: '\necho "' + x.content + '" > "' + x.path + '"', RemoteFile.NAMESPACE, addr)


def get_default_script(addr):
    return _get_default_entity(ExecScript, "unset http_proxy\nunset https_proxy\n", lambda x: x.code, ExecScript.NAMESPACE, addr)


def get_user_networks(email, is_admin=False):
    if is_admin:
        return [result for result in Network.query()]
    return [result.network.get() for result in AllowedUser.query(AllowedUser.email == email)]


def invalidate_cache(network_key, entity=None):
    if entity:
        memcache.delete("N" + entity.NAMESPACE + network_key)
    else:
        memcache.delete("N" + ExecScript.NAMESPACE + network_key)
        memcache.delete("N" + RemoteFile.NAMESPACE + network_key)


def flush_cache():
    memcache.flush_all()


class Network(ndb.Model):
    name = ndb.StringProperty(required=True)
    addr = ndb.StringProperty(required=True)

    def __getattr__(self, attr):
        if attr == 'netaddr':
            return netaddr.IPNetwork(self.addr)


class ExecScript(ndb.Model):
    NAMESPACE = "S:"
    code = ndb.TextProperty(required=True)
    name = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)


class RemoteFile(ndb.Model):
    NAMESPACE = "R:"
    content = ndb.TextProperty(required=True)
    path = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)


class AllowedUser(ndb.Model):
    email = ndb.StringProperty(required=True)
    network = ndb.KeyProperty(required=True, kind=Network)
