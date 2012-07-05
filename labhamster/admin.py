## Copyright 2012 Raik Gruenberg

## This file is part of the labhamster project (http://labhamster.sf.net)
## Labhamster is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as
## published by the Free Software Foundation, either version 3 of the
## License, or (at your option) any later version.

## Labhamster is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.

## You should have received a copy of the GNU Affero General Public
## License along with labhamster. If not, see <http://www.gnu.org/licenses/>.

from labhamster.models import *
from django.contrib import admin
from django.http import HttpResponse

class GrantAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Grant, GrantAdmin)

class CategoryAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Category, CategoryAdmin)


class VendorAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Vendor, VendorAdmin)

class ItemAdmin(admin.ModelAdmin):
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
               'mark_deprecated']

    def make_ok(self, request, queryset):
        n = queryset.update(status='ok')
        self.message_user(request, '%i items were updated' % n)

    make_ok.short_description = 'Mark selected entries as in stock'

    def make_low(self, request, queryset):
        n = queryset.update(status='low')
        self.message_user(request, '%i items were updated' % n)

    make_low.short_description = 'Mark selected entries as running low'

    def make_out(self, request, queryset):
        n = queryset.update(status='out')
        self.message_user(request, '%i items were updated' % n)

    make_out.short_description = 'Mark selected entries as out of stock'

    def make_deprecated(self, request, queryset):
        n = queryset.update(status='deprecated')
        self.message_user(request, '%i items were updated' % n)

    make_deprecated.short_description = 'Mark selected entries as deprecated'


admin.site.register(Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    
    raw_id_fields = ('item',)

    fieldsets = ((None, 
                  {'fields': (('status', 'item'), 
                              ('created_by', 'ordered_by', 'date_ordered', 
                               'date_received'))}),
                 ('Details', {'fields': (('unit_size', 'quantity'),
                                         'price',
                                         ('grant', 'grant_category'),
                                         'comment')}))
    
    radio_fields = {'grant': admin.VERTICAL,
                    'grant_category': admin.VERTICAL}
    
    list_display = ('item', 'quantity', 'Price', 'requested', 'ordered', 
                    'received', 'truncated_comment', 'Status')
    list_filter = ('status', 
                   'item__category__name', 'created_by', 'item__vendor__name' )
    ordering = ('-date_created', 'item', 'quantity')

    search_fields = ('comment', 'grant__name', 'grant__grant_id', 'item__name', 
                     'item__vendor__name')

    save_as = True

    date_hierarchy = 'date_created'

    actions = ['make_ordered', 'make_received', 'make_cancelled', 'make_csv']

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
            order.item.status = 'ok'
            order.item.save()
            i += 1

        self.message_user(request, 
                          '%i orders were updated and %i items set to "in stock"'\
                          % (n, i))

    make_received.short_description= 'Mark as received (and update item status)'

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
        import csv
        from collections import OrderedDict
       
        fields = OrderedDict( [('Item', 'item.name'),
                               ('Quantity', 'quantity'),
                               ('Price','price'),
                               ('Vendor','item.vendor.name'),
                               ('Catalog','item.catalog'),
                               ('Requested','date_created'),
                               ('Requested by','created_by.username'),
                               ('Ordered','date_ordered'),
                               ('Ordered by','ordered_by.username'),
                               ('Received','date_received'),
                               ('Status','status'),
                               ('Comment','comment')])
        
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders.csv'
        
        writer = csv.writer(response)
        writer.writerow(fields.keys())

        for order in queryset:
            columns = []
            for name,value in fields.items():
                try:
                    columns.append( eval('order.%s'%value) )
                except:
                    columns.append("")  ## capture 'None' fields

            columns = [ c.encode('utf-8') if type(c) is unicode else c \
                        for c in columns]
                
            writer.writerow( columns )
 
        return response
    
    make_csv.short_description = 'Export orders as CSV'


admin.site.register(Order, OrderAdmin)