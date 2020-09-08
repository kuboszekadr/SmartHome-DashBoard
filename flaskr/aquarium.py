from flask import Blueprint, render_template
from . import pages

# Register page in global variable
pages.append({
    'name': 'Aquarium',
    'icon': 'fas fa-fish'
})

bp = Blueprint('aquarium',
               __name__,
               template_folder='templates',
               static_url_path='static')

@bp.route('/aquarium')
def aquarium():
    return render_template('aquarium.html', pages=pages)
