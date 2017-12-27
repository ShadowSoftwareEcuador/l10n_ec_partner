# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class PartnerTest(TransactionCase):

    def setUp(self):
        super(PartnerTest, self).setUp()
        self.Partner = self.env['res.partner']

    def test_create_partner_natural(self):
        vat = '0103893962'
        name = 'CRISTIAN GONZALO SALAMEA MALDONADO'
        identifier_type = 'cedula'

        self.partner_natural = self.Partner.create({
            'vat': vat,
            'name': name,
            'identifier_type': identifier_type,
        })

        self.assertEquals(self.partner_natural.vat, vat)
        self.assertEquals(self.partner_natural.name, name)
        self.assertEquals(self.partner_natural.identifier_type, identifier_type)

    def test_create_partner_juridico(self):
        vat = '0190416380001'
        name = 'AYNI CONSULTING'
        identifier_type = 'ruc'

        self.partner_juridico = self.Partner.create({
            'vat': vat,
            'name': name,
            'identifier_type': identifier_type,
        })
        self.assertEquals(self.partner_juridico.vat, vat)
        self.assertEquals(self.partner_juridico.name, name)
        self.assertEquals(self.partner_juridico.identifier_type, identifier_type)

    def test_search_consumidor_final(self):
        res = self.Partner.search([('vat', '=', '9999999999')], limit=1)
        self.assertEquals(res.name, 'CONSUMIDOR FINAL')
