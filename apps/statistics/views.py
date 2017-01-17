# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.shortcuts import render_to_response
from _utils import page_load_utils as _helper
from agents.ZMQHelper.zmq_pub import ZMQ_PUB
from _utils.page_load_utils import get_device_list_side_navigation
from apps.alerts.views import get_notifications, general_notifications
from apps.dashboard.models import DeviceMetadata
from apps.lighting.models import Lighting
import json
import psycopg2
import _utils.defaults as __
from apps.statistics.models import Daily_Consumption
from decimal import Decimal

kwargs = {'subscribe_address': __.SUB_SOCKET,
          'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)

def energy_and_bill_database(start_date, end_date, remaining_day):
    energy_and_bill = Daily_Consumption.objects.values_list('gridimportenergy', 'solarenergy', 'gridimportbill',
                                                            'solarbill').filter(date__range=(start_date, end_date))
    gridimportenergy = []
    solarenergy = []
    gridimportbill = []
    solarbill = []
    for i in range(len(energy_and_bill)):
        gridimportenergy.append(float(energy_and_bill[i][0]))
        solarenergy.append(float(energy_and_bill[i][1]))
        gridimportbill.append(float(energy_and_bill[i][2]))
        solarbill.append(float(energy_and_bill[i][3]))
    gridimportenergy.extend([0] * remaining_day)
    solarenergy.extend([0] * remaining_day)
    gridimportbill.extend([0] * remaining_day)
    solarbill.extend([0] * remaining_day)

    return [gridimportenergy, solarenergy, gridimportbill, solarbill]

# Functionality for lighting page load
@login_required(login_url='/login/')
def source_statistics(request):
    print 'inside source_statistics view method'
    context = RequestContext(request)
    username = request.session.get('user')
    print username
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1

    today = datetime.now().date()
    weekday_today = today.weekday()
    remaining_day = 6 - weekday_today
    start_date = today - timedelta(days=weekday_today)
    energy_and_bill_daily = energy_and_bill_database(start_date, today, remaining_day)

    end_week_3 = start_date - timedelta(days=1)
    start_week_3 = end_week_3 - timedelta(days=6)
    end_week_2 = start_week_3 - timedelta(days=1)
    start_week_2 = end_week_2 - timedelta(days=6)
    end_week_1 = start_week_2 - timedelta(days=1)
    start_week_1 = end_week_1 - timedelta(days=6)
    energy_and_bill_week_1 = energy_and_bill_database(start_week_1, end_week_1, 0)
    energy_and_bill_week_2 = energy_and_bill_database(start_week_2, end_week_2, 0)
    energy_and_bill_week_3 = energy_and_bill_database(start_week_3, end_week_3, 0)
    gridimportenergy_week = [sum(energy_and_bill_week_1[0]), sum(energy_and_bill_week_2[0]), sum(energy_and_bill_week_3[0]), sum(energy_and_bill_daily[0])]
    solarenergy_week = [sum(energy_and_bill_week_1[1]), sum(energy_and_bill_week_2[1]), sum(energy_and_bill_week_3[1]), sum(energy_and_bill_daily[1])]
    gridimportbill_week = [sum(energy_and_bill_week_1[2]), sum(energy_and_bill_week_2[2]), sum(energy_and_bill_week_3[2]), sum(energy_and_bill_daily[2])]
    solarbill_week = [sum(energy_and_bill_week_1[3]), sum(energy_and_bill_week_2[3]), sum(energy_and_bill_week_3[3]), sum(energy_and_bill_daily[3])]

    this_month = today.month
    first_date_this_month = today.replace(day=1)
    remaining_month = 12 - this_month
    energy_and_bill_this_month = energy_and_bill_database(first_date_this_month, today, 0)
    gridimportenergy_month = []
    solarenergy_month = []
    gridimportbill_month = []
    solarbill_month = []
    for i in range(1, this_month):
        first_date_of_month = today.replace(month=i)
        end_date_of_month = first_date_of_month + relativedelta(day=31)
        energy_and_bill_of_month = energy_and_bill_database(first_date_of_month, end_date_of_month, 0)
        gridimportenergy_month.append(round(sum(energy_and_bill_of_month[0]), 2))
        solarenergy_month.append(round(sum(energy_and_bill_of_month[1]), 2))
        gridimportbill_month.append(round(sum(energy_and_bill_of_month[2]), 2))
        solarbill_month.append(round(sum(energy_and_bill_of_month[3]), 2))
    gridimportenergy_month.append(round(sum(energy_and_bill_this_month[0]), 2))
    solarenergy_month.append(round(sum(energy_and_bill_this_month[1]), 2))
    gridimportbill_month.append(round(sum(energy_and_bill_this_month[2]), 2))
    solarbill_month.append(round(sum(energy_and_bill_this_month[3]), 2))
    gridimportenergy_month.extend([0] * remaining_month)
    solarenergy_month.extend([0] * remaining_month)
    gridimportbill_month.extend([0] * remaining_month)
    solarbill_month.extend([0] * remaining_month)


    return render_to_response(
        'statistics/statistics_all.html',
        # {'type': controller_type, 'device_data': _data, 'device_id': device_id, 'device_zone': device_zone,
        #  'device_type': controller_type, 'mac_address': mac, 'zone_nickname': zone_nickname,
        #  'device_nickname': device_nickname}, context)
        {'type': "source", 'gridimportenergy': energy_and_bill_daily[0], 'solarenergy': energy_and_bill_daily[1],
         'gridimportbill': energy_and_bill_daily[2], 'solarbill': energy_and_bill_daily[3],
         'gridimportenergyweek': gridimportenergy_week, 'solarenergyweek': solarenergy_week,
         'gridimportbillweek': gridimportbill_week, 'solarbillweek': solarbill_week,
         'gridimportenergymonth': gridimportenergy_month, 'solarenergymonth': solarenergy_month,
         'gridimportbillmonth': gridimportbill_month, 'solarbillmonth': solarbill_month}, context)
        # {'type': "source"}, context)

def load_statistics(request):
    print 'inside load_statistics view method'
    context = RequestContext(request)
    username = request.session.get('user')
    print username
    if request.session.get('last_visit'):
        # The session has a value for the last visit
        last_visit_time = request.session.get('last_visit')

        visits = request.session.get('visits', 0)

        if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
            request.session['visits'] = visits + 1
    else:
        # The get returns None, and the session does not have a value for the last visit.
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1


    return render_to_response(
        'statistics/statistics_load.html',
        # {'type': controller_type, 'device_data': _data, 'device_id': device_id, 'device_zone': device_zone,
        #  'device_type': controller_type, 'mac_address': mac, 'zone_nickname': zone_nickname,
        #  'device_nickname': device_nickname}, context)
        {'type': "load"}, context)