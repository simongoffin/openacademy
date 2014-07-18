# -*- coding: utf-8 -*-
from openerp.osv import osv, fields

class Attendee(osv.Model):
    _name = "openacademy.attendee"
    
    _rec_name = 'partner_id'
    
    _columns = {

        'partner_id': fields.many2one('res.partner', string="Partner",
            required=True, ondelete='cascade'),
        'session_id': fields.many2one('openacademy.session', string="Session",
            required=True, ondelete='cascade'),
    }
    
    _sql_constraints = [("pair_unique", "unique(partner_id, session_id)",
        "The partner already follows this session")]