# __openerp__.py
{
    'name': "Open Academy",
    'description': "Technical test",
    'author' : "Simon",
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'view/openacademy.xml',
        'view/openacademy_view.xml',
        'view/partner_view.xml',
        'wizard/create_attendee_view.xml',
    ],
    'depends': ['base'],
}