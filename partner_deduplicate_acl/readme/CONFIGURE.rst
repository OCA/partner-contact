To configure this module, you need to:

#. Go to *Settings > Users > Users*.
#. Choose a user.
#. Choose the desired permission level(s) in *Appplication > Deduplicate
   Contacts*:

   - *Manually* allows him to do the manual deduplication process.
   - *Automatically* allows him to do the automatic deduplication process.

     .. warning::
         Automatic contact deduplication can easily lead to unwanted results.
         Better backup before doing it.

   - *Without restrictions* executes the chosen deduplication method with admin
     rigts, to be able to update objects where the user would normally not have
     write rights, and to allow him to merge contacts with different email
     addresses.

     .. warning::
        This is an advanced feature, be sure to train the user before enabling
        this permission for him.
