## Copyright 2016 Raik Gruenberg

## This file is part of the LabHamster project (https://github.com/graik/labhamster). 
## LabHamster is released under the MIT open source license, which you can find
## along with this project (LICENSE) or at <https://opensource.org/licenses/MIT>.

from labhamster.models import *
from django.contrib import admin
import django.forms
from django.http import HttpResponse

import customforms

def export_csv(request, queryset, fields):
    """
    Helper method for Admin make_csv action. Exports selected objects as 
    CSV file.
    fields - OrderedDict of name / field pairs, see Product.make_csv for example
    """
    import csv

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'
    
    writer = csv.writer(response)
    writer.writerow(fields.keys())

    for o in queryset:
        columns = []
        for name,value in fields.items():
            try:
                columns.append( eval('o.%s'%value) )
            except:
                columns.append("")  ## capture 'None' fields

        columns = [ c.encode('utf-8') if type(c) is unicode else c \
                    for c in columns]
            
        writer.writerow( columns )

    return response
    

class RequestFormAdmin(admin.ModelAdmin):
    """
    ModelAdmin that adds a 'request' field to the form generated
    by the Admin. 
    """

    def get_form(self, request, obj=None, **kwargs):
        """
        Assign request variable to form
        http://stackoverflow.com/questions/1057252/how-do-i-access-the-request-object-or-any-other-variable-in-a-forms-clean-met
        (last answer, much simpler than Django 1.6 version)
        """
        form = super(RequestFormAdmin, self).get_form(request, obj=obj, **kwargs)
        form.request = request
        return form   


class GrantAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Grant, GrantAdmin)

class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)


class VendorAdmin(admin.ModelAdmin):

    fieldsets = ((None, {'fields': (('name',),
                                    ('link', 'login', 'password'),)}),
                 ('Contact', {'fields' : (('contact',),
                                          ('email','phone'),)})
                 )


    list_display = ('name', 'link', 'login', 'password')

    ordering = ('name',)
    search_fields = ('name', 'contact')

admin.site.register(Vendor, VendorAdmin)

class ProductAdmin(admin.ModelAdmin):
    fieldsets = ((None, {'fields': (('name', 'category'),
                                    ('vendor', 'catalog', 'link'),
                                    ('status', 'shelflife'),
                                    'comment',
                                    'location')}),)
    
    list_display = ('name', 'vendor', 'category', 'shelf_life', 'status')
    list_filter = ('status', 'category', 'vendor')

    ordering = ('name',)
    search_fields = ('name', 'comment', 'catalog', 'location', 'vendor__name')

    save_as = True

    actions = ['make_ok',
               'make_low',
               'make_out',
               'make_deprecated',
               'make_csv']

    ## reduce size of Description text field.
    formfield_overrides = {
        models.TextField: {'widget': django.forms.Textarea(
            attrs={'rows': 4,
                   'cols': 80})},
    }    

    def make_ok(self, request, queryset):
        n = queryset.update(status='ok')
        self.message_user(request, '%i products were updated' % n)

    make_ok.short_description = 'Mark selected entries as in stock'

    def make_low(self, request, queryset):
        n = queryset.update(status='low')
        self.message_user(request, '%i products were updated' % n)

    make_low.short_description = 'Mark selected entries as running low'

    def make_out(self, request, queryset):
        n = queryset.update(status='out')
        self.message_user(request, '%i products were updated' % n)

    make_out.short_description = 'Mark selected entries as out of stock'

    def make_deprecated(self, request, queryset):
        n = queryset.update(status='deprecated')
        self.message_user(request, '%i products were updated' % n)

    make_deprecated.short_description = 'Mark selected entries as deprecated'
    
    def make_csv(self, request, queryset):
        from collections import OrderedDict
        
        fields = OrderedDict( [('Name', 'name'),
                               ('Vendor', 'vendor.name'),
                               ('Catalog','catalog'),
                               ('Category','category.name'),
                               ('Shelf_life','shelflife'),
                               ('Status','status'),
                               ('Location','location'),
                               ('Link','link'),
                               ('Comment','comment')])
        return export_csv( request, queryset, fields)
    
    make_csv.short_description = 'Export products as CSV'

admin.site.register(Product, ProductAdmin)


class OrderAdmin(RequestFormAdmin):
    form = customforms.OrderForm
    
    raw_id_fields = ('product',)

    fieldsets = ((None, 
                  {'fields': (('status', 'product'), 
                              ('created_by', 'ordered_by', 'date_ordered', 
                               'date_received'))}),
                 ('Details', {'fields': (('unit_size', 'quantity'),
                                         'price',
                                         ('grant', 'grant_category'),
                                         'comment')}))
    
    radio_fields = {'grant': admin.VERTICAL,
                    'grant_category': admin.VERTICAL}
    
    list_display = ('product', 'quantity', 'Price', 'requested', 'ordered', 
                    'received', 'truncated_comment', 'Status')
    list_filter = ('status', 
                   'product__category__name', 'grant', 'created_by', 'product__vendor__name',)
    ordering = ('-date_created', 'product', 'quantity')

    search_fields = ('comment', 'grant__name', 'grant__grant_id', 'product__name', 
                     'product__vendor__name')

    save_as = True

    date_hierarchy = 'date_created'

    actions = ['make_ordered', 'make_received', 'make_cancelled', 'make_csv']
    
    ## reduce size of Description text field.
    formfield_overrides = {
        models.TextField: {'widget': django.forms.Textarea(
            attrs={'rows': 4,
                   'cols': 80})},
    }    

    def truncated_comment(self, obj):
        """shorten comment to 15 characters for table display"""
        return T.truncate( obj.comment, 17 )
    truncated_comment.short_description = 'comment'


    def make_ordered(self, request, queryset):
        """
        Mark several orders as 'ordered'
        see: https://docs.djangoproject.com/en/1.4/ref/contrib/admin/actions/
        """
        import datetime
        n = queryset.update(status='ordered', ordered_by=request.user, 
                            date_ordered=datetime.datetime.now())
        self.message_user(request, '%i orders were updated' % n)

    make_ordered.short_description = 'Mark selected entries as ordered'

    def make_received(self, request, queryset):
        import datetime
        n = queryset.update(date_received=datetime.datetime.now(), 
                            status='received')
        i = 0
        for order in queryset:
            order.product.status = 'ok'
            order.product.save()
            i += 1

        self.message_user(request, 
                          '%i orders were updated and %i products set to "in stock"'\
                          % (n, i))

    make_received.short_description= 'Mark as received (and update product status)'

    def make_cancelled(self, request, queryset):
        import datetime

        n = queryset.update(date_received=None, date_ordered=None, 
                            status='cancelled')
        self.message_user(request, '%i orders were set to cancelled' % n)

    make_cancelled.short_description = 'Mark selected entries as cancelled'
    

    def make_csv(self, request, queryset):
        """
        Export selected orders as CSV file
        """
        from collections import OrderedDict
       
        fields = OrderedDict( [('Product', 'product.name'),
                               ('Quantity', 'quantity'),
                               ('Price','price'),
                               ('Vendor','product.vendor.name'),
                               ('Catalog','product.catalog'),
                               ('Requested','date_created'),
                               ('Requested by','created_by.username'),
                               ('Ordered','date_ordered'),
                               ('Ordered by','ordered_by.username'),
                               ('Received','date_received'),
                               ('Status','status'),
                               ('Comment','comment')])
        
        return export_csv(request, queryset, fields)
    
    make_csv.short_description = 'Export orders as CSV'


admin.site.register(Order, OrderAdmin)