from django import template

register = template.Library()


@register.inclusion_tag('core/slideshow_tag.html')
def slideshow(images):
    return {'images': images}
