from django.db import models
from dateutil import rrule
from datetime import datetime, date, timedelta
from django.utils.translation import ugettext_lazy as _
import os

from feincms.content.image.models import ImageContent
import ImageFile

def get_storage_path(instance, filename):
    return os.path.join('uploads/contacts/', 'photos', filename)

class Beamline(models.Model):
    '''
    Basic beamline information for ``Visit`` entries.
    
    '''
    name = models.CharField(blank=False,max_length=30)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        """Human readable string for Beamline"""
        return self.name        
        
class SupportPerson(models.Model):
    '''
    Identification and contact information for ``OnCall`` entries.
    '''
    STAFF_CHOICES = (
        (0, u'Beamline Staff'),
        (1, u'Students'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, help_text="Four digit extension", blank=True)
    image = models.ImageField(_('image'), blank=True, upload_to=get_storage_path)
    office = models.CharField(blank=True, max_length=50)
    category = models.IntegerField(blank=False, choices=STAFF_CHOICES)
    
    def __unicode__(self):
        """Human readable string for ``SupportPerson``"""
        return '%s, %s' % (self.last_name, self.first_name)

    def initials(self):
        return '%c%c' % (self.first_name[0].upper(), self.last_name[0].upper())    
    
    class Meta:
        unique_together = (
            ("first_name", "last_name", "email"),
            )
        verbose_name_plural = "Personnel"

class VisitManager(models.Manager):
    use_for_related_fields = True
   
    def shift_occurences(self, dt=None, shift=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular shift.
        
        * ``dt`` may be either a datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``shift`` an enumerated item from  ``Visit.SHIFT_CHOICES``.
        '''
        dt = dt or datetime.date(datetime.now())
        qs = self.filter(
            models.Q(
                start_date__lte=dt,
                first_shift__lte=shift,
                last_shift__gte=shift,
                end_date__gte=dt,
            )
        )
        
        return qs
                
    def week_occurences(self, dt=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular week.
        
        * ``dt`` is any date within the week of interest
          ``None``. If ``None``, default to the current week.
        
        * ``shift`` an enumerated item from  ``Visit.SHIFT_CHOICES``.
        '''
        if dt is None:
            dt = datetime.now()
        
        year, week, day = dt.isocalendar()
        d = date(year, 1, 4) # The Jan 4th must be in week 1  according to ISO

        start = d + timedelta(weeks=(week-1), days=-d.weekday())
        end = start + timedelta(days=6)

        qs = self.filter(
            models.Q(
                end_date__gte=start,
                #end_date__lte=end,
            ) |
            models.Q(
                #start_date__gte=start,
                start_date__lte=end,
            )                 
        )
        
        return qs
        

class Visit(models.Model):
    '''
    Represents the start and end time for a specific beamline information for ``OnCall`` entries.
    
    '''
    SHIFT_CHOICES = (
        (0, u'08:00 - 16:00'),
        (1, u'16:00 - 24:00'),
        (2, u'24:00 - 08:00'),
    )
    
    description = models.CharField('Visitor', max_length=60)
    beamline = models.ForeignKey(Beamline)
    start_date = models.DateField(blank=True)
    first_shift = models.IntegerField(blank=True, choices=SHIFT_CHOICES)
    end_date = models.DateField(blank=True)
    last_shift = models.IntegerField(blank=False, choices=SHIFT_CHOICES)
    objects = VisitManager()    

    def __unicode__(self):
        """Human readable string for ``Visit``"""
        return '%s, %s to %s' % (self.description, self.start_date, self.end_date)
    
    def get_shifts(self, dt):
        """Get all shifts for given date"""
        shifts = [None, None, None]
        
        if self.start_date <= dt <= self.end_date:
            day_first = 0
            day_last = 2
            if self.start_date == dt:
                day_first = self.first_shift
            if self.end_date == dt:
                day_last = self.last_shift
            for i in range(day_first, day_last+1):
                shifts[i] = self.description
        
        return shifts
        
    class Meta:
        unique_together = (
            ("beamline", "start_date", "first_shift"),
            ("beamline", "end_date", "last_shift"),
            )
        get_latest_by = "date"
        verbose_name = "Beamline Visit"

   
class OnCallManager(models.Manager):
    use_for_related_fields = True
    
    def week_occurences(self, dt=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular week.
        
        * ``dt`` is any date within the week of interest
          ``None``. If ``None``, default to the current week.
        
        '''
        if dt is None:
            dt = datetime.now()
    
        start = dt - timedelta(days=dt.weekday())
        end = start + timedelta(days=6)

        
        qs = self.filter(
            models.Q(
                date__gte=start,
                date__lte=end,
            )                
        )
        
        return qs

class OnCall(models.Model):
    local_contact = models.ForeignKey(SupportPerson)
    date = models.DateField()
    objects = OnCallManager()
    
    def __unicode__(self):
        """Human readable string for ``Visit``"""
        return '%s, %s' % (self.local_contact.initials(), self.date)
        
    class Meta:
        unique_together = (("local_contact", "date"),)
        get_latest_by = "date"
        verbose_name = "On Call Person"
        verbose_name_plural = "On Call Personnel"


class Mode(models.Model):
    '''
    Basic beamline information for ``Visit`` entries.
    
    '''
    name = models.CharField(blank=False,max_length=30)
#    description = models.CharField(max_length=200)

    def __unicode__(self):
        """Human readable string for Beamline"""
        return self.name        

class StatManager(models.Manager):
    use_for_related_fields = True
   
    def shift_occurences(self, dt=None, shift=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular shift.
        
        * ``dt`` may be either a datetime.date object, or
          ``None``. If ``None``, default to the current day.
        
        * ``shift`` an enumerated item from  ``Visit.SHIFT_CHOICES``.
        '''
        dt = dt or datetime.date(datetime.now())
        qs = self.filter(
            models.Q(
                start_date__lte=dt,
                first_shift__lte=shift,
                last_shift__gte=shift,
                end_date__gte=dt,
            )
        )
        
        return qs
                
    def week_occurences(self, dt=None):
        '''
        Returns a queryset of for instances that have any overlap with a 
        particular week.
        
        * ``dt`` is any date within the week of interest
          ``None``. If ``None``, default to the current week.
        
        * ``shift`` an enumerated item from  ``Visit.SHIFT_CHOICES``.
        '''
        if dt is None:
            dt = datetime.now()
        
        year, week, day = dt.isocalendar()
        d = date(year, 1, 4) # The Jan 4th must be in week 1  according to ISO

        start = d + timedelta(weeks=(week-1), days=-d.weekday())
        end = start + timedelta(days=6)

        qs = self.filter(
            models.Q(
                end_date__gte=start,
                #end_date__lte=end,
            ) |
            models.Q(
                #start_date__gte=start,
                start_date__lte=end,
            )                 
        )
        
        return qs
        

class Stat(models.Model):
    '''
    Represents the start and end time for a specific beamline information for ``OnCall`` entries.
    
    '''
    STATUS_CHOICES = (
	('Maintenance',	'Maintenance Mode'),
	('Shutdown', 	'Shutdown Mode'),
	('Development', 	'Development Mode'),
	('NormalMode', 	'Normal Mode'),
	('Special', 	'Special Request/Commissioning'),
    )
    SHIFT_CHOICES = (
        (0, u'08:00 - 16:00'),
        (1, u'16:00 - 24:00'),
        (2, u'24:00 - 08:00'),
    )
    
#    description = models.CharField('Visitor', max_length=60)
    mode = models.CharField(max_length=60, choices=STATUS_CHOICES)
   # mode = models.ForeignKey(Mode)
    start_date = models.DateField(blank=True)
    first_shift = models.IntegerField(blank=True, choices=SHIFT_CHOICES)
    end_date = models.DateField(blank=True)
    last_shift = models.IntegerField(blank=False, choices=SHIFT_CHOICES)
    objects = VisitManager()    

    def __unicode__(self):
        """Human readable string for ``Visit``"""
        return '%s, %s to %s' % (self.mode, self.start_date, self.end_date)
    
    def get_shifts(self, dt):
        """Get all shifts for given date"""
        shifts = [None, None, None]
        
        if self.start_date <= dt <= self.end_date:
            day_first = 0
            day_last = 2
            if self.start_date == dt:
                day_first = self.first_shift
            if self.end_date == dt:
                day_last = self.last_shift
            for i in range(day_first, day_last+1):
                shifts[i] = self.mode
        
        return shifts
        
    class Meta:
        unique_together = (
            ("mode", "start_date", "first_shift"),
            ("mode", "end_date", "last_shift"),
            )
        get_latest_by = "date"
        verbose_name = "Beamline Status"
	verbose_name_plural = "Beamline Statuses"

