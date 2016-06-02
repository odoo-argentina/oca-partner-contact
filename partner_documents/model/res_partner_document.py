# -*- coding: utf-8 -*-
'''Define res.partner.document model'''
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError, UserError
import re

_help_validator_re = '''
https://docs.python.org/2/library/re.html#regular-expression-syntax
'''

_help_sub_re = '''
https://docs.python.org/2/library/re.html#regular-expression-syntax
'''

_help_template_re = '''
https://docs.python.org/2/library/re.html#regular-expression-syntax
'''

_help_template = '''
https://docs.python.org/2.7/library/string.html#formatspec
'''

_help_user_help = '''
You must describe how the user must write the document value to be parsed
and formated in the right way.
'''


class ResPartnerDocumentType(models.Model):
    _name = 'res.partner.document.type'
    _description = 'Partner document types'
    _rec_name = 'abbreviation'

    name = fields.Char('Name', size=120, required=True)
    abbreviation = fields.Char('Abbreviation', size=16, required=True)
    code = fields.Char(
        'Code',  size=16,
        help='This code is to be used by differents localizations',)
    validator_re = fields.Char('Validator parser', help=_help_validator_re)
    sub_re = fields.Char('Replace parser', help=_help_sub_re)
    sub = fields.Char('Replace for')
    template_re = fields.Char('Template parser', default='(.*)', required=True,
                              help=_help_template_re)
    template = fields.Char('Template', default='{0}', required=True,
                           help=_help_template)
    user_help = fields.Text('User help', help=_help_user_help)
    test_in = fields.Char('Input test string', default='', required=True)
    test_out = fields.Char('Output test string', compute='_get_test_out')
    active = fields.Boolean('Active', default=True)

    @api.onchange('validator_re',
                  'test_in')
    def _onchange_test_in(self):
        self.ensure_one()
        if not self.is_valid(self.test_in):
            return {
                'warning': {
                    'title': _('Warning'),
                    'message': _('Invalid input for %s') %
                    self.abbreviation}
            }

    @api.multi
    @api.constrains('validator_re',
                    'sub_re', 'sub',
                    'template_re', 'template',
                    'test_in')
    def _check_document_type(self):
        ''' Check if regular expression for this document type is well formated
            and if the test can be formated with the template expression '''
        for doc in self:
            if not doc.is_valid(doc.test_in):
                raise ValidationError('Invalid input for validation')

            if doc.sub_re:
                try:
                    sub = re.compile(doc.sub_re)
                except Exception, er:
                    raise ValidationError('Invalid regular expression'
                                          ' for substitution: %s' % er)
                test_in = sub.sub(doc.sub or '', doc.test_in)
            else:
                test_in = doc.test_in

            try:
                parser = re.compile(doc.template_re)
            except Exception, er:
                raise ValidationError('Invalid regular expression: %s' % er)

            match = parser.match(test_in)
            if not match:
                raise ValidationError('Test don\'t match with'
                                      ' regular expression')

            data_l = match.groups()
            data_d = match.groupdict()

            try:
                self.template.format(*data_l, **data_d)
            except Exception, er:
                raise ValidationError('Invalid format expression: %s' % er)

    @api.multi
    def is_valid(self, data):
        ''' Check if document is valid '''
        self.ensure_one()

        if not data:
            return True

        try:
            r = re.compile(self.validator_re).match(data)
        except:
            raise Warning(_('The document can\t be formated. %s')
                          % self.user_help)

        if r:
            return True
        else:
            return False

    @api.multi
    def _format(self, data):
        ''' Return formated document '''
        self.ensure_one()

        if not data:
            return False

        if self.sub_re:
            try:
                sub = re.compile(self.sub_re)
            except:
                raise Warning(_('The document can\'t be formated. %s')
                              % self.user_help)
            data = sub.sub(self.sub or '', data)

        try:
            parser = re.compile(self.template_re)
        except:
            raise Warning(_('The document can\'t be formated. %s')
                          % self.user_help)

        match = parser.match(data)

        if not match:
            raise Warning(_('The document can\'t be formated. %s')
                          % self.user_help)

        data_l = match.groups()
        data_d = match.groupdict()

        return self.template.format(*data_l, **data_d)

    @api.multi
    @api.depends('test_in',
                 'sub_re', 'sub',
                 'template_re', 'template')
    def _get_test_out(self):
        for doc in self:
            doc.test_out = doc._format(doc.test_in)
            try:
                pass
            except:
                doc.test_out = False


class ResPartnerDocument(models.Model):
    _name = 'res.partner.document'
    _order = 'sequence'

    partner_id = fields.Many2one('res.partner', 'Partner')
    document_type_id = fields.Many2one('res.partner.document.type', 'Type')
    value = fields.Char('Value')
    sequence = fields.Integer('Sequence', default=10)

    @api.constrains('document_type_id', 'value')
    def _check_document(self):
        for document in self:
            if not document.document_type_id.is_valid(self.value):
                raise UserError(_(
                    'Invalid document value %s for document type %s') % (
                    document.value, document.document_type_id.abbreviation))
