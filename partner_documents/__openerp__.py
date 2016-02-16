# -*- coding: utf-8 -*-
{
    "name": "Partner documents",
    "version": "9.0.0.0.0",
    "author": "Moldeo Interactive,ADHOC SA,Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "depends": [
        'base_setup',
    ],
    "demo": [
        'data/demo.xml',
    ],
    "test": [
        'test/test_dni.yml',
        'test/test_cuit.yml',
    ],
    "data": [
        'view/res_partner.xml',
        'view/res_partner_document_type.xml',
        'view/menu.xml',
        'res_config_view.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
    ],
    "js": [
    ],
    "css": [
    ],
    "qweb": [
    ],
    "auto_install": False,
    'installable': True,
    "external_dependencies": {
        'python': [],
    },
}
