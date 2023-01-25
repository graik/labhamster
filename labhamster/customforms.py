# Copyright 2016 - 2018 Raik Gruenberg

# This file is part of the LabHamster project (https://github.com/graik/labhamster).
# LabHamster is released under the MIT open source license, which you can find
# along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.
import django.forms as forms
from django.db.models import Case, When
from django.contrib.auth.models import User
import labhamster.models as M


class OrderForm(forms.ModelForm):
    """Customized form for Order add/change"""

    def __init__(self, *args, **kwargs):
        """
        relies on self.request which is created by RequestFormAdmin
        """
        super(OrderForm, self).__init__(*args, **kwargs)

        # only execute for Add forms without existing instance
        o = kwargs.get('instance', None)
        if not o and self.request:
            # stopped working in django 1.9:
            ## self.initial['created_by'] = str(self.request.user.id)
            self.fields['created_by'].initial = self.request.user.id

        users = User.objects.order_by(
            Case(When(id=self.request.user.id, then=0), default=1), 'username')

        self.fields['created_by'].queryset = users
        self.fields['ordered_by'].queryset = users

        if self.instance.grant:
            grants = M.Grant.objects.filter(active=True) \
                | M.Grant.objects.filter(pk=self.instance.grant.pk)
        else:
            grants = M.Grant.objects.filter(active=True)

        self.fields['grant'].queryset = grants
        self.fields['grant'].label_from_instance = self.label_from_instance

    def label_from_instance(self, option):
        """Sets the string displayed in the form for the given option."""
        label = option.__str__()
        if not option.active:
            label += " (expired)"
        return label

    class Meta:
        model = M.Order
        fields = "__all__"
        widgets = {'po_number': forms.TextInput(attrs={'size': 20}),
                   'comment': forms.Textarea(attrs={'rows': 4, 'cols': 80}),
                   }
