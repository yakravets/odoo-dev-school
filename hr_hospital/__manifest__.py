{
    'name': 'Odoo Hospital',
    'version': '18.0.0.0.1',
    'author': 'Yaroslav Kravets',
    'website': 'https://yaroslavkravets.pp.ua',
    'license': 'LGPL-3',
    'category': 'Customization',
    'depends': [
        'base'
    ],
    'external_dependencies': {
        'python': []
    },
    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'report/report_doctor.xml',
        'data/ir_sequence_data.xml',
        'wizard/hr_hospital_disease_report_wizard_view.xml',
        'wizard/hr_hospital_doctor_schedule_wizard_view.xml',
        'wizard/hr_hospital_mass_reassign_doctor_wizard_view.xml',
        'wizard/hr_hospital_patient_card_export_wizard_view.xml',
        'views/hr_hospital_specialization_view.xml',
        'views/hr_hospital_doctor_view.xml',
        'views/hr_hospital_patient_view.xml',
        'views/hr_hospital_type_of_disease_view.xml',
        'views/hr_hospital_patient_visit_view.xml',
        'views/hr_hospital_contact_person_view.xml',
        'views/hr_hospital_doctor_schedule_view.xml',
        'views/hr_hospital_medical_diagnosis_view.xml',
        'views/hr_hospital_patient_doctor_history_view.xml',
        'views/hr_hospital_menus.xml',
    ],
    'demo': [
        'demo/hr_hospital_specialization_demo.xml',
        'demo/hr_hospital_type_of_disease_demo.xml',
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_contact_person_demo.xml',
        'demo/hr_hospital_patient_visit_demo.xml',
        'demo/hr_hospital_medical_diagnosis_demo.xml',
        'demo/hr_hospital_doctor_schedule_demo.xml',
        'demo/hr_hospital_patient_doctor_history_demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': [
        'static/description/icon.jpg'
    ]
}
