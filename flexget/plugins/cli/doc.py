from __future__ import unicode_literals, division, absolute_import
import logging
import sys
from flexget.plugin import plugins
from flexget.options import add_subparser

log = logging.getLogger('doc')


def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def print_doc(options):
    plugin_name = options.doc
    plugin = plugins.get(plugin_name, None)
    if plugin:
        if not plugin.instance.__doc__:
            print 'Plugin %s does not have documentation' % plugin_name
        else:
            print ''
            print trim(plugin.instance.__doc__)
            print ''
    else:
        print 'Could not find plugin %s' % plugin_name

parser = add_subparser('doc', print_doc, help='display plugin documentation')
parser.add_argument('doc', metavar='<plugin name>', help='name of plugin to show docs for')
