from django.db import models
from dateutil import rrule
from datetime import datetime, date, timedelta
from django.utils.translation import ugettext_lazy as _
import os
from django.conf import settings

from jsonfield import JSONField
#import django.dispatch

from feincms.content.image.models import ImageContent
import ImageFile

import urllib2
from BeautifulSoup import BeautifulSoup
from django.db.models.signals import post_save



def get_storage_path(instance, filename):
    return os.path.join('uploads/contacts/', 'photos', filename)

#cls_modes = django.dispatch.Signal(providing_args=["year", "week"])

def cls(**kwargs):
    '''
        Dec/07/2011 - To use this function, save the year-long beam mode spreadsheet
        from the intranet as a .csv (comma separated) file. Strip the header info (including
        the first line with the days of the week).  Change year.

        TODO: read in year from header info.
    '''
    year = 2012
    f = open('/users/kathryn/Documents/CopyofRun_Schedule_2012.csv')
    data = f.read()
    dat = []
        
    for row in data.split('\n'):
        dat.append(row.split(','))

    mode_calendar = []
    dates = []
    w = 0

    for x in range(len(dat)):
        try:
            if len(dat[x]) is not 8:
                dat.pop(x)
        except IndexError:
            pass

    for x in range(len(dat)/4):
        for x in range(1,8):
            if dat[0][x]:
                day = dat[0][x].split('-')[0].replace(' ','')
                if len(day) is 1:
                    day = '0' + day
                date = '%s/%s/%s' % (dat[0][x].split('-')[1].replace(' ','')[:3], day, str(year))
                mode_calendar.append([date, dat[1][x], dat[2][x], dat[3][x]])
        for x in range(4):
            dat.pop(0)
    
    no_print = False
    
    for x in range(len(mode_calendar)):
        status1 = mode_calendar[x][2][:min(mode_calendar[x][2],2)]
        status2 = mode_calendar[x][3][:min(mode_calendar[x][3],2)]
        try:
            status3 = mode_calendar[x+1][1][:min(mode_calendar[x+1][1],2)]
        except IndexError:
            status3 = ''
        day_status = WebStatus(date=mode_calendar[x][0], status1=status1, status2=status2, status3=status3)
        if WebStatus.objects.filter(date=day_status.date):
            no_print = True
        if no_print:
            no_print=False
        else:
            print "Saving...", day_status.date, status1, status2, status3
            day_status.save()

    return mode_calendar


def get_cls_modes(sender, **kwargs):
    ''' Read the schedule table from the CLS website, and save the information there into 
        the database.  This can be set up as a post_save function.  After every manual 
        Status is saved, new modes will be updated if they are available.
    '''

    page = urllib2.urlopen("http://www.lightsource.ca/operations/schedule.php")
    soup = BeautifulSoup(page)
    t = soup.find("table", "excel1")
    dat = [ map(str, row.findAll("td")) for row in t.findAll("tr") ]
    mode_calendar = []
    dates = []
    w = 0

    # Strip empty and formatting rows
    for x in range(len(dat)):
        z = 0
        for y in range(len(dat[w])):
            if dat[w][z].endswith('&nbsp;</td>'):
                dat[w].pop(z)
            else:
                dat[w][z] = ' '.join(' '.join(dat[w][z].split('>')[1:]).split('<')[:-1])
                z += 1
        if dat[w]:
            w += 1
        else:
            dat.pop(w)

    if dat[0][0][:2] == 'Su':   
        dat.pop(0)

    month = "Jan"
    year = "1999"

    # get initial month and year from the table
    for i in range(0, len(dat)):
        if dat[i][0][0] not in [0,1,2,3,4,5,6,7,8,9]:
            month = dat[i][0].split(" ")[0][:3]
            year = dat[i][0].split(" ")[-1][-4:]
            break

    x = 0
    while x is not len(dat):
        if len(dat[x]) < 7:
            dat.pop(x)
        else:
            empty = True
            for y in range(len(dat[x])):
                if len(dat[x][y]):
                    empty = False
            if empty:
                dat.pop(x)
            else:
                x = x+1

    for x in range(len(dat)):
        if dat[x][0][2:3] != ':':
            if len(dat[x][0]) > 8:
                for y in range(1,8):
                    if len(dat[x][y]) == 1:
                        month = dat[x][0][:3]
                        year = dat[x][0][-4:]
                        dat[x][y] = month + '/0' + dat[x][y].split(' ')[0] + '/' + year
                    if len(dat[x][y]) == 2:
                        dat[x][y] = month + '/' + dat[x][y].split(' ')[0] + '/' + year
            else:
                for y in range(len(dat[x])):
                    if len(dat[x][y]) == 1:
                        dat[x][y] = '0' + dat[x][y]
                    if month:
                        dat[x][y] = month + '/' + dat[x][y].split(' ')[0] + '/' + year

    for x in range(len(dat)):
        if len(dat[x]) > 7:
            dat[x].pop(0)

    no_print = False
    
    #GOOD
            
    for z in range(len(dat)/4):
        for x in range(0,7):
            mode_day = []
            for y in range(0,4):
                mode_day.append(dat[y][x])
            dates.append(mode_day[0])
            mode_calendar.append(mode_day)
        if x == 6:
            for i in range(0,4):
                dat.pop(0)

    for x in range(len(mode_calendar)):
        mode_calendar[x][1] = mode_calendar[x][2]
        mode_calendar[x][2] = mode_calendar[x][3]
        if x != len(mode_calendar)-1:
            mode_calendar[x][3] = mode_calendar[x+1][1]
        day_status = WebStatus(date=dates[x], status1=mode_calendar[x][1], status2=mode_calendar[x][2], status3=mode_calendar[x][3])
        if WebStatus.objects.filter(date=day_status.date):
            no_print = True
        if no_print:
            #print "Skipping", day_status.date
            no_print=False
        else:
            #print "Saving...", day_status.date
            day_status.save()

    return mode_calendar


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
        (1, u'Students and Postdocs'),
        (2, u'CLS Technical Support'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, help_text="Seven digit number", blank=True)
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
    HELP = {
        'description': "Should include a name and proposal number in this format: Bruce Wayne (12-3456).  This information will be given to the User's Office.",
        'mail_in': "If selected, a symbol indicating mail-in access will be displayed along with the user's last name.",
        'purchased': "If selected, only 'Purchased Access' will appear on the public CMCF schedule.",
        'remote': "If selected, a symbol indicating remote access will be displayed along with the user's last name.",
        'maintenance': "If selected, the beamline mode (colour) on the public CMCF schedule will indicate maintenance activities." 
    }
    
    SHIFT_CHOICES = (
        (0, u'08:00 - 16:00'),
        (1, u'16:00 - 24:00'),
        (2, u'24:00 - 08:00'),
    )
    
    description = models.CharField('Visitor and Proposal Number (eg. John Doe (#14-5290))', max_length=60)
    beamline = models.ForeignKey(Beamline)
    start_date = models.DateField(blank=True, null=False)
    first_shift = models.IntegerField(blank=True, choices=SHIFT_CHOICES, null=False)
    end_date = models.DateField(blank=True, null=False)
    last_shift = models.IntegerField(blank=True, choices=SHIFT_CHOICES, null=False)
    remote = models.BooleanField(default=False)
    mail_in = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)  
    objects = VisitManager()    

    def __unicode__(self):
        """Human readable string for ``Visit``"""
        return '%s, %s to %s' % (self.description, self.start_date, self.end_date)
    
    def get_shifts(self, dt, ids=False):
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
                if ids:
                    shifts[i] = [self.description, self]
                else:
                    shifts[i] = self.description
        return shifts
    
    def parse_name(self):
        try:
            return [self.description.split('(')[0], self.description.split('(')[1].split(')')[0]]
        except:
            return [self.description, None]

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
        
    def initials(self):
        return self.local_contact.initials()
    
    class Meta:
        unique_together = (("local_contact", "date"),)
        get_latest_by = "date"
        verbose_name = "On Call Person"
        verbose_name_plural = "On Call Personnel"

class WebStatus(models.Model):
    date = models.CharField(max_length=15, default='')
    status1 = models.CharField(max_length=10, default='')
    status2 = models.CharField(max_length=10, default='')
    status3 = models.CharField(max_length=10, default='')

    class Meta:
        unique_together = (("date"),)
        verbose_name = "Upload CLS Beam Mode"

class Stat(models.Model):
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
    
    mode = models.CharField(max_length=60, choices=STATUS_CHOICES)
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
        verbose_name = "Beamline Status (to override CLS status)"
	verbose_name_plural = "Beamline Statuses (override CLS status)"

post_save.send(sender=Stat)
post_save.connect(get_cls_modes, sender=Stat)













