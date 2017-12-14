# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class PartnerTest(TransactionCase):

    def setUp(self):
        super(PartnerTest, self).setUp()
        self.Partner = self.env['res.partner']

        self.partner_natural = self.Partner.create({
            'vat': '0103893962',
            'name': 'CRISTIAN GONZALO SALAMEA MALDONADO',
            'identifier_type': 'cedula',
        })
        self.partner_juridico = self.Partner.create({
            'vat': '0190416380001',
            'name': 'AYNI CONSULTING',
            'identifier_type': 'ruc'
        })

    def test_create_partner_natural(self):
        self.assertEquals(self.partner_natural.vat, '0103893962')

    def test_create_partner_juridico(self):
        self.assertEquals(self.partner_juridico.vat, '0190416380001')

    def test_search(self):
        res = self.Partner.search([('vat', '=', '9999999999')], limit=1)
        self.assertEquals(res.name, 'CONSUMIDOR FINAL')
