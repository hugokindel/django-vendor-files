from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
@stringfilter
def vendor(vendor_key, only=None):
    vendor_config = settings.VENDOR[vendor_key]

    tags = []

    if 'js' in vendor_config:
        if only is None or only == 'js':
            for file in vendor_config['js']:
                if hasattr(settings, 'VENDOR_CDN') and settings.VENDOR_CDN:
                    tag = '<script defer src="%(url)s/%(path)s" integrity="%(sri)s" crossorigin="anonymous" referrerpolicy="no-referrer"></script>' % {
                        'url': vendor_config['url'].rstrip('/'),
                        'path': file['path'],
                        'sri': file['sri'] if 'sri' in file else ''
                    }
                else:
                    tag = '<script defer src="%(vendor_url)s/%(vendor_key)s/%(path)s"></script>' % {
                        'vendor_url': settings.VENDOR_URL.rstrip('/'),
                        'vendor_key': vendor_key,
                        'path': file['path']
                    }

                tags.append(tag)

    if 'css' in vendor_config:
        if only is None or only == 'css':
            for file in vendor_config['css']:
                if hasattr(settings, 'VENDOR_CDN') and settings.VENDOR_CDN:
                    tag = '<link rel="stylesheet" href="%(url)s/%(path)s" integrity="%(sri)s" crossorigin="anonymous" referrerpolicy="no-referrer"/>' % { # noqa
                        'url': vendor_config['url'].rstrip('/'),
                        'path': file['path'],
                        'sri': file['sri'] if 'sri' in file else ''
                    }
                else:
                    tag = '<link rel="stylesheet" href="%(vendor_url)s/%(vendor_key)s/%(path)s" />' % {
                        'vendor_url': settings.VENDOR_URL.rstrip('/'),
                        'vendor_key': vendor_key,
                        'path': file['path']
                    }

                tags.append(tag)

    return mark_safe(''.join(tags))


@register.simple_tag()
@stringfilter
def vendor_js(vendor_key):
    return vendor(vendor_key, only='js')


@register.simple_tag()
@stringfilter
def vendor_css(vendor_key):
    return vendor(vendor_key, only='css')
