# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Partners Skills Management',
    'category': 'Partner / Contacts',
    'sequence': 270,
    'version': '1.0',
    'summary': 'Manage skills, knowledge and resumé contacts or partners',
    'description':
        """
Skills and Resumé for Partner Contacts
========================

This module introduces skills and resumé management for Patners. Forked from the hr_skills set of modules to serve as a stand-alone module when HR modules are not needed.
        """,
    'depends': ['contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/partner_skills_security.xml',
        'views/partner_views.xml',
        'data/partner_resume_data.xml',
    ],
    'demo': [
        'data/partner_resume_demo.xml',
        'data/partner.skill.csv',
        'data/partner.resume.line.csv',
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'partner_skills/static/src/css/partner_skills.scss',
            'partner_skills/static/src/js/resume_widget.js',
        ],
        'web.qunit_suite_tests': [
            'partner_skills/static/tests/**/*',
        ],
        'web.assets_qweb': [
            'partner_skills/static/src/xml/**/*',
        ],
    },
    'license': 'LGPL-3',
}
