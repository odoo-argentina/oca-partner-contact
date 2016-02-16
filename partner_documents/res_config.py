# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class base_config_settings(models.TransientModel):
    _inherit = 'base.config.settings'

    group_multiple_partner_documents = fields.Boolean(
        "Manage Multiple Partner Documents",
        implied_group='partner_documents.multiple_partner_documents',
        help="Show a new tab to edit multiple documents per partner"
        )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
