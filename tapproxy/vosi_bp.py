from .vosiproxy import VosiProxy

from flask import ( Blueprint, render_template, current_app )

bp = Blueprint('vosi', __name__, url_prefix='')

vosi = None

def init_app(app):
    global vosi
    tapurl = app.config['TAP_URL']
    vosi = VosiProxy( url=tapurl,
        perm_note='VOSKit TAPProxy server for ' + tapurl,
        upmsg='TAPProxy is accepting queries', 
        downmsg='TAPProxy is not accepting queries')

@bp.route('/availability')
def availability():
    vosi.update_availability()
    return render_template(
        'availability.xml', isup=vosi.up,
        up_since_xml=vosi.up_dt_xml(),
        notes=vosi.get_notes()), \
        200, {'Content-Type': 'application/xml'}
