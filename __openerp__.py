# __openerp__.py
{
    'name': "Open Academy",
    'description': "Technical test",
    'author' : "Simon",
    'data': [
        'security/ir.model.access.csv',
        'view/openacademy.xml',
        'view/openacademy_view.xml',
        'view/partner_view.xml',
    ],
    'depends': ['base'],
}