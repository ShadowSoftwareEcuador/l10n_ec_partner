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
    def update_identifiers(self):
        sql = """UPDATE res_partner SET identifier='9999999999'
        WHERE identifier is NULL"""
        self.env.cr.execute(sql)

    @api.model_cr_context
    def init(self):
        self.update_identifiers()
        super(ResPartner, self).init()
        sql_index = """
        CREATE UNIQUE INDEX IF NOT EXISTS
        unique_company_partner_identifier_type on res_partner
        (company_id, identifier_type, identifier)
        WHERE identifier_type <> 'pasaporte'"""
        self._cr.execute(sql_index)

    @api.multi
    @api.depends('identifier', 'name')
    def name_get(self):
        data = []
        for partner in self:
            display_val = u'{0} {1}'.format(
                partner.identifier or '*',
                partner.name
            )
            data.append((partner.id, display_val))
        return data

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=80):
        if not args:
            args = []
        if name:
            partners = self.search([('identifier', operator, name)] + args, limit=limit)  # noqa
            if not partners:
                partners = self.search([('name', operator, name)] + args, limit=limit)  # noqa
        else:
            partners = self.search(args, limit=limit)
        return partners.name_get()

    @api.one
    @api.constrains('identifier')
    def _check_identifier(self):
        if self.identifier_type == 'cedula':
            res = ec.ci.is_valid(self.identifier)
        elif self.identifier_type == 'ruc':
            res = ec.ruc.is_valid(self.identifier)
        else:
            return True
        if not res:
            raise ValidationError('Error en el identificador.')

    @api.one
    @api.depends('identifier')
    def _compute_person_type(self):
        if not self.identifier:
            self.person_type = '0'
        elif int(self.identifier[2]) <= 6:
            self.person_type = '6'
        elif int(self.identifier[2]) in [6, 9]:
            self.person_type = '9'
        else:
            self.person_type = '0'

    identifier = fields.Char('Cedula/ RUC',
        size=13,
        required=True,
        help='Identificación o Registro Único de Contribuyentes')
    identifier_type = fields.Selection(
        [
            ('cedula', 'CEDULA'),
            ('ruc', 'RUC'),
            ('pasaporte', 'PASAPORTE')
            ],
        'Tipo ID',
        required=True,
        default='pasaporte'
    )
    person_type = fields.Selection(
        compute='_compute_person_type',
        selection=[
            ('6', 'Persona Natural'),
            ('9', 'Persona Juridica'),
            ('0', 'Otro')
        ],
        string='Persona',
        store=True
    )
    is_company = fields.Boolean(default=True)