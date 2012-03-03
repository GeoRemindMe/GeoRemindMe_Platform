try:
  import cjson as json
except (ImportError, NameError):
  raise
  try:
    from django.utils import simplejson as json
  except (ImportError, NameError):
    import simplejson as json
try:
  json.dumps
  json.loads
except AttributeError:
  try: # monkey patching for python-json package
    json.dumps = lambda obj, *args, **kwargs: json.encode(obj)
    json.loads = lambda str, *args, **kwargs: json.decode(str)
  except AttributeError:
    raise ImportError('Could not load an apropriate JSON library '
                      'currently supported are simplejson, '
                      'python2.6 json and python-json')

loads = json.loads
dumps = json.dumps