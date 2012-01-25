from paypal.standard.ipn.signals import payment_was_successful
def show_me_the_money(sender, **kwargs):
    ipn_obj = sender
    # Undertake some action depending upon `ipn_obj`.
    if ipn_obj.custom == "Upgrade all users!":
        Users.objects.update(paid=True)
        
    print __file__,1, 'This works'
    
payment_was_successful.connect(show_me_the_money) 