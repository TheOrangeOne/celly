import datetime
from jinja2 import Environment, PackageLoader

env = Environment(
    loader=PackageLoader('celly', 'pages'),
)
env.globals['now'] = datetime.datetime.utcnow
