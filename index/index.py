import os

from docker import Client

from bottle import route, run, template

hostname = os.environ["HOSTNAME"]

client = Client(base_url="unix:///var/run/docker.sock")

T = """

<html>
  <body>
    % if not streams:
    <h1>No streams are active.</h1>
    % else:
    <h1>Current Streams:</h1>
    <ul>
      % for stream in streams:
      <li>
        <a href="{{stream.url}}">{{stream.port}}</a>
        <span>{{stream.advert}}</span>
      </li>
      % end
    </ul>
    % end
  </body>
</html>
"""

class Stream(object):
    def __init__(self, port, advert):
        self.port = port
        self.advert = advert
        self.url = "http://{}:{}/".format(hostname, port)

def get_containers():
    containers = client.containers(filters=dict(status='running'))
    return filter(lambda c: 'dlacewell/ttycast' in c["Image"], containers)

def get_env(info, name, default=None):
    config = info.get("Config")
    if not config: return default
    env = config.get("Env")
    if not env: return default
    for var in env:
        key, val = var.split("=")
        if key == name:
            return val
    return default

def get_streams():
    containers = get_containers()
    for c in containers:
        info = client.inspect_container(c["Id"])
        port = get_env(info, "PORT", "BLANK")
        advert = get_env(info, "ADVERT", "BLANK")
        yield Stream(port, advert)

@route('/')
def index():
    streams = get_streams()
    return template(T, streams=streams)

run(host='0.0.0.0', port=9000)
