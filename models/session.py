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
        
    def onchange_taken_seats(self, cr, uid, ids, attendee_ids, seats, context=None): 
        attendee_records = self.resolve_2many_commands(cr, uid, 'attendee_ids',attendee_ids, ['id'])
        res = { 'value': { 'taken_seats': self._compute_taken_seats(attendee_records,seats), }, }
        if seats < 0:
            res['warning'] = {
                'title': "Warning: bad value",
                'message' : "You cannot have negative number of seats",
            }
        elif seats < len(attendee_records):
            res['warning'] = {
                'title': "Warning: problems",
                'message' : "You need more seats for this session",
            }
        return res
        
    def _check_instructor_is_not_attendee(self, cr, uid, ids):
        for session in self.browse(cr, uid, ids):
          if session.instructor_id:
            for attendee in session.attendee_ids:
              if session.instructor_id == attendee.partner_id:
                return False
        return True
        
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
    
    _constraints = [(_check_instructor_is_not_attendee,
    "The instructor cannot attend his own course!",
     ['instructor_id', 'attendee_ids'])]