This module uppercases last names on create and write.

This module uses python `upper` function. This function uses the default
unicode case folding*. This works for many languages, but not for all, like
turkish where ı/I i/İ pairs work differently (see cpython issue
`17252 <https://bugs.python.org/issue17252>`_).

\* The uppercasing algorithm used is described in section 3.13
‘Default Case Folding’ of the
`Unicode Standard <https://www.unicode.org/versions/Unicode15.0.0/ch03.pdf>`_.
