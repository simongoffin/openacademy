# -*- coding: utf-8 -*-
from openerp.osv import osv, fields
from datetime import datetime, timedelta

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
        
    def _determine_end_date(self, cr, uid, ids, field, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.start_date and session.duration:
                start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
                duration = timedelta( days=(session.duration - 1) )
                end_date = start_date + duration
                result[session.id] = end_date.strftime("%Y-%m-%d")
            else:
                result[session.id] = session.start_date
        return result
        
    def _write_end_date(self, cr, uid, ids, field, value, arg, context=None):
        session = self.browse(cr, uid, ids, context=context)
        if session.start_date and value:
            start_date = datetime.strptime(session.start_date, "%Y-%m-%d")
            end_date = datetime.strptime(value[:10], "%Y-%m-%d")
            duration = end_date - start_date
            self.write(cr, uid, ids, {'duration' : (duration.days + 1)}, context=context)
            
    def _determine_hours_from_duration(self, cr, uid, ids, field, arg, context=None):
        result = {}
        for session in self.browse(cr, uid, ids, context=context):
            if session.duration:
                result[session.id] = session.duration * 24
            else:
                result[session.id] = 0
        return result

    def _set_hours(self, cr, uid, ids, field, value, arg, context=None):
        if value:
            self.write(cr, uid, ids, {'duration' : (value / 24)}, context=context)
            
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for session in self.browse(cr, uid, ids, context=context):
            res[session.id] = len(session.attendee_ids)
        return res

    
    _columns = {
        'name' : fields.char(string="Name", size=256, required=True),
        'start_date' : fields.date(string="Start date"),
        'duration' : fields.float(string="Duration", digits=(6,2),help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),
        'end_date': fields.function(_determine_end_date, string="End date",type='date', fnct_inv=_write_end_date),
        #Relational
        'instructor_id' : fields.many2one('res.partner', string="Instructor",domain=[('instructor','=',True)]),
        'course_id' : fields.many2one('openacademy.course',ondelete='cascade', string="Course", required=True),
        'attendee_ids' : fields.one2many('openacademy.attendee', 'session_id',string="Attendees"),
        #Fonctionnal
        'taken_seats_percent' : fields.function(_get_taken_seats,type='float', string='Taken Seats'),
        'hours' : fields.function(_determine_hours_from_duration, fnct_inv=_set_hours, type='float', string="Hours"),
        'attendee_count': fields.function(_get_attendee_count,type='integer', string='Attendee Count', store=True),
    }
    
    _constraints = [(_check_instructor_is_not_attendee,
    "The instructor cannot attend his own course!",
     ['instructor_id', 'attendee_ids'])]