from flask import Blueprint, render_template
from . import pages

# Register page in global variable
pages.append({
    'name': 'Home',
    'icon': 'fas fa-home'
})

bp = Blueprint('index',
               __name__,
               template_folder='templates',
               static_url_path='static')

@bp.route('/')
def index():
    return render_template('index.html', pages=pages)
