from jinja2.environment import Environment
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='static/templates')
jinja_env = Environment(extensions=['jinja2.ext.do'])