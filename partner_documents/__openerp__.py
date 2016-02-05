# -*- coding: utf-8 -*-
{
    "name": "Partner documents",
    "version": "9.0.0.0.0",
    "author": "Moldeo Interactive, Ing. Adhoc,Odoo Community Association (OCA)",
    "complexity": "normal",
    "category": "Customer Relationship Management",
    "depends": [
        'base',
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
        'security/ir.model.access.csv',
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
