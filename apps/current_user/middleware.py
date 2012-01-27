from django.db.models import signals
from django.utils.functional import curry
from django.utils.decorators import decorator_from_middleware
import logging

from current_user import registration
#import pdb
class CurrentUserMiddleware(object):
    def process_request(self, request):
        #logging.debug("CurrentUserMiddleware.process_request")
        if request.method in ('HEAD', 'OPTIONS', 'TRACE'):
            # this request shouldn't update anything, so no signal handler should be attached
            return

        if hasattr(request, 'user') and request.user.is_authenticated():
            user = request.user
        else:
            user = None

        logging.debug("CurrentUserMiddleware.process_request: %s" % user)


        update_users = curry(self.update_users, user)
        signals.pre_save.connect(update_users, dispatch_uid = request, weak = False)

    def update_users(self, user, sender, instance, **kwargs):
        registry = registration.FieldRegistry()
        if sender in registry:
            for field in registry.get_fields(sender):
                # need to only set owner id if it hasn't already been set
                if instance.id and field.name == 'owner':
                     owner_id = sender.objects.get(id=instance.id).owner_id
                     if owner_id:
                        #pdb.set_trace()
                        instance.owner_id = owner_id
                     else:
                        setattr(instance, field.name, user)
                else:
                    setattr(instance, field.name, user)

    def process_response(self, request, response):

        signals.pre_save.disconnect(dispatch_uid = request)
        return response

record_current_user = decorator_from_middleware(CurrentUserMiddleware)
#logging.debug("CurrentUserMiddleware.process_request")