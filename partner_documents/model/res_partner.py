# -*- coding: utf-8 -*-
'''Extend res.partner model'''
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    document_ids = fields.One2many('res.partner.document', 'partner_id',
                                   string='Documents')
    document_type_id = fields.Many2one('res.partner.document.type',
                                       string='Document Type',
                                       )
    document_value = fields.Char(compute='_get_document_value',
                                 inverse='_set_document_value',
                                 string='Document Value')

    @api.multi
    @api.depends('document_type_id')
    def _get_document_value(self):
        """
        We get the first partner document for partner main document type
        """
        for partner in self:
            documents = partner.document_ids.filtered(
                lambda x: x.document_type_id == partner.document_type_id)
            partner.document_value = documents and documents[0].value or False

    @api.multi
    def _set_document_value(self):
        for partner in self:
            if partner.document_type_id and partner.document_value:
                partner_documents = partner.document_ids.filtered(
                    lambda d: d.document_type_id == partner.document_type_id)
                if partner_documents:
                    partner_documents[0].value = partner.document_value
                else:
                    partner_documents.create({
                        'partner_id': partner.id,
                        'document_type_id': partner.document_type_id.id,
                        'value': partner.document_value
                    })
