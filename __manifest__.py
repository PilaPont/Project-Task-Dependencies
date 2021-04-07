{
    'name': 'Project Task Dependencies',
    'version': '14.0.0.0.1.0+210322',
    'summary': 'Enables to define dependencies (other tasks) of a task',
    'author': 'Kenevist Developers, Maryam Kia',
    'website': "www.kenevist.ir",
    'license': 'OPL-1',
    'category': 'Project',

    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}

