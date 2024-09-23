#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


def _get_name_from_date(date):
    return f"Name from {date}"


def _set_partner_name(partner, name, date=None):
    name_history = partner.name_history_ids
    partner.name = name
    if date is not None:
        new_name_history = partner.name_history_ids - name_history
        new_name_history.change_date = date
