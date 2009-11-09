from htmlentitydefs import name2codepoint
import re

def _replace_entity(m):
 s = m.group(1)
 if s[0] == u'#':
  s = s[1:]
  try:
   if s[0] in u'xX':
    c = int(s[1:], 16)
   else:
    c = int(s)
   return unichr(c)
  except ValueError:
   return m.group(0)
 else:
  try:
   return unichr(name2codepoint[s])
  except (ValueError, KeyError):
   return m.group(0)

_entity_re = re.compile(r"&(#?[xX]?(?:[0-9a-fA-F]+|\w{1,8}));")
def unescape(s):
 return _entity_re.sub(_replace_entity, s)
