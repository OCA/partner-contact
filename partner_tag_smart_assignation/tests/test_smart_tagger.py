from odoo.tests.common import SavepointCase
import logging

logger = logging.getLogger(__name__)


class TestSmartTagger(SavepointCase):

    @classmethod
    def setUpClass(cls):
        """ Load test data."""
        super().setUpClass()

        michel_fletcher = cls.browse_ref(cls, 'base.res_partner_address_4')
        chao_wang = cls.browse_ref(cls, 'base.res_partner_address_5')
        david_simpson = cls.browse_ref(cls, 'base.res_partner_address_10')
        john_m_brown = cls.browse_ref(cls, 'base.res_partner_address_11')
        charlie_bernard = cls.browse_ref(cls, 'base.res_partner_address_13')

        cls.partners = michel_fletcher + chao_wang + david_simpson + \
            john_m_brown + charlie_bernard
        cls.o_partners = chao_wang + david_simpson + john_m_brown
        cls.non_o_partners = michel_fletcher + charlie_bernard
        cls.michel_fletcher = michel_fletcher

    def create_condition(self):
        """
        create a condition, which filters all objects containing the letter 'o'
        in their name.
        """
        return self.env['ir.filters'].create({
            'user_id': False,
            'model_id': 'res.partner',
            'active': True,
            'domain': '[["name","ilike","o"]]',
            'context': '{}',
            'sort': '[]',
            'name': 'SmartTagTestCondition',
            'is_default': False,
            'action_id': False
        })

    def create_tag(self):
        """
        create a smart tag, which tags all partners containing the letter 'o'
        in their name.
        """
        return self.env['res.partner.category'].create({
            'name': 'Test Smart Tag',
            'active': True,
            'smart': True,
            'parent_id': False,
            'tag_filter_partner_field': 'partner_id',
            'tag_filter_condition_id': self.create_condition().id
        })

    def test_create_tag(self):
        """
        Tag all partners which have the letter 'o' in the name.
        """
        smart_tag = self.create_tag()
        for partner in self.o_partners:
            self.assertTrue(partner in smart_tag.partner_ids)

        for partner in self.non_o_partners:
            self.assertFalse(partner in smart_tag.partner_ids)

        for partner in smart_tag.partner_ids:
            self.assertTrue('o' in partner.name)

    def test_modify_partner(self):
        """
        Tag partners with the letter 'o' in the name.
        Then edit some name and check whether the smart tag updates
        """

        smart_tag = self.create_tag()

        # update some first names
        michael = self.michel_fletcher
        michael.update({'name': 'Michel Angelo'})

        # Simulate a cron trigger
        self.env['res.partner.category'].update_all_smart_tags()

        # verify that the updated tag contains the partner 'Michel Angelo'
        self.assertTrue(michael in smart_tag.partner_ids)

        for partner in smart_tag.partner_ids:
            self.assertTrue('o' in partner.name)

    def test_smart_tag_sql(self):
        """ Test query SQL for smart tags """
        smart_tag = self.env['res.partner.category'].create({
            'name': 'Test Smart Tag SQL',
            'active': True,
            'smart': True,
            'parent_id': False,
            'tag_filter_sql_query': """
                SELECT id
                FROM res_partner
                Where name like '%o%'
            """
        })
        # update some first names
        michael = self.michel_fletcher
        michael.write({'name': 'Michel Angelo'})

        # Trigger tag update
        smart_tag.update_partner_tags()

        # verify that the updated tag contains the partner 'Michel Angelo'
        self.assertTrue(michael in smart_tag.partner_ids)

        for partner in smart_tag.partner_ids:
            self.assertTrue('o' in partner.name)
