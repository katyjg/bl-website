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
    #mode_calendar = get_cls_modes()

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

        if day is not None:
            yr = str(day)
        else:
            yr = str(datetime.now().date())
        if WebStatus.objects.filter(date=key.split(' ')[1] + '/' + yr[:4]):
            stat = WebStatus.objects.get(date=key.split(' ')[1] + '/' + yr[:4])
            mode_day.append(stat.status1)
            mode_day.append(stat.status2)
            mode_day.append(stat.status3)
                
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

