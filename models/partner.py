
from openerp.osv import osv, fields 

class Partner(osv.Model):


    _inherit = 'res.partner'
    _columns = {
        'instructor' : fields.boolean("Instructor"),
    }
    _defaults = {
        'instructor' : False,
    }