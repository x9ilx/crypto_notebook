from jinja2.environment import Environment
from fastapi.templating import Jinja2Templates

from frontend.jinja_filters import format_float

templates = Jinja2Templates(directory='static/templates')
jinja_env = Environment(extensions=['jinja2.ext.do'])

templates.env.filters['format_float'] = format_float