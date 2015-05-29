# -*- encoding: utf-8 -*-

# Odoo, Open Source Management Solution
# Copyright (C) 2014-2015  Grupo ESOC <www.grupoesoc.es>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

{
    "name": "Partner second last name",
    "description": """
Add a second las tname for non company partners
===============================================

In some countries, it"s important to have a second last name for contacts. This
module extends the module ``partner_firstname`` to fit that need.

Contact partners will need to fulfill at least one of the name fields
(*First name*, *First last name* or *Second last name*).
""",
    "version": "1.0",
    "author": "Grupo ESOC",
    "maintainer": "Grupo ESOC",
    "category": "Extra Tools",
    "website": "http://www.grupoesoc.es",
    "depends": [
        "partner_firstname"
    ],
    "data": [
        "views/res_partner.xml",
        "views/res_user.xml",
    ],
    "installable": True,
}
