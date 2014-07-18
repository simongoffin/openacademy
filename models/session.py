# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Session(osv.Model):

    _name = "openacademy.session"
    
    def _compute_taken_seats(self, attendees, seats):
        try:
            return (1.0 * len(attendees) / seats) * 100
        except ZeroDivisionError:
            return 0.0

    def _get_taken_seats(self, cr, uid, ids, name, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            result[session.id] = self._compute_taken_seats(session.attendee_ids,session.seats)
        return result
        
    _columns = {
        'name' : fields.char(string="Name", size=256, required=True),
        'start_date' : fields.date(string="Start date"),
        'duration' : fields.float(string="Duration", digits=(6,2),help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),
        #Relational
        'instructor_id' : fields.many2one('res.partner', string="Instructor",domain=[('instructor','=',True)]),
        'course_id' : fields.many2one('openacademy.course',ondelete='cascade', string="Course", required=True),
        'attendee_ids' : fields.one2many('openacademy.attendee', 'session_id',string="Attendees"),
        #Fonctionnal
        'taken_seats_percent' : fields.function(_get_taken_seats,type='float', string='Taken Seats'),
    }