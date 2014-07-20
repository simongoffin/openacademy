from openerp.osv import fields, osv

class CreateAttendeeWizard(osv.TransientModel):
    _name = 'openacademy.create.attendee.wizard'

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