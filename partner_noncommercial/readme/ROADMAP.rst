After installing this module a situation has been encountered where the new
menu's were added to the database, but not shown in the UI. This was due to
partner_left and partner_right not being filled. To solve this, use the
generic solution when the menu-system has been messed up:

#.  stop server
#.  drop parent_left and parent_right columns from ir_ui_menu table
#.  start server while updating base module

