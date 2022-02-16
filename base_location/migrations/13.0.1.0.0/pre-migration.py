# Copyright 2022 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    """Make city information consistent, as in previous versions, this field was
    conditionally filled depending if the country has enforced such data, and
    now, it's always filled.
    """
    cr.execute(
        """UPDATE res_partner rp
        SET city_id = rcz.city_id
        FROM res_city_zip rcz
        WHERE rp.city_id IS NULL AND rp.zip_id = rcz.id"""
    )
