# -*- coding: utf-8 -*-
{
    'name': "Carpooling",

    'summary': """
        This carpooling module allows the users to create car trips as well as booking others' trips to go somewhere together by sharing a vehivle.
        """,

    'description': """
        This module has been developed during the OpenWeek 2022 organised by the EPL (UCLouvain).
        It was developed in parternship with Odoo with the objective to propose a carpooling module to replace the existing solution (Excel sheets).
        This module allows the user to create car trips (in which he will be the driver) as well as book an existing trip (in which he will be a passenger).
        A trip corresponds to going from some place to another at a given date and time. Thus drivers and passengers can share a vehicle and optimise their trips.
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
