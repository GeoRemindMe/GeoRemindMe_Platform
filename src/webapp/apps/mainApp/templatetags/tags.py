# coding=utf-8

from django import template
register = template.Library()


@register.tag
def url2(parser, token):
    """
based on default tag
"""
    bits = token.split_contents()
    if len(bits) < 2:
        from django.template import TemplateSyntaxError
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    in_facebook = parser.compile_filter(bits[1])
    viewname = bits[2]
    args = []
    kwargs = {}
    asvar = None
    bits = bits[3:]
    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]
    import re
    kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")
    if len(bits):
        for bit in bits:
            match = kwarg_re.match(bit)
            if not match:
                raise TemplateSyntaxError("Malformed arguments to url tag")
            name, value = match.groups()
            if name:
                kwargs[name] = parser.compile_filter(value)
            else:
                args.append(parser.compile_filter(value))
    return URL2Node(viewname, args, kwargs, asvar, legacy_view_name=True, in_facebook=in_facebook)

class URL2Node(template.Node):
    def __init__(self, view_name, args, kwargs, asvar, legacy_view_name=True, in_facebook=False):
        self.view_name = view_name
        self.in_facebook = in_facebook
        self.legacy_view_name = legacy_view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.core.urlresolvers import reverse, NoReverseMatch
        from django.conf import settings
        args = [arg.resolve(context) for arg in self.args]
        from django.utils.encoding import smart_str
        kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                       for k, v in self.kwargs.items()])
        view_name = self.view_name
        in_facebook = self.in_facebook.resolve(context)
        if not self.legacy_view_name:
            view_name = view_name.resolve(context)
        if in_facebook and view_name.find('fb_') == -1:
            view_name = '%s%s' % ('fb_', view_name)
        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail,
        # re-raise the NoReverseMatch unless we're using the
        # {% url ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(view_name, args=args, kwargs=kwargs, current_app=context.current_app)
        except NoReverseMatch, e:
            if settings.SETTINGS_MODULE:
                project_name = settings.SETTINGS_MODULE.split('.')[0]
                try:
                    url = reverse(project_name + '.' + view_name,
                              args=args, kwargs=kwargs,
                              current_app=context.current_app)
                except NoReverseMatch:
                    if self.asvar is None:
                        # Re-raise the original exception, not the one with
                        # the path relative to the project. This makes a
                        # better error message.
                        raise e
            else:
                if self.asvar is None:
                    raise e

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


@register.filter
def naturaltime(value, arg=None):
    """
https://code.djangoproject.com/attachment/ticket/12771/humanize%2Bnaturaltime.diff
For date and time values shows how many seconds, minutes or hours ago compared to
current timestamp returns representing string. Otherwise, returns a string
formatted according to settings.DATE_FORMAT
"""
    from datetime import datetime
    from django.utils.translation import ugettext as _
    try:
        value = datetime(value.year, value.month, value.day, value.hour, value.minute, value.second)
    except AttributeError:
        return value
    except ValueError:
        return value
    delta = datetime.now() - value
    if delta.days > 0:
        value = datetime(value.year, value.month, value.day, value.hour, value.minute)
        return value #.strftime("%d/%m/%y %H:%M")
    elif delta.seconds == 0:
        return _(u'ahora mismo')
    elif delta.seconds < 60:
        return _(u"hace %s segundos" % (delta.seconds))
    elif delta.seconds / 60 < 2:
        return _(r'hace un minuto')
    elif delta.seconds / 60 < 60:
        return _(u"hace %s minutos" % (delta.seconds/60))
    elif delta.seconds / 60 / 60 < 2:
        return _(u'hace una hora')
    elif delta.seconds / 60 / 60 < 24:
        return _(u"hace %s horas" % (delta.seconds/60/60))
    value = datetime(value.year, value.month, value.day)
    return value


@register.simple_tag
def embedded_avatar(username):
    return None