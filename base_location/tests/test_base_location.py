# Copyright 2015 Yannick Vaucher, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestBaseLocation(TransactionCase):

    def test_onchange_better_zip_state_id(self):
        """ Test onchange on res.better.zip """
        usa_MA = self.env.ref('base.state_us_34')
        better_zip1 = self.env['res.better.zip'].new(self.values_better_zip1())
        better_zip1.state_id = usa_MA
        better_zip1._onchange_state_id()
        self.assertEqual(better_zip1.country_id, usa_MA.country_id)

    def test_onchange_better_zip_city_id(self):
        better_zip2 = self.env['res.better.zip'].new(self.values_better_zip2())
        better_zip2.city_id = self.city_madrid
        better_zip2._onchange_city_id()
        self.assertEqual(better_zip2.city, self.city_madrid.name)

    def test_onchange_better_zip_country_id(self):
        better_zip1 = self.env['res.better.zip'].new(self.values_better_zip1())
        better_zip1.country_id = self.env.ref('base.es')
        better_zip1._onchange_country_id()
        self.assertFalse(better_zip1.state_id)

    def test_onchange_better_zip_none(self):
        better_zip1 = self.env['res.better.zip'].new(self.values_better_zip1())
        better_zip1.country_id = False
        better_zip1._onchange_country_id()
        self.assertFalse(better_zip1.state_id)

    def test_onchange_partner_city_completion(self):
        partner1 = self.env['res.partner'].new({
            'name': 'Camptocamp',
        })
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())
        better_zip2.country_id.enforce_cities = True
        partner1.zip_id = better_zip2
        partner1._onchange_zip_id()
        self.assertEqual(partner1.zip, better_zip2.name)
        self.assertEqual(partner1.city, better_zip2.city)
        self.assertEqual(partner1.state_id, better_zip2.state_id)
        self.assertEqual(partner1.country_id, better_zip2.country_id)

    def test_onchange_company_city_completion(self):
        company = self.env['res.company'].new({'name': 'Test'})
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        company.zip_id = better_zip1
        company._onchange_zip_id()
        self.assertEqual(company.zip, better_zip1.name)
        self.assertEqual(company.city, better_zip1.city)
        self.assertEqual(company.state_id, better_zip1.state_id)
        self.assertEqual(company.country_id, better_zip1.country_id)

    def test_company_address_fields(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1()
        )
        company = self.env['res.company'].create({
            'name': 'Test',
        })
        self.assertTrue(company.partner_id)
        company.partner_id.write({
            'zip_id': better_zip1.id,
            'state_id': better_zip1.state_id.id,
            'country_id': better_zip1.country_id.id,
            'city_id': better_zip1.city_id.id,
            'city': better_zip1.city,
            'zip': better_zip1.name,
        })
        company._compute_address()
        self.assertEqual(company.zip_id, company.partner_id.zip_id)
        self.assertEqual(company.city_id, company.partner_id.city_id)

    def test_company_address_fields_inverse(self):
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2()
        )
        company = self.env['res.company'].new({
            'name': 'Test',
            'partner_id': self.env['res.partner'].new({}).id
            # Partner must be initiated in order to be filled
        })
        company.update({
            'zip_id': better_zip2.id,
        })
        company._inverse_city_id()
        company._inverse_zip_id()
        self.assertEqual(company.zip_id, company.partner_id.zip_id)
        self.assertEqual(company.city_id, company.partner_id.city_id)

    def test_onchange_company_city_id_completion(self):
        company = self.env['res.company'].new({'name': 'Test'})
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())
        company.zip_id = better_zip2
        company._onchange_zip_id()
        self.assertEqual(company.city_id, better_zip2.city_id)

    def test_constrains_better_zip_01(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())

        better_zip1.city_id = self.city_lausanne
        with self.assertRaises(ValidationError):
            better_zip2.city_id = better_zip1.city_id

    def test_constrains_better_zip_02(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())

        with self.assertRaises(ValidationError):
            better_zip2.country_id = better_zip1.country_id

    def test_constrains_better_zip_03(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())

        with self.assertRaises(ValidationError):
            better_zip2.state_id = better_zip1.state_id

    def test_constrains_better_zip_04(self):
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())

        with self.assertRaises(ValidationError):
            better_zip2.city_id = self.city_madrid

    def test_constrains_partner_01(self):
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())
        with self.assertRaises(ValidationError):
            self.env['res.partner'].create({
                'name': 'P1',
                'zip_id': better_zip2.id,
            })

    def test_constrains_partner_02(self):
        better_zip2 = self.env['res.better.zip'].create(
            self.values_better_zip2())
        partner = self.env['res.partner'].create({
            'name': 'P1',
            'zip_id': better_zip2.id,
            'country_id': better_zip2.country_id.id,
            'state_id': better_zip2.state_id.id,
            'city_id': better_zip2.city_id.id,
        })

        with self.assertRaises(ValidationError):
            partner.country_id = self.ref('base.ch')

        with self.assertRaises(ValidationError):
            partner.state_id = self.state_vd.id,

        with self.assertRaises(ValidationError):
            partner.city_id = self.city_lausanne

    def values_better_zip1(self):
        return {
            'name': 1000,
            'city': 'Lausanne',
            'state_id': self.state_vd.id,
            'country_id': self.ref('base.ch'),
        }

    def values_better_zip2(self):
        return {
            'city_id': self.city_bcn.id,
            'city': self.city_bcn.name,
            'state_id': self.state_bcn.id,
            'country_id': self.ref('base.es'),
        }

    def test_partner_onchange_country(self):
        country_es = self.browse_ref('base.es')
        country_es.enforce_cities = True
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        partner = self.env['res.partner'].new({
            'name': 'TEST',
            'zip_id': better_zip1.id
        })
        partner.country_id = country_es
        partner._onchange_country_id()
        self.assertFalse(partner.zip_id)

    def test_partner_onchange_city(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        partner = self.env['res.partner'].new({
            'name': 'TEST',
            'zip_id': better_zip1.id
        })
        self.city_bcn.country_id.enforce_cities = False
        partner.city_id = self.city_bcn
        partner._onchange_city_id()
        self.assertFalse(partner.zip_id)
        partner.city_id = False
        res = partner._onchange_city_id()
        self.assertFalse(res['domain']['zip_id'])

    def test_partner_onchange_state(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        partner = self.env['res.partner'].new({
            'name': 'TEST',
            'zip_id': better_zip1.id
        })
        partner.state_id = self.state_bcn
        partner._onchange_state_id()
        self.assertFalse(partner.zip_id)

    def test_display_name(self):
        better_zip1 = self.env['res.better.zip'].create(
            self.values_better_zip1())
        self.assertEqual(
            better_zip1.display_name, '1000, Lausanne, Vaud, '+self.browse_ref(
                'base.ch'
            ).name
        )

    def setUp(self):
        super(TestBaseLocation, self).setUp()
        self.state_vd = self.env['res.country.state'].create({
            'name': 'Vaud',
            'code': 'VD',
            'country_id': self.ref('base.ch'),
        })
        self.env['res.country'].browse(self.ref('base.es')).write({
            'enforce_cities': True
        })
        self.company = self.env.ref('base.main_company')

        self.state_bcn = self.env['res.country.state'].create({
            'name': 'Barcelona',
            'code': '08',
            'country_id': self.ref('base.es'),
        })
        self.state_madrid = self.env['res.country.state'].create({
            'name': 'Madrid',
            'code': '28',
            'country_id': self.ref('base.es'),
        })
        self.city_bcn = self.env['res.city'].create({
            'name': 'Barcelona',
            'state_id': self.state_bcn.id,
            'country_id': self.ref('base.es'),
        })
        self.city_madrid = self.env['res.city'].create({
            'name': 'Madrid',
            'state_id': self.state_madrid.id,
            'country_id': self.ref('base.es'),
        })
        self.city_lausanne = self.env['res.city'].create({
            'name': 'Lausanne',
            'state_id': self.state_vd.id,
            'country_id': self.ref('base.ch'),
        })
