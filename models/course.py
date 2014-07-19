# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class Course(osv.Model):
    _name = "openacademy.course"
    
    def copy(self, cr, uid, id, defaults, context=None):
        course = self.browse(cr, uid, id)
        new_name = "Copy of " + course.name
        other_name = self.search(cr, uid, [('name', '=like', course.name)],
        count=True, context=context)
        if other_name > 0:
            new_name += " (" + str(other_name) + ")"
        defaults['name'] = new_name
        return super(Course, self).copy(cr, uid, id, defaults, context)
        
    def _get_attendee_count(self, cr, uid, ids, name, args, context=None):
        res = {}
        for course in self.browse(cr, uid, ids, context=context):
            res[course.id] = 0
            for session in course.session_ids:
                res[course.id] += len(session.attendee_ids)
        return res

    # /!\ This method is called from the session object!!
    def _get_courses_from_sessions(self, cr, uid, ids, context=None):
        sessions = self.browse(cr, uid, ids, context=context)
        # Return a list of Course ids with only one occurrence of each
        return list(set(sess.course_id.id for sess in sessions))
        
        

    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        'start_date' : fields.date(string="Start date"),
        'description' : fields.text(string="Description"),
        'active' : fields.boolean("Active"),
        #Relational
        'responsible_id' : fields.many2one('res.users',
            ondelete='set null', string='Responsible', select=True),
        'session_ids' : fields.one2many('openacademy.session', 'course_id',
            string='Session'),
        #Fonctional
        'attendee_count_course': fields.function(_get_attendee_count,type='integer',
            string='Attendee Count', store={
            'openacademy.session' :
            (_get_courses_from_sessions,['attendee_ids'],0)}),
    }
    
    _sql_constraints = [("name_different_from_description",
        "CHECK (description != name)", "The title and the description must be different"),
        ("name_unique", "unique(name)", "There is already a course with that title")]
        
    _defaults = {
        'active': True,
        'start_date': fields.date.today,
    }
