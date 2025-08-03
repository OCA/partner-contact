* With many partner records the search can be slow because all partners are computed.
* No grouping is allowed.
* We can't use negative operators on advanced searches as they won't throw the right
  results. This seems to be due tu the subfield negative search where we end up having
  an `=` operator and a ``Query`` object that is use to optimize this kind of searches.
