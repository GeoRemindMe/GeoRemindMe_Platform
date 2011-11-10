"""
    django templates tags for images
    @author: R. BECK
    @version: 0.1
"""
# http://djangosnippets.org/snippets/2267/

#from __future__ import with_statement #Python 2.5

import base64
import os
import Image
from re import compile as compile_re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO  import StringIO

from django.conf     import settings
from django.template import TemplateSyntaxError, Node, Library, Template

register = Library()

TEMPLATE_DEBUG = settings.TEMPLATE_DEBUG
MEDIA_ROOT     = settings.MEDIA_ROOT
CACHE_DIR      = "/tmp"

templatevar_re = compile_re("\{\{(.+)\}\}")
media_re       = compile_re("\{\{MEDIA_ROOT|MEDIA_URL\}\}")


class EmbeddedImgNode(Node):
    """Image node parser for rendering html inline base64 image"""
    
    def __init__(self, attributes):
        self.attrs = {}
        attrs = self.attrs
        for attr_value in attributes:
            try:
                attr, value = attr_value.split('=', 1)
            except ValueError, val_err:
                raise TemplateSyntaxError(u"Syntax Error :", val_err)
            attrs[attr] = value

        src = attrs.get('src')
        if not src:
            raise TemplateSyntaxError(u"You have to specify a non-empty src \
                                        attribute")


    def _encode_img(self, file_path):
        """Returns image base64 string representation and makes a cache file"""
        filename   = file_path.rpartition(os.sep)[2]
        need_cache = True
        content    = ""

        cache_file = "%s_cache" % os.path.join(CACHE_DIR, filename)

        try:
            with open(cache_file, 'r') as cached_file:
                content = cached_file.read()
            need_cache = False
        except IOError:
            pass

        if need_cache:
            try:
                image = open(file_path, 'r')
                out   = StringIO()
                base64.encode(image, out)
                content = out.getvalue().replace('\n', '')
            except IOError:
                pass
            else:
                try:
                    with open(cache_file, 'w+') as cached_file:
                        cached_file.write(content)
                except IOError:
                    pass
        return content


    def _render_img(self):
        """Prepare image attributes"""
        attrs = self.attrs
        attrs_get = attrs.get
        src    = attrs_get('src')
        height = attrs_get('height')
        width  = attrs_get('width')

        if media_re.search(src):
            src = src.replace('{{MEDIA_ROOT}}', '') \
                     .replace('{{MEDIA_URL}}', '')
         
        src = src.replace('"', '')
        src = os.path.join(MEDIA_ROOT, src)

        try:
            img     = Image.open(src)
            _width, _height    = img.size
            _format = 'image/%s' % img.format

            if not height:
                attrs['height'] = '%spx' % _height

            if not width:
                attrs['width'] = '%spx' % _width

            b64encoded = self._encode_img(img.filename)

            attrs['src'] = "data:%s;base64,%s" % (_format, b64encoded)
        except IOError:
            attrs['src'] = ""


    def render(self, context):
        self._render_img()

        attrs  = self.attrs
        search = templatevar_re.search

        for k, v in attrs.iteritems():
            if search(v):
                attrs[k] = Template(v).render(context)

        return """<img %s />""" % ' '.join(['%s=%s' % (k, v if v else '""')
                                             for k, v in attrs.iteritems()])



@register.tag(name="embedded_img")
def do_embedded_img(parser, token):
    return EmbeddedImgNode(token.split_contents()[1:])