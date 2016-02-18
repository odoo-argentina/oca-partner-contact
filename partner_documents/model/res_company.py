# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    document_type_id = fields.Many2one(
        related='partner_id.document_type_id'
        )
    document_value = fields.Char(
        related='partner_id.document_value'
        )
