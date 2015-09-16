# -*- coding: utf-8 -*-
#
#
#    Authors: Guewen Baconnier
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#


class RevisionMixin(object):

    def assert_revision(self, partner, expected_changes):
        """ Check if a revision has been created according to expected values

        The partner should have no prior revision than the one created in the
        test (so it has exactly 1 revision).

        The expected changes are tuples with (field, current_value,
        new_value, state)

        :param partner: record of partner having a revision
        :param expected_changes: contains tuples with the changes
        :type expected_changes: list(tuple))
        """
        revision = self.env['res.partner.revision'].search(
            [('partner_id', '=', partner.id)],
        )
        self.assertEqual(len(revision), 1,
                         "1 revision expected, got %s" % (revision,))
        changes = revision.change_ids
        missing = []
        for expected_change in expected_changes:
            for change in changes:
                if (change.field_id, change.current_value, change.new_value,
                        change.state) == expected_change:
                    changes -= change
                    break
            else:
                missing.append(expected_change)
        message = u''
        for field, current_value, new_value, state in missing:
            message += ("- field: '%s', current_value: '%s', "
                        "new_value: '%s', state: '%s'\n" %
                        (field.name, current_value, new_value, state))
        for change in changes:
            message += ("+ field: '%s', current_value: '%s', "
                        "new_value: '%s', state: '%s'\n" %
                        (change.field_id.name, change.current_value,
                         change.new_value, change.state))
        if message:
            raise AssertionError('Changes do not match\n\n:%s' % message)

    def _create_revision(self, partner, changes):
        """ Create a revision and its associated changes

        :param partner: 'res.partner' record
        :param changes: list of changes [(field, new value, state)]
        :returns: 'res.partner.revision' record
        """
        change_values = [
            (0, 0, {
                'field_id': field.id,
                'current_value': partner[field.name],
                'new_value': value,
                'state': state,
            }) for field, value, state in changes
        ]
        values = {
            'partner_id': partner.id,
            'change_ids': change_values,
        }
        return self.env['res.partner.revision'].create(values)
