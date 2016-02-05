# -*- coding: utf-8 -*-
'''Extend res.partner model'''
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    document_ids = fields.One2many('res.partner.document', 'partner_id',
                                   string='Documents')
    document_type_id = fields.Many2one('res.partner.document.type',
                                       string='Document Type')
    document_value = fields.Char(compute='_get_document_value',
                                 inverse='_set_document_value',
                                 string='Document Value')

    @api.multi
    @api.depends('document_type_id')
    def _get_document_value(self):
        document_ids = self.document_ids.filter(
            lambda d: d.document_type_id == self.document_type_id)
        if document_ids:
            return self.document_ids.value
        else:
            return False

    @api.multi
    def _set_document_value(self):
        document_ids = self.document_ids.filter(
            lambda d: d.document_type_id == self.document_type_id)
        if document_ids:
            self.document_ids.value = self.document_value
        else:
            document_ids.create({
                'partner_id': self.id,
                'document_type_id': self.document_ids.id,
                'document_value': self.document_value.id
            })
