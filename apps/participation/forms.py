from django.forms import ModelForm, HiddenInput

from participation.models import Idea, Meetingnote, Newsarticle, Media, Data

class IdeaForm(ModelForm):
	class Meta:
		model = Idea
		exclude = ("author", "desc_markup_type", "ip", "created", "last_modified", "itemtype")
		widgets = {
			"geometry": HiddenInput(),
		}
		
class MeetingnoteForm(ModelForm):
	class Meta:
		model = Meetingnote
		exclude = ("author", "desc_markup_type", "ip", "created", "last_modified", "itemtype")
		widgets = {
			"geometry": HiddenInput(),
		}
		
class NewsarticleForm(ModelForm):
	class Meta:
		model = Newsarticle
		exclude = ("author", "desc_markup_type", "ip", "created", "last_modified", "itemtype")
		widgets = {
			"geometry": HiddenInput(),
		}
		
class MediaForm(ModelForm):
	class Meta:
		model = Media
		exclude = ("author", "desc_markup_type", "ip", "created", "last_modified", "itemtype")
		widgets = {
			"geometry": HiddenInput(),
		}
		
class DataForm(ModelForm):
	class Meta:
		model = Data
		exclude = ("author", "desc_markup_type", "ip", "created", "last_modified", "itemtype")
		widgets = {
			"geometry": HiddenInput(),
		}