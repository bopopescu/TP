# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from _utils.page_load_utils import get_device_list_side_navigation
from apps.alerts.views import get_notifications, general_notifications
from apps.dashboard.models import DeviceMetadata
from apps.powermeter.models import Powermeter
from agents.ZMQHelper.zmq_pub import ZMQ_PUB
from _utils import page_load_utils as _helper
import json

from _utils import defaults as __

kwargs = {'subscribe_address': __.SUB_SOCKET, 'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)

@login_required(login_url='/login/')
def powermeter(request, mac):
    print 'inside powermeter view method'
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

    mac = mac.encode('ascii', 'ignore')
    print "unside powermeter view for mac: {}".format(mac)

    # device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    # print device_metadata
    # device_id = device_metadata[0]['device_id']
    # device_type_id = device_metadata[0]['device_model_id']
    # device_type_id = device_type_id.device_model_id
    #
    # device_status = [ob.data_as_json() for ob in Plugload.objects.filter(plugload_id=device_id)]
    # device_zone = device_status[0]['zone']['id']
    # device_nickname = device_status[0]['nickname']
    # zone_nickname = device_status[0]['zone']['zone_nickname']
    #
    # _data = _helper.get_page_load_data(device_id, 'plugload', device_type_id)
    #
    # device_list_side_nav = get_device_list_side_navigation()
    # context.update(device_list_side_nav)
    # active_al = get_notifications()
    # context.update({'active_al':active_al})
    # bemoss_not = general_notifications()
    # context.update({'b_al': bemoss_not})

    return render_to_response(
        'powermeter/powermeter.html',
        # {'device_data': _data, 'device_id': device_id, 'device_zone': device_zone, 'zone_nickname': zone_nickname,
        #  'mac_address': mac, 'device_nickname': device_nickname, 'device_type_id': device_type_id},
        # context)
        {'device_type': "powermeter"},
        context)

@login_required(login_url='/login/')
def submit_changes(request):
    print 'inside powermeter update device method'
    if request.POST:
        _data = request.body
        print _data
        _data = json.loads(_data)
        print _data

        device_info = _data['device_info']
        #_data = {"status": _data['status']}
        _data.pop('device_info')
        print _data
        print device_info
        content_type = "application/json"
        fromUI = "UI"
        print "created instance of the zmqpub class"

        #device_info = device_info.split('/')  # e.g. 999/lighting/1NST18b43017e76a
        # TODO fix building name -> should be changeable from 'bemoss'
        powermeter_update_send_topic = '/ui/agent/'+device_info[1]+'/update/bemoss/'+device_info[0]+'/'+device_info[2]
        print powermeter_update_send_topic
        zmq_pub.sendToAgent(powermeter_update_send_topic, _data, content_type, fromUI)
        print "success in sending message to agent"

    if request.is_ajax():
            return HttpResponse(json.dumps(_data), mimetype='application/json')

def get_powermeter_current_status(request):
    print "getting current status of powermeter"
    if request.method == 'POST':
        data_recv = request.body
        data_recv = json.loads(data_recv)
        device_info = data_recv['device_info']
        # same as the thermostat load method
        print "created instance of the zmqpub class"

        info_required = "Update powermeter data"

        #device_info = device_info.split('/')  # e.g. 999/lighting/1NST18b43017e76a
        # TODO fix building name -> should be changeable from 'bemoss'
        powermeter_update_send_topic = '/ui/agent/'+device_info[1]+'/device_status/bemoss/'+device_info[0]+'/'+device_info[2]
        print powermeter_update_send_topic

        zmq_pub.requestAgent(powermeter_update_send_topic, info_required, "text/plain", "UI")
        jsonresult = {'status': 'sent'}
        if request.is_ajax():
            return HttpResponse(json.dumps(jsonresult), mimetype='application/json')
