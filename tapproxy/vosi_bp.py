from .vosi import Vosi

from flask import ( Blueprint, render_template )

bp = Blueprint('vosi', __name__, url_prefix='')

vosi = Vosi(perm_note='VOSKit TAPProxy server', upmsg='TAPProxy is accepting queries', downmsg='TAPProxy is not accepting queries')

@bp.route('/availability')
def availability():
    return render_template('availability.xml', isup=vosi.up, up_since_xml=vosi.up_dt_xml(), notes=vosi.get_notes()), 200, {'Content-Type': 'application/xml'}
