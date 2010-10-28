# Create your views here.

from urllib import quote
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.create_update import delete_object
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.create_update import delete_object
from datetime import datetime, date, timedelta

import datetime
import re
from django.db.models import Q
from django.conf import settings
from tagging.models import Tag, TaggedItem

from scheduler.models import *
from calendar import Calendar, HTMLCalendar

import urllib2
from BeautifulSoup import BeautifulSoup


from django.db.models.signals import post_save



def my_callback(sender, **kwargs):
    print "Request finished!"

post_save.connect(my_callback, sender=Visit)

def save_cls_modes():
    page = urllib2.urlopen("http://www.lightsource.ca/operations/schedule.php")
    soup = BeautifulSoup(page)
    t = soup.find("table", "schedule")
    dat = [ map(str, row.findAll("td")) for row in t.findAll("tr") ]
    mode_calendar = []
    w = 0

    for x in range(len(dat)):
        z = 0
        for y in range(len(dat[w])):
            if dat[w][z].endswith('&nbsp;</td>'):
                dat[w].pop(z)
            else:
                dat[w][z] = dat[w][z].split('>')[1].split('<')[0]
                z += 1
        if dat[w]:
            w += 1
        else:
            dat.pop(w)
    
    for x in range(len(dat)):
        if dat[x][0][2:3] != ':':
            if len(dat[x][0]) > 8:
                for y in range(1,8):
                    if len(dat[x][y]) == 1:
                        month = dat[x][0][:3]
                        dat[x][y] = month + '/0' + dat[x][y]
                    if len(dat[x][y]) == 2:
                        dat[x][y] = month + '/' + dat[x][y]
            else:
                for y in range(0,7):
                    if len(dat[x][y]) == 1:
                        dat[x][y] = '0' + dat[x][y]
                    if month:
                        dat[x][y] = month + '/' + dat[x][y]

    for x in range(len(dat)):
        if len(dat[x]) > 7:
            dat[x].pop(0)
 
    for z in range(len(dat)/4+1):
        for x in range(0,7):
            mode_day = []
            for y in range(0,4):
                mode_day.append(dat[y][x])
            mode_calendar.append(mode_day)
        if z != len(dat)/4:
            for i in range(0,4):
                dat.pop(0)

    
    for x in range(len(mode_calendar)):
        mode_calendar[x][1] = mode_calendar[x][2]
        mode_calendar[x][2] = mode_calendar[x][3]
        if x != len(mode_calendar)-1:
            mode_calendar[x][3] = mode_calendar[x+1][1]

    print mode_calendar

    return mode_calendar

def get_cls_modes():
    page = urllib2.urlopen("http://www.lightsource.ca/operations/schedule.php")
    soup = BeautifulSoup(page)
    t = soup.find("table", "schedule")
    dat = [ map(str, row.findAll("td")) for row in t.findAll("tr") ]
    mode_calendar = []
    dates = []
    w = 0
    stats = WebStatus.objects.all()

    for x in range(len(dat)):
        z = 0
        for y in range(len(dat[w])):
            if dat[w][z].endswith('&nbsp;</td>'):
                dat[w].pop(z)
            else:
                dat[w][z] = dat[w][z].split('>')[1].split('<')[0]
                z += 1
        if dat[w]:
            w += 1
        else:
            dat.pop(w)
    
    month = "Oct"
    year = "2010"
    
    for x in range(len(dat)):
        if dat[x][0][2:3] != ':':
            if len(dat[x][0]) > 8:
                for y in range(1,8):
                    if len(dat[x][y]) == 1:
                        month = dat[x][0][:3]
                        year = dat[x][0][-4:]
                        dat[x][y] = month + '/0' + dat[x][y] + '/' + year
                    if len(dat[x][y]) == 2:
                        dat[x][y] = month + '/' + dat[x][y] + '/' + year
            else:
                for y in range(0,7):
                    if len(dat[x][y]) == 1:
                        dat[x][y] = '0' + dat[x][y]
                    if month:
                        dat[x][y] = month + '/' + dat[x][y] + '/' + year

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
            print "z", z, "x", x, "mode_day[0]", mode_day[0], "dat now is", dat[0][0]
            dates.append(mode_day[0])
            mode_calendar.append(mode_day)
        if x == 6:
            for i in range(0,4):
                dat.pop(0)

    #GONE
    
    for x in range(len(mode_calendar)):
        mode_calendar[x][1] = mode_calendar[x][2]
        mode_calendar[x][2] = mode_calendar[x][3]
        if x != len(mode_calendar)-1:
            mode_calendar[x][3] = mode_calendar[x+1][1]
        day_status = WebStatus(date=dates[x], status1=mode_calendar[x][1], status2=mode_calendar[x][2], status3=mode_calendar[x][3])
        for stat in stats:
            if day_status.date == stat.date:
                no_print = True
        if no_print:
            no_print=False
        else:
            print "Saving...", day_status.date
            day_status.save()

    return mode_calendar


def get_one_week(dt=None):
    if dt is None:
        dt = datetime.now().date()
        
    # start on first day of week
    wk_dt = dt - timedelta(days=dt.weekday())
    week = [wk_dt]
    for i in range(6):
        wk_dt = wk_dt + timedelta(days=1)
        week.append( wk_dt )
    return week
        
def combine_shifts(shifts):
    new_shifts = [[],[],[]]
    for shift in shifts:
        for i in range(3):
            if shift[i] is not None:
                new_shifts[i].append(shift[i])
    for i in range(3):
        new_shifts[i] = ','.join(new_shifts[i])
    
    return new_shifts
            
    
def current_week(request, day=None):

    if day is not None:
        dt = datetime.strptime(day, '%Y-%m-%d').date()
    else:
        dt = datetime.now().date()
        
    this_wk = get_one_week(dt)
    prev_wk_day = (dt + timedelta(weeks=-1)).strftime('%Y-%m-%d')
    next_wk_day = (dt + timedelta(weeks=1)).strftime('%Y-%m-%d')
    
    calendar = []    
    bl_keys = []
    mode_keys = []
    bl_week = {}
    mode_week = {}
    beamlines = Beamline.objects.all()
    week_personnel = OnCall.objects.week_occurences(dt)
    modes = Stat.objects.all()
    mode_calendar = get_cls_modes()

    for bl in beamlines:
        bl_week[bl.name] = bl.visit_set.week_occurences(dt)
        bl_keys.append(bl.name)
    
    for day in this_wk:
        key = day.strftime('%a %b/%d')
        shifts = {}
	mode_shifts = []
	beammode = []

	for current_mode in modes:
	    beammode.append(current_mode.get_shifts(day))

	mode_shifts.append(combine_shifts(beammode))
        for blkey, blvis in bl_week.items():
            shifts[blkey] = []

            for vis in blvis:
                shifts[blkey].append(vis.get_shifts(day))

        day_shifts = []
        for blkey in bl_keys:
            day_shifts.append(combine_shifts(shifts[blkey]))

        on_call = ','.join([o.local_contact.initials() for o in week_personnel if o.date == day])
        mode_day = []

        found = False

        for x in range(len(mode_calendar)):
            if mode_calendar[x][0][:6] == key.split(' ')[1]:
                mode_day = mode_calendar[x][1:]
                found = True
        if found == False:
            mode_day = []
            for stat in WebStatus.objects.all():
                if key.split(' ')[1] == stat.date[:6]:
                    mode_day.append(stat.status1)
                    mode_day.append(stat.status2)
                    mode_day.append(stat.status3)
        
        print mode_day
        calendar.append((key, day_shifts, on_call, mode_shifts, mode_day))

    return render_to_response(
        'scheduler/schedule_week.html', 
        {
            'beamlines': beamlines,
            'calendar': calendar,
            'next_week': next_wk_day,
            'prev_week': prev_wk_day,
        },
        context_instance=RequestContext(request),
    )
    
def contact_legend(request):
    support_list = []
    for person in SupportPerson.objects.all():
            support_list.append(person)

    return render_to_response(     
   	'contacts/contact_legend.html', 
        {'contact_list': support_list},
        )

def contact_list(request):
    support_list = []
    categories = []
    for category in SupportPerson.STAFF_CHOICES:
        categories.append(category)
    for person in SupportPerson.objects.all():
            support_list.append(person)

    return render_to_response(     
   	'contacts/contact_list.html', 
        {
            'contact_list': support_list,
            'categories': categories,
        },
        )

