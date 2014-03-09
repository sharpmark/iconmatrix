# coding=utf-8
from django import template
register = template.Library()

@register.tag()
def active(parser, token):
    import re
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1:])

class NavSelectedNode(template.Node):
    '''
        def __init__(self, patterns):
            self.patterns = patterns

        def render(self, context):
            path = context['request'].path
            for p in self.patterns:
                pValue = template.Variable(p).resolve(context)
                if path == pValue:
                    return "active"
            return ""
    '''

    def __init__(self, urls):
        self.urls = urls

    def render(self, context):
        path = context['request'].path
        for url in self.urls:
            if '"' not in url:
                cpath = template.Variable(url).resolve(context)
            else:
                cpath = url.strip('"')

            if (cpath == '/' or cpath == '') and not (path == '/' or path == ''):
                return ""
            if path.startswith(cpath):
                return 'active'
        return ""
