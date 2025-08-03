You can configure some common name patterns for the inverse function
in Settings > Configuration > General settings:

* Lastname SecondLastname Firstname: For example 'Anderson Lavarge Robert'
* Lastname SecondLastname, Firstname: For example 'Anderson Lavarge, Robert'
* Firstname Lastname SecondLastname: For example 'Robert Anderson Lavarge'

After applying the changes, you can recalculate all partners name clicking
"Recalculate names" button. Note: This process could take so much time depending
how many partners there are in database.

You can use *_get_inverse_name* method to get firstname, lastname and
second lastname from a simple string and also *_get_computed_name* to get a
name form the firstname, lastname and second lastname.
These methods can be overridden to change the format specified above.
