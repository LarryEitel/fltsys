from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from idios.views import profile, base_profile
from idios.utils import get_profile_model


def profile(request, username, **kwargs):
	# @@@ not group-aware (need to look at moving to profile model)
	page_user = get_object_or_404(User, username=username)
	profile_class = get_profile_model()
	profile = get_object_or_404(profile_class, user=page_user)
	return base_profile(request, profile, page_user, **kwargs)