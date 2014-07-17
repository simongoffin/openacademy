# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Session(osv.Model):
    _name = "openacademy.session"
    _columns = {
        'name' : fields.char(string="Name", size=256, required=True),
        'start_date' : fields.date(string="Start date"),
        'duration' : fields.float(string="Duration", digits=(6,2),help="Duration in days"),
        'seats' : fields.integer(string="Number of seats"),
        'instructor_id' : fields.many2one('res.partner', string="Instructor"),
        'course_id' : fields.many2one('openacademy.course',
            ondelete=’cascade’, string="Course", required=True),
        'attendee_ids' : fields.one2many('openacademy.attendee', 'session_id',
            string="Attendees"),
    }