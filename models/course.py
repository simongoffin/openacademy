# -*- coding: utf-8 -*-
from openerp.osv import osv, fields


class Course(osv.Model):
    _name = "openacademy.course"
    _columns = {
        'name' : fields.char(string="Title", size=256, required=True),
        'description' : fields.text(string="Description"),
        'responsible_id' : fields.many2one('res.users',
            ondelete='set null', string='Responsible', select=True),
    }
    
    