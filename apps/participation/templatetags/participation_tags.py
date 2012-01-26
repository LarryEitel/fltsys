from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import Count
from django.contrib.comments.models import Comment

from participation.models import Shareditem, Station, Theme

register = template.Library()


@register.filter
@stringfilter
def fixbackslash(value):
	"""Replace backslashes '\'  in encoded polylines for Google Maps overlay."""
	return value.replace('\\','\\\\')


def get_activity(activity):
	""" Returns resource for given external media object """
	if activity.itemtype == "e" and activity.url:
		resource = activity.get_oembed()
		return {
			'activity': activity,
			'resource': resource,
		}

	return {
		'activity': activity,
	}


def get_activity_stats(section, target):
	""" Returns aggregated counts for Shareditems """
	
	if section == 'station':
		stats = Shareditem.objects.filter(station=target).values('itemtype').order_by().annotate(Count('itemtype'))
		shareditems = Shareditem.objects.filter(station=target).select_subclasses()
	elif section == 'theme':
		stats = Shareditem.objects.filter(theme=target).values('itemtype').order_by().annotate(Count('itemtype'))
		shareditems = Shareditem.objects.filter(theme=target).select_subclasses()
	# [{'itemtype__count': 4, 'itemtype': u'e'}]
	
	# total comment count for target, theme or station
	comment_count = Comment.objects.for_model(target).count()
	for shareditem in shareditems:
		contenttype = shareditem.get_child_contenttype()
		comment_count += Comment.objects.filter(content_type=contenttype.id, object_pk=shareditem.id).count()
		
	# add a verbose version of the itemtype key
	for stat in stats:
		stat['itemtype_display'] = Shareditem.ITEMTYPES_PLURAL[stat['itemtype']]
	
	return {
		'object': target,
		'stats': stats,
		'comment_count': comment_count,
	}


def get_topbar_content(context):
	request = context['request']
	stations = Station.objects.all().order_by('name')
	themes = Theme.objects.all().order_by('title')

	return {
		'user': request.user,
		'stations': stations,
		'themes': themes,
	}


register.inclusion_tag("participation/_activity.html")(get_activity)
register.inclusion_tag("participation/_activity_stats.html")(get_activity_stats)
register.inclusion_tag("_topbar.html", takes_context=True)(get_topbar_content)
