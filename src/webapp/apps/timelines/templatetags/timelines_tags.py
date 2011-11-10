# coding=utf-8

from django import template
register = template.Library()

@register.tag
def timeline_item(parser, token):
    try:
        item = token.contents.split()[1]
    except ValueError:
        raise template.TemplateSyntaxError, "Tag requires one argument (timeline item)"
    
    return RenderTimelineNode(item)


class RenderTimelineNode(template.Node):
    def __init__(self, item):
        self.item = template.Variable(item)
        
    def render(self, context):
        try:
            item = self.item.resolve(context)
            t = template.loader.get_template('timeline/%s.html' % item.msg_id)
            context['obj'] = item
            return t.render(context)
        except Exception, e:
            raise
        

