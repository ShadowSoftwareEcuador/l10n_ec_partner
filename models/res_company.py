# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    from stdnum import ec
except ImportError as err:
    _logger.debug('Cannot import stdnum')


class ResCompany(models.Model):
    _inherit = 'res.company'

    accountant_id = fields.Many2one('res.partner', 'Contador')
    sri_id = fields.Many2one('res.partner', 'Servicio de Rentas Internas')
    legal_representative_id = fields.Char('Cédula Representante Legal', size=10)
