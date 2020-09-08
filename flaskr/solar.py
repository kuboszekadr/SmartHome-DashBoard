from flask import Blueprint, render_template
from . import pages

# Register page in global variable
pages.append({
    'name': 'Solar',
    'icon': 'fas fa-solar-panel'
})

bp = Blueprint('solar',
               __name__,
               template_folder='templates',
               static_url_path='static')

@bp.route('/solar')
def solar():
    return render_template('solar.html', pages=pages)
