from types import ListType, TupleType, IntType
from DateTime import DateTime

def getType(data):
  res = 'str'
  if isinstance(data, ListType):
    res = 'list'
  if isinstance(data, TupleType):
    res = 'tuple'
  if isinstance(data, IntType):
    res = 'int'
  if type(data) == type(DateTime()):
    res = 'date'
  return res