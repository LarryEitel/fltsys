# from http://gist.github.com/67724

from django.db import models
from django.conf import settings
from django.utils.html import linebreaks, urlize
from django.utils.safestring import mark_safe

PLAIN_TEXT, HTML, MARKDOWN, REST, TEXTILE = range(5)
MARKUP_TYPES = (
    (PLAIN_TEXT, 'plain'),
    (HTML, 'html'),
)

try:
    import markdown
    MARKUP_TYPES += ( (MARKDOWN, 'markdown'), )
except ImportError:
    pass

try:
    from docutils.core import publish_parts
    MARKUP_TYPES += ( (REST, 'restructuredtext'), )
except ImportError:
    pass

try:
    import textile
    MARKUP_TYPES += ( (TEXTILE, 'textile'), )
except ImportError:
    pass

_rendered_field_name = lambda name: '%s_rendered' % name
_markup_type_field_name = lambda name: '%s_markup_type' % name

class MarkupField(models.TextField):
    ''' Provides a field that allows multiple markup types.
        Also stores the pre-rendered result in the database. 

        Example usage:

        class BlogPost(models.Model):
        ...
        post = MarkupField()

        Fields can then be accessed as follows:

        BlogPost.objects.get(pk=1).post # raw content
        BlogPost.objects.get(pk=1).post_markup_type # markup type (plain text, html, markdown, rest, textile)
        BlogPost.objects.get(pk=1).post_rendered # content of post rendered to html
        BlogPost.objects.get(pk=1).post_as_html # property that access post_rendered but marked safe for easy use in template 
    '''
    def __init__(self, *args, **kwargs):
        super(MarkupField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        markup_type_field = models.PositiveIntegerField(choices=MARKUP_TYPES, default=MARKDOWN)
        rendered_field = models.TextField(editable=False)
        cls.add_to_class(_markup_type_field_name(name), markup_type_field)
        cls.add_to_class(_rendered_field_name(name), rendered_field)
        super(MarkupField, self).contribute_to_class(cls, name)

        def as_html(self):
            return mark_safe(getattr(self, _rendered_field_name(name)))
        cls.add_to_class('%s_as_html' % name, property(as_html))

    def pre_save(self, model_instance, add):
        markup_type = getattr(model_instance, _markup_type_field_name(self.attname))
        markup = getattr(model_instance, self.attname)

        if markup_type == MARKDOWN:
            rendered = markdown.markdown(markup)
        elif markup_type == REST:
            docutils_settings = getattr(settings, "RESTRUCTUREDTEXT_FILTER_SETTINGS", {})
            parts = publish_parts(source=markup, writer_name="html4css1", settings_overrides=docutils_settings)
            rendered = parts["fragment"]
        elif markup_type == TEXTILE:
            rendered = textile.textile(markup, encoding='utf-8', output='utf-8')
        elif markup_type == PLAIN_TEXT:
            rendered = urlize(linebreaks(markup))
        else:
            rendered = markup

        setattr(model_instance, _rendered_field_name(self.attname), rendered)

        return markup