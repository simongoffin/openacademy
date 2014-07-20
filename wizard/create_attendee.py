from openerp.osv import fields, osv

class CreateAttendeeWizard(osv.TransientModel):
    _name = 'openacademy.create.attendee.wizard'
    
    def action_add_attendee(self, cr, uid, ids, context=None):
        session_model = self.pool.get('openacademy.session')
        wizard = self.browse(cr, uid, ids[0], context=context)
        session_ids = [sess.id for sess in wizard.session_ids]
        att_data = [{'partner_id':att.partner_id.id} for att in wizard.attendee_ids]
        session_model.write(cr, uid, session_ids,
            {'attendee_ids': [(0, 0, data) for data in att_data]}, context)
        return {}

    _columns = {
        'session_id': fields.many2one('openacademy.session', 'Session',required=True),
        'attendee_ids': fields.one2many('openacademy.attendee.wizard','wizard_id', 'Attendees'),
    }

class AttendeeWizard(osv.TransientModel):
    _name = 'openacademy.attendee.wizard'
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Partner', required=True),
        'wizard_id':fields.many2one('openacademy.create.attendee.wizard'),
    }