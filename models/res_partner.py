# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

try:
    from stdnum import ec
except ImportError as err:
    _logger.debug('Cannot import stdnum')


class ResPartner(models.Model):

    _inherit = 'res.partner'

    @api.multi
    @api.depends('vat', 'name')
    def name_get(self):
        data = []
        for partner in self:
            display_val = u'{0} {1}'.format(
                partner.vat or '*',
                partner.name
            )
            data.append((partner.id, display_val))
        return data

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        if not args:
            args = []
        if name:
            partners = self.search([('vat', operator, name)] + args, limit=limit)  # noqa
            if not partners:
                partners = self.search([('name', operator, name)] + args, limit=limit)  # noqa
        else:
            partners = self.search(args, limit=limit)
        return partners.name_get()

    @api.one
    @api.constrains('vat')
    def _check_identifier(self):
        if self.identifier_type == 'cedula':
            res = ec.ci.is_valid(self.vat)
        elif self.identifier_type == 'ruc':
            res = ec.ruc.is_valid(self.vat)
        else:
            return True
        if not res:
            raise ValidationError('Error en el identificador.')

    @api.one
    @api.depends('vat')
    def _compute_person_type(self):
        if not self.vat:
            self.person_type = '0'
        elif int(self.vat[2]) <= 6:
            self.person_type = '6'
        elif int(self.vat[2]) in [6, 9]:
            self.person_type = '9'
        else:
            self.person_type = '0'

    identifier_type = fields.Selection(
        [
            ('cedula', 'CEDULA'),
            ('ruc', 'RUC'),
            ('pasaporte', 'PASAPORTE')
            ],
        string='Tipo Identificador',
        required=True,
        default='ruc'
    )
    person_type = fields.Selection(
        compute='_compute_person_type',
        selection=[
            ('6', 'Persona Natural'),
            ('9', 'Persona Juridica'),
            ('0', 'Otro')
        ],
        string='Tipo Persona',
        store=True,
        default='9'
    )
    is_company = fields.Boolean(default=True)