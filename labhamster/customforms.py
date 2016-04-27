import django.forms as forms
import labhamster.models as M


class OrderForm(forms.ModelForm):
    """Customized form for Order add/change"""
    
    def __init__(self, *args, **kwargs):
        """
        relies on self.request which is created by RequestFormAdmin
        """
        super(OrderForm, self).__init__(*args, **kwargs)
        
        ## only execute for Add forms without existing instance
        o = kwargs.get('instance', None)
        if not o and self.request: 
            ## stopped working in django 1.9:
            ## self.initial['created_by'] = str(self.request.user.id)
            self.fields['created_by'].initial = self.request.user.id

    class Meta:
        model = M.Order
        fields = "__all__" 
