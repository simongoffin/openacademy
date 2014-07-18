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
        
        

    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        'start_date' : fields.date(string="Start date"),
        'description' : fields.text(string="Description"),
        'responsible_id' : fields.many2one('res.users',
            ondelete='set null', string='Responsible', select=True),
        'session_ids' : fields.one2many('openacademy.session', 'course_id',
            string='Session'),
        'active' : fields.boolean("Active"),
    }
    
    _sql_constraints = [("name_different_from_description",
        "CHECK (description != name)", "The title and the description must be different"),
        ("name_unique", "unique(name)", "There is already a course with that title")]
        
    _defaults = {
        'active': True,
        'start_date': fields.date.today,
    }
