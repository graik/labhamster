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

from django.db import models
from django.contrib.auth.models import User
from customfields import DayModelField, DayConversion
import tools as T

APP_URL = '/admin/labhamster'

class Order(models.Model):
    STATUS_TYPES = (('draft', 'draft'),
                    ('pending', 'pending'),
                    ('ordered', 'ordered'),
                    ('received', 'received'),
                    ('cancelled', 'cancelled'))
    
    status = models.CharField('Status', max_length=20, choices=STATUS_TYPES, 
                              default='pending')
    
    date_created = models.DateField('requested', auto_now_add=True, 
                                    help_text='Date when order was created')

    date_ordered = models.DateField('ordered', blank=True, null=True, 
                                    help_text='Date when order was placed')

    date_received = models.DateField('received', blank=True, null=True, 
                                     help_text='Date when item was received')

    created_by = models.ForeignKey(User, null=False, blank=False, db_index=True, 
                                   verbose_name='requested by', 
                                   related_name='requests', 
                                   help_text='user who created this order')

    ordered_by = models.ForeignKey(User, null=True, blank=True, db_index=True, 
                                   verbose_name='ordered by', 
                                   related_name='orders', 
                                   help_text='user who sent this order out')

    item = models.ForeignKey('Item', verbose_name='Item', related_name='orders', 
                             blank=False, null=False, 
                help_text='Click the magnifying lens to select from the list of existing items.\n'+\
                'For a new item, first click the lens, then click "Add Item" and fill out and save the Item form.' )

    unit_size = models.IntegerField(default=1)

    quantity = models.IntegerField(default=1)

    price = models.DecimalField(max_digits=6, decimal_places=2, 
                                blank=True, null=True)

    grant_category = models.CharField('Grant category', 
                                      choices=(('consumables', 'consumables'), 
                                               ('equipment', 'equipment')), 
                                      default='consumables', max_length=20)

    grant = models.ForeignKey('Grant', null=True, blank=True, db_index=True, 
                              related_name='orders')

    comment = models.TextField(blank=True, 
                               help_text="Order-related remarks. " +\
        "Please put catalog number and descriptions not here but into the "+\
        "item page.") 

    def __unicode__(self):
        return u'%04i -- %s' % (self.id, unicode(self.item))

    def get_absolute_url(self):
        """
        Define standard URL for object.get_absolute_url access in templates
        """
        return APP_URL + '/'+ self.get_relative_url()
    
    def get_relative_url(self):
        """
        Define standard relative URL for object access in templates
        """
        return 'order/%i/' % self.id

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)

    def Status(self):
        """color status display"""
        color = {u'ordered': '088A08',
                 u'pending': 'B40404'}
        return '<span style="color: #%s;">%s</span>' %\
               (color.get(self.status, '000000'), self.status)

    Status.allow_tags = True
    Status.admin_order_field = 'status'

    def requested(self):
        """filter '(None)' display in admin table"""
        if self.date_created:
            return self.date_created
        return u''

    requested.allow_tags = True
    requested.admin_order_field = 'date_created'
    
    def ordered(self):
        """filter '(None)' display in admin table"""
        if self.date_ordered:
            return self.date_ordered
        return u''

    ordered.allow_tags = True
    ordered.admin_order_field = 'date_ordered'

    def received(self):
        """filter '(None)' display in admin table"""
        if self.date_received:
            return self.date_received
        return u''

    received.allow_tags = True
    received.admin_order_field = 'date_ordered'

    def Price(self):
        """filter '(None)' display in admin table"""
        if self.price:
            return '%7.2f' % self.price
        return u''

    received.allow_tags = True
    received.admin_order_field = 'date_ordered'

    class Meta:
        ordering = ('date_created',)


class Item(models.Model):
    
    name = models.CharField(max_length=30, unique=True,
                            help_text='short descriptive name of this item')
    
    vendor = models.ForeignKey('Vendor', verbose_name='Vendor', 
                               blank=False, 
                               help_text='select normal supplier of this item')

    catalog = models.CharField(max_length=30, unique=False, blank=False, 
                               help_text='catalogue number')

    category = models.ForeignKey('Category', verbose_name='Product Category', 
                                 blank=False)

    shelflife = DayModelField(verbose_name='Shelf Life', unit='months', 
                              blank=True, null=True)

    STATUS_TYPES = (('ok', 'in stock'),
                    ('low', 'running low'),
                    ('out', 'not in stock'),
                    ('expired', 'expired'),
                    ('deprecated', 'deprecated'))

    status = models.CharField('Status', max_length=20, choices=STATUS_TYPES, 
                              default='out')

    link = models.URLField(verify_exists=True, blank=True, 
                           help_text='URL Link to product description')

    comment = models.TextField('comments & description', blank=True, 
                               help_text='')

    location = models.CharField(max_length=60, blank=True, 
                                help_text='location in the lab')

    def __unicode__(self):
        return u'%s [%s]' % (self.name, unicode(self.vendor))

    def get_absolute_url(self):
        """
        Define standard URL for object.get_absolute_url access in templates
        """
        return APP_URL + '/' + self.get_relative_url()
    
    def get_relative_url(self):
        """
        Define standard relative URL for object access in templates
        """
        return 'item/%i/' % self.id

    def related_orders(self):
        """
        @return: QuerySet of orders for this item
        """
        if self.orders:
            r = Order.objects.filter(item=self)
            return r
        return []

    def received(self):
        """filter '(None)' display in admin table"""
        if self.date_received:
            return self.date_received
        return ''

    received.allow_tags = True
    received.admin_order_field = 'date_ordered'

    def shelf_life(self):
        """filter '(None)' display in admin table"""
        if not self.shelflife:
            return ''
        return DayConversion.days2str(self.shelflife)

    class Meta:
        ordering = ('name', 'vendor')


class Vendor(models.Model):

    name = models.CharField(max_length=30, unique=True, 
                            verbose_name='Vendor name', 
                            help_text='short descriptive name of this supplier')

    link = models.URLField(verify_exists=True, blank=True, 
                           help_text='URL Link to Vendor home page')

    phone = models.CharField(max_length=20, blank=True, 
                             verbose_name='Contact phone')

    email = models.CharField(max_length=30, blank=True, 
                             verbose_name='Contact e-mail')

    contact = models.CharField(max_length=30, blank=True, 
                               verbose_name='Contact name')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        """
        Define standard URL for object.get_absolute_url access in templates
        """
        return APP_URL + '/' + self.get_relative_url()
    
    def get_relative_url(self):
        """
        Define standard relative URL for object access in templates
        """
        return 'vendor/%i/' % self.id
    

class Category(models.Model):

    name = models.CharField(max_length=20, unique=True, 
                            verbose_name='Product Category', 
                            help_text='name of product category')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Grant(models.Model):

    name = models.CharField(max_length=40, unique=True, 
                            help_text='descriptive name of grant')

    grant_id = models.CharField(max_length=30, unique=True, blank=True)

    comment = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.name + u' ' + self.grant_id)

    class Meta:
        ordering = ('name', 'grant_id')