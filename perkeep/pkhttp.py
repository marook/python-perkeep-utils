import json
import os
import platform
import ssl
import urllib.request

def urlopen(path, data=None, content_type=None):
    server_config = get_default_server_config()
    request = urllib.request.Request(server_config['server'] + path, data=data)
    if(not content_type is None):
        request.add_header('Content-Type', content_type)
    return get_default_perkeep_opener().open(request)

perkeep_opener = None

def get_default_perkeep_opener():
    global perkeep_opener
    if(perkeep_opener is None):
        server_config = get_default_server_config()
        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE
        https_handler = urllib.request.HTTPSHandler(debuglevel=0, check_hostname=False, context=ssl_ctx)
        auth_method, user, password = server_config['auth'].split(':')
        if(auth_method != 'userpass'):
            raise Exception('Unknown auth_method {}'.format(auth_method))
        auth_handler = urllib.request.HTTPBasicAuthHandler()
        auth_handler.add_password(
            realm='',
            uri=server_config['server'],
            user=user,
            passwd=password)
        perkeep_opener = urllib.request.build_opener(https_handler)
        perkeep_opener.add_handler(auth_handler)
    return perkeep_opener

def get_default_server_config():
    config = get_client_config()
    for server in config['servers'].values():
        if(not server['default']):
            continue
        return server
    raise Exception('No default server found')

client_config_cache = None

def get_client_config():
    global client_config_cache
    if(client_config_cache is None):
        client_config_cache = read_client_config()
    return client_config_cache

def read_client_config():
    config_dir = get_perkeep_config_dir_path()
    with open(os.path.join(config_dir, 'client-config.json'), 'r') as f:
        return json.load(f)

def get_perkeep_config_dir_path():
    if('CAMLI_CONFIG_DIR' in os.environ):
        return os.environ['CAMLI_CONFIG_DIR']
    if(platform.system() == 'Windows'):
        return os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Camlistore')
    return os.path.join(os.path.expanduser('~'), '.config', 'camlistore')
