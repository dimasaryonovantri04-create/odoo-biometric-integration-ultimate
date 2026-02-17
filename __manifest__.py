{
    'name': 'Odoo Pro Biometric Integration',
    'summary': 'Professional biometric integration with advanced logging, UI, and configuration.',
    'author': 'Dimas Aryo Novantri',
    'category': 'Human Resources/Attendances',
    'depends': [
        'hr_attendance',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/hr_biometric_data_views.xml', 
        'views/hr_attendance_views.xml',   
        'views/biometric_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
