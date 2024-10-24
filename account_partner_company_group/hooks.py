# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import logging


def pre_init_hook(env):
    """Prepopulate stored related fields for faster installation"""
    logger = logging.getLogger(__name__)
    logger.info("Prepopulating stored related fields")
    env.execute(
        """
        ALTER TABLE account_move
        ADD COLUMN IF NOT EXISTS company_group_id integer;
        """
    )
