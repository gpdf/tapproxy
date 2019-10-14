from datetime import datetime

class Vosi:
    """Representation of the standards-conformant information needed to produce VOSI-compliant responses"""

    def __init__(self, up=True, perm_note=None, 
                 upmsg='Service is accepting queries', 
                 downmsg='Service is not accepting queries'):
        self.up_dt_initial = datetime.utcnow()
        self.down_at = None
        self.back_at = None
        self.up = up
        self.up_dt = self.up_dt_initial if up else None
        self.perm_note = perm_note
        self.upmsg = upmsg
        self.downmsg = downmsg
        self.notes = []

    def go_up(self):
        if not self.up: self.up_dt = datetime.utcnow()
        self.up = True

    def go_down(self):
        self.up_dt = None
        self.up = False

    def set_notes(self,new_notes):
        self.notes = new_notes

    def get_notes(self):
        prefix = []
        if self.up and self.upmsg: prefix.append(self.upmsg)
        if ( not self.up ) and self.downmsg: prefix.append(self.downmsg)
        if self.perm_note: prefix.append(self.perm_note)
        return prefix + self.notes

    def up_dt_xml(self):
        return '' if self.up_dt == None else self.up_dt.isoformat() + 'Z'
