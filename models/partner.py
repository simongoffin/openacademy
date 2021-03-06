
from openerp.osv import osv, fields 

class Partner(osv.Model):
    
    """Inherited res.partner"""


    _inherit = 'res.partner'
    _columns = {
        'instructor' : fields.boolean("Instructor"),
        
        # Relational fields
        'session_ids': fields.many2many("openacademy.session", string="Session",
        domain=['|',('instructor','=',True),('category_id.name','ilike','Teacher')]),
    }
    _defaults = {
        'instructor' : False,
    }