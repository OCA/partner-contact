# Copyright 2015 Yannick Vaucher, Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import tagged, common
from odoo.tools.misc import mute_logger
import psycopg2


@tagged('post_install', '-at_install')
class TestBaseLocation(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        country_obj = cls.env['res.country.state']
        city_obj = cls.env['res.city']
        zip_obj = cls.env['res.city.zip']
        cls.partner_obj = cls.env['res.partner']
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.state_vd = country_obj.create({
            'name': 'Vaud',
            'code': 'VD',
            'country_id': cls.env.ref('base.ch').id,
        })
        cls.env.ref('base.es').write({
            'enforce_cities': True
        })
        cls.company = cls.env.ref('base.main_company')

        cls.state_bcn = country_obj.create({
            'name': 'Barcelona',
            'code': '08',
            'country_id': cls.env.ref('base.es').id,
        })
        cls.state_madrid = country_obj.create({
            'name': 'Madrid',
            'code': '28',
            'country_id': cls.env.ref('base.es').id,
        })
        cls.city_bcn = city_obj.create({
            'name': 'Barcelona',
            'state_id': cls.state_bcn.id,
            'country_id': cls.env.ref('base.es').id,
        })
        cls.city_madrid = city_obj.create({
            'name': 'Madrid',
            'state_id': cls.state_madrid.id,
            'country_id': cls.env.ref('base.es').id,
        })
        cls.city_lausanne = city_obj.create({
            'name': 'Lausanne',
            'state_id': cls.state_vd.id,
            'country_id': cls.env.ref('base.ch').id,
        })
        cls.lausanne = zip_obj.create({
            'name': '666',
            'city_id': cls.city_lausanne.id,
        })
        cls.barcelona = zip_obj.create({
            'name': '444',
            'city_id': cls.city_bcn.id,
        })

    def test_onchange_partner_city_completion(self):
        """Test that partner data is filled accodingly"""
        partner1 = self.partner_obj.new({
            'name': 'Camptocamp',
        })
        self.barcelona.city_id.country_id.enforce_cities = True
        partner1.zip_id = self.barcelona
        partner1._onchange_zip_id()
        self.assertEqual(partner1.zip, self.barcelona.name)
        self.assertEqual(partner1.city, self.barcelona.city_id.name)
        self.assertEqual(partner1.state_id, self.barcelona.city_id.state_id)
        self.assertEqual(partner1.country_id,
                         self.barcelona.city_id.country_id)

    def test_onchange_company_city_completion(self):
        """Test that company data is filled accodingly"""
        company = self.env['res.company'].new({'name': 'Test'})
        company.zip_id = self.lausanne
        company._onchange_zip_id()
        self.assertEqual(company.zip, self.lausanne.name)
        self.assertEqual(company.city, self.lausanne.city_id.name)
        self.assertEqual(company.state_id, self.lausanne.city_id.state_id)
        self.assertEqual(company.country_id, self.lausanne.city_id.country_id)

    def test_company_address_fields(self):
        """Test if the partner address fields changes when
        changing the ones from the company"""
        company = self.env['res.company'].create({
            'name': 'Test',
        })
        self.assertTrue(company.partner_id)
        company.partner_id.write({
            'zip_id': self.lausanne.id,
            'state_id': self.lausanne.city_id.state_id.id,
            'country_id': self.lausanne.city_id.country_id.id,
            'city_id': self.lausanne.city_id.id,
            'city': self.lausanne.city_id.name,
            'zip': self.lausanne.name,
        })
        company._compute_address()
        self.assertEqual(company.zip_id, company.partner_id.zip_id)
        self.assertEqual(company.city_id, company.partner_id.city_id)

    def test_company_address_fields_inverse(self):
        """Test inverse fields from res.company"""
        company = self.env['res.company'].new({
            'name': 'Test',
            'partner_id': self.partner_obj.new({}).id
            # Partner must be initiated in order to be filled
        })
        company.update({
            'zip_id': self.barcelona.id,
        })
        company._inverse_city_id()
        company._inverse_zip_id()
        self.assertEqual(company.zip_id, company.partner_id.zip_id)
        self.assertEqual(company.city_id, company.partner_id.city_id)

    def test_onchange_company_city_id_completion(self):
        """Test city auto-completion when changing zip in a company"""
        company = self.env['res.company'].new({'name': 'Test'})
        company.zip_id = self.barcelona
        company._onchange_zip_id()
        self.assertEqual(company.city_id, self.barcelona.city_id)

    def test_constrains_partner_01(self):
        """Test partner 1 constraints"""
        with self.assertRaises(ValidationError):
            self.partner_obj.create({
                'name': 'P1',
                'zip_id': self.barcelona.id,
            })

    def test_writing_company(self):
        self.company.zip_id = self.barcelona

    def test_constrains_partner_country(self):
        """Test partner country constraints"""
        partner = self.partner_obj.create({
            'name': 'P1',
            'zip_id': self.barcelona.id,
            'country_id': self.barcelona.city_id.country_id.id,
            'state_id': self.barcelona.city_id.state_id.id,
            'city_id': self.barcelona.city_id.id,
        })

        with self.assertRaises(ValidationError):
            partner.country_id = self.ref('base.ch')

    def test_constrains_partner_state(self):
        """Test partner state constraints"""
        partner = self.partner_obj.create({
            'name': 'P1',
            'zip_id': self.barcelona.id,
            'country_id': self.barcelona.city_id.country_id.id,
            'state_id': self.barcelona.city_id.state_id.id,
            'city_id': self.barcelona.city_id.id,
        })

        with self.assertRaises(ValidationError):
            partner.state_id = self.state_vd.id

    def test_constrains_partner_city(self):
        """Test partner city constraints"""
        partner = self.partner_obj.create({
            'name': 'P1',
            'zip_id': self.barcelona.id,
            'country_id': self.barcelona.city_id.country_id.id,
            'state_id': self.barcelona.city_id.state_id.id,
            'city_id': self.barcelona.city_id.id,
        })

        with self.assertRaises(ValidationError):
            partner.city_id = self.city_lausanne

    def test_partner_onchange_country(self):
        """Test partner onchange country_id"""
        country_es = self.env.ref('base.es')
        country_es.enforce_cities = True
        partner = self.partner_obj.new({
            'name': 'TEST',
            'zip_id': self.lausanne.id
        })
        partner.country_id = country_es
        partner._onchange_country_id()
        self.assertFalse(partner.zip_id)

    def test_partner_onchange_city(self):
        """Test partner onchange city_id"""
        partner = self.partner_obj.new({
            'name': 'TEST',
            'zip_id': self.lausanne.id
        })
        self.city_bcn.country_id.enforce_cities = False
        partner.city_id = self.city_bcn
        partner._onchange_city_id()
        self.assertFalse(partner.zip_id)
        partner.city_id = False
        res = partner._onchange_city_id()
        self.assertFalse(res['domain']['zip_id'])

    def test_partner_onchange_state(self):
        """Test partner onchange state_id"""
        partner = self.partner_obj.new({
            'name': 'TEST',
            'zip_id': self.lausanne.id
        })
        partner.state_id = self.state_bcn
        partner._onchange_state_id()
        self.assertFalse(partner.zip_id)
        self.assertEqual(partner.country_id, partner.state_id.country_id)

    def test_company_onchange_state(self):
        """Test company onchange state_id"""
        self.company.state_id = self.state_bcn
        self.company._onchange_state_id()
        self.assertEqual(self.company.country_id,
                         self.company.state_id.country_id)

    def test_display_name(self):
        """Test if the display_name is stored and computed properly"""
        self.assertEqual(
            self.lausanne.display_name,
            '666, Lausanne, Vaud, ' + self.browse_ref(
                'base.ch'
            ).name
        )

    def test_name_search(self):
        """Test that zips can be searched through both the name of the
        city or the zip code"""
        madrid_data = {
            'city_id': self.city_madrid.id,
            'name': '555',
        }

        madrid = self.env['res.city.zip'].create(madrid_data)

        found_recs = self.env['res.city.zip'].name_search(name='444')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], self.barcelona.id)
        found_recs = self.env['res.city.zip'].name_search(name='Barcelona')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], self.barcelona.id)

        found_recs = self.env['res.city.zip'].name_search(name='555')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], madrid.id)
        found_recs = self.env['res.city.zip'].name_search(name='Madrid')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], madrid.id)

        found_recs = self.env['res.city.zip'].name_search(name='666')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], self.lausanne.id)
        found_recs = self.env['res.city.zip'].name_search(name='Lausanne')
        self.assertEqual(len(found_recs), 1)
        self.assertEqual(found_recs[0][0], self.lausanne.id)

    def test_zip_ql_constraints(self):
        """Test UNIQUE name within it's area for zips"""
        with self.assertRaises(
                psycopg2.IntegrityError), mute_logger('odoo.sql_db'):
            self.env['res.city.zip'].create({
                'name': '666',
                'city_id': self.city_lausanne.id,
            })

    def test_city_sql_contraint(self):
        """Test UNIQUE name within it's area for cities"""
        with self.assertRaises(
                psycopg2.IntegrityError), mute_logger('odoo.sql_db'):
            self.env['res.city'].create({
                'name': 'Barcelona',
                'state_id': self.state_bcn.id,
                'country_id': self.ref('base.es'),
            })
