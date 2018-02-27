## Copyright 2016 - 2018 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.
from __future__ import unicode_literals

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
        widgets = { 'po_number': forms.TextInput(attrs={'size': 20}),
                    'comment':forms.Textarea(attrs={'rows': 4, 'cols': 80}),
                    }
        
