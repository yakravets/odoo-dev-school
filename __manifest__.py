{
    'name': 'Odoo Hospital',
    'version': '18.0.0.0.1',
    'description': ' Hospital module app',
    'author': 'Yaroslav Kravets',
    'website': 'https://yaroslavkravets.pp.ua',
    'license': 'OPL-1',
    'category': 'Customization',
    
    'depends': [
        'base'
    ],

    'external_dependencies':{
        'python':[]
    },

    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menus.xml',
        'views/hr_hospital_specialization_view.xml',
        'views/hr_hospital_doctor_view.xml',
        'views/hr_hospital_patient_view.xml',
        'views/hr_hospital_type_of_disease_view.xml',
        'views/hr_hospital_patient_visit_view.xml',
    ],

    'demo': [

    ],

    'instalable': True,
    'auto_install': False,
    'application': True,

    'images': [
        'static/description/icon.jpg'
    ]
}