## Copyright 2016 - 2018 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.
from __future__ import unicode_literals

from django.db import models
import django.forms as forms
from django.utils.text import capfirst
from django.utils.translation import gettext as _
import re
from os.path import splitext

class TextField(forms.CharField):
    """
    A multi-line text input area with custom dimensions
    """
    widget = forms.Textarea

    def __init__(self, rows = None, cols = None, attrs = {}, *args, **kwargs):
        """
        widget - override default widget (default: django.forms.Textarea)
        rows   - int, row parameter passed to default Textarea widget
        cols   - int, cols parameter passed to default Textarea widget
        attrs  - {str:str}, other parameters passed to widget
        """
        self.attrs = {}
        if rows:
            self.attrs['rows'] = rows
        if cols:
            self.attrs['cols'] = cols
        self.attrs.update(attrs)
        for key, value in self.attrs.items():
            if value is not None:
                self.attrs[key] = str(value)

        super(TextField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return self.attrs


class TextModelField(models.TextField):

    def __init__(self, *args, **kw):
        """
        @param extensions: [str], allowed file extensions
        @param size: int, maximum file size
        """
        self.rows = kw.pop('rows', None)
        self.cols = kw.pop('cols', None)
        super(TextModelField, self).__init__(*args, **kw)

    def formfield(self, **kwargs):
        defaults = {'form_class': TextField}
        defaults.update(kwargs)
        defaults.update({'rows': self.rows,
                         'cols': self.cols})
        
        return super(TextModelField, self).formfield(**defaults)


class DayConversion:
    UNITS = ('days', 'weeks', 'months', 'years')
    CONVERSION = (1, 7, 30, 365)

    @staticmethod
    def days2tuple(value):
        """
        value - int, time in days
        -> ( int, int ) - ( duration, factor ) where factor is 1, 7, 30 or 365
        """
        choices = zip(DayConversion.UNITS, DayConversion.CONVERSION)
        choices.reverse()
        for unit, factor in choices:
            if value % factor == 0:
                return (value / factor, factor)

        return (value, 1)

    @staticmethod
    def tuple2days(time, factor):
        return time * factor

    @staticmethod
    def days2str(value):
        """
        value - int, time in days
        -> str, 'duration unit' where unit is days, weeks, months or years
        """
        duration, factor = DayConversion.days2tuple(value)
        lookup = dict(zip(DayConversion.CONVERSION, DayConversion.UNITS))
        unit = lookup[factor]
        
        if duration == 1:
            unit = unit[:-1]
        
        return '%i %s' % (duration, unit)


class DayWidget(forms.MultiWidget):
    """
    A widget that displays a duration of days as days, weeks, months or years
    Adapted from: http://djangosnippets.org/snippets/2327/
    """
    UNITS = ('days', 'weeks', 'months', 'years')
    CONVERSION = (1, 7, 30, 365)

    def __init__(self, attrs = None):
        choices = zip(self.CONVERSION, self.UNITS)
        self.attrs = attrs or {}
        
        widgets = (forms.TextInput(attrs={'size': '5'}), 
                   forms.Select(attrs=self.attrs, choices=choices))
        
        super(DayWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        """
        Called for display of Widget -- convert single value from database
        (days) into two values (integer + unit).
        """
        if value:
            return DayConversion.days2tuple(value)
        return (None, None)


class DayFormField(forms.MultiValueField):
    widget = DayWidget

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        choices = zip(self.widget.CONVERSION, self.widget.UNITS)
        initial = str(kwargs.get('unitchoice', 1))
        initial = ('months', '30')
        
        if 'unitchoice' in kwargs:
            del kwargs['unitchoice']

        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])

        localize = kwargs.get('localize', False)

        fields = (forms.IntegerField(min_value=0, required=False, 
                                     localize=localize), 
                  forms.ChoiceField(choices=choices, initial=initial))

        super(DayFormField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """
        convert input from form widget (int + unit) into single number (days)
        """
        if data_list and data_list[0]:
            duration = data_list[0]
            unit = data_list[1] or '1'
            unit = int(unit)
            return data_list[0] * unit


class DayModelField(models.Field):

    def __init__(self, unit = 'days', *args, **kwargs):
        """
        unit - str, either of: 'days', 'weeks', 'months' or 'years' ['days'] 
        """
        self.conversion = dict(zip(DayWidget.UNITS, DayWidget.CONVERSION))
        self.unitchoice = self.conversion.get(unit, None)
        
        super(DayModelField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'IntegerField'

    def formfield(self, **kwargs):
        defaults = {'form_class': DayFormField,
                    'unitchoice': self.unitchoice}
        defaults.update(**kwargs)
        
        return super(DayModelField, self).formfield(**defaults)
    
    def deconstruct(self):
        """
        Required for migrations support
        https://docs.djangoproject.com/en/1.9/howto/custom-model-fields/#custom-field-deconstruct-method
        """
        name, path, args, kwargs = super(DayModelField, self).deconstruct()
        if self.unitchoice != self.conversion['days']:
            backconversion = dict(zip(self.conversion.values(), self.conversion.keys()))
            kwargs['unit'] = backconversion.get(self.unitchoice, None)
        return name, path, args, kwargs

    ## replaced by deconstruct() in django v1.7+ 
    ##from south.modelsinspector import add_introspection_rules
    ##add_introspection_rules([], ["^labhamster\.customfields\.datafields\.DayModelField"])

if __name__ == '__main__':
    pass