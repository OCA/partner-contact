To configure this module you need to:

#. Go to *Settings > Users & Companies > Users*.
#. Choose a user.
#. From field *Deduplicate Contacts* under *Other* in *Access Rights* tab
   choose desired permission level:

   - *Manually* allows to run a manual deduplication process.
   - *Automatically* allows to run an automatic deduplication process.

     .. warning::
      Automatic contact deduplication can easily lead to unwanted
      results. Better backup before choosing this option.

   - *Without restrictions* executes chosen deduplication method with admin
     rights, to be able to update objects where the user would not normally
     have write rights, and to allow them to merge contacts with different
     email addresses.

     .. warning::
      This is an advanced feature. Make sure to train the user(s) before
      enabling this permission.
