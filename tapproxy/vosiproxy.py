from .vosi import Vosi

from pyvo.dal import TAPService

class VosiProxy(Vosi):
    def __init__(self, url, **kwargs):
        super().__init__(**kwargs)

        self.url = url

    def update_availability(self):
        tap = TAPService(self.url)
        print( 'TAP availability: ' + ( 'true' if tap.available else 'false') )
        tap_avail = tap.availability
        if tap_avail.available:
            super().go_up()
        else:
            super().go_down()

        tap_notes = [ 'Remote TAP service note: ' + n for n in tap_avail.notes ]
        super().set_notes(tap_notes)
