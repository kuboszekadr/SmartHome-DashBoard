from flask import Blueprint, render_template
from . import pages

# Register page in global variable
pages.append({
    'name': 'Aquarium',
    'icon': 'fas fa-fish'
})

bp = Blueprint('aquarium',
               __name__,
               template_folder='templates/aquarium',
               url_prefix='/aquarium',
               static_folder='templates/aquarium/static')

@bp.route('/')
@bp.route('/overview')
def aquarium():
    return render_template('overview.html', pages=pages)

@bp.route('/time_series')
def time_series():
    return render_template('time_series.html', pages=pages)    

@bp.route('/config')
def config():
    return render_template('config.html', pages=pages)    