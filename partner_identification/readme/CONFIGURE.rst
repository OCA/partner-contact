Configure all ID types you need in Contacts > Configuration > Partner ID Categories.
For example, we create a category 'Driver License':

Name:
  Name of this ID type. For example, 'Driver License'
Code:
  Code, abbreviation or acronym of this ID type. For example, 'driver_license'
Python validation code:
  Optional python code called to validate ID numbers of this ID type. This functionality can be
  overridden by setting ``id_no_validate`` to ``True`` in the context, such as:

  .. code-block:: python

     partner.with_context(id_no_validate=True).write({
        'name': 'Bad Value',
        'category_id': self.env.ref('id_category_only_numerics').id,
     })
