# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render_to_response
from _utils import page_load_utils as _helper
from agents.ZMQHelper.zmq_pub import ZMQ_PUB
from _utils.page_load_utils import get_device_list_side_navigation
from apps.alerts.views import get_notifications, general_notifications
from apps.dashboard.models import DeviceMetadata
from apps.lighting.models import Lighting
from apps.airconditioner.models import Airconditioner
import json
import _utils.defaults as __

kwargs = {'subscribe_address': __.SUB_SOCKET,
          'publish_address': __.PUSH_SOCKET}

zmq_pub = ZMQ_PUB(**kwargs)

# Functionality for lighting page load
@login_required(login_url='/login/')
def airconditioner(request, mac):
    print 'inside airconditioner view method'
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
    print "air conditioner view for mac: {}".format(mac)

    # device_metadata = [ob.device_control_page_info() for ob in DeviceMetadata.objects.filter(mac_address=mac)]
    # print "device_metadata: {}".format(device_metadata)
    # device_id = device_metadata[0]['device_id']
    # controller_type = device_metadata[0]['device_model_id']
    # controller_type = controller_type.device_model_id
    #
    # device_status = [ob.data_as_json() for ob in Airconditioner.objects.filter(lighting_id=device_id)]
    # device_zone = device_status[0]['zone']['id']
    # device_nickname = device_status[0]['nickname']
    # zone_nickname = device_status[0]['zone']['zone_nickname']
    #
    # _data = _helper.get_page_load_data(device_id, 'airconditioner', controller_type)
    #
    # device_list_side_nav = get_device_list_side_navigation()
    # context.update(device_list_side_nav)
    # active_al = get_notifications()
    # context.update({'active_al': active_al})
    # bemoss_not = general_notifications()
    # context.update({'b_al': bemoss_not})

    # TODO add air to database
    return render_to_response(
        'airconditioner/airconditioner.html',
        # {'type': controller_type, 'device_data': _data, 'device_id': device_id, 'device_zone': device_zone,
        #  'device_type': controller_type, 'mac_address': mac, 'zone_nickname': zone_nickname,
        #  'device_nickname': device_nickname}, context)
        {'type': "airconditioner", 'mac_address': mac}, context)

# Update lighting controller status
@login_required(login_url='/login/')
def update_device_air(request):
    print 'inside Aircond update device method'
    if request.POST:
        _data = request.body
        _data = json.loads(_data)
        device_info = _data['device_info']
        if 'color' in str(_data):
            lt_color = _data['color']
            if 'a(' in str(lt_color):
                lt_color = '(0,0,0)'
            try:
                lt_color = eval(lt_color)
            except:
                lt_color = '(0,0,0)'
            _data['color'] = lt_color

        _data.pop('device_info')
        content_type = "application/json"
        fromUI = "UI"
        print(device_info)
        # print(type(device_info))
        # device_info = device_info.split('/')  # e.g. 999/lighting/1NST18b43017e76a
        # TODO fix building name -> should be changeable from 'bemoss'
        lighting_update_send_topic = '/ui/agent/' + device_info[1] + '/update/bemoss/' + device_info[0] + '/1TH' + device_info[2]
        print lighting_update_send_topic
        _data['actor'] = 'ui'
        print _data
        zmq_pub.sendToAgent(lighting_update_send_topic, _data, content_type, fromUI)

    if request.is_ajax():
        return HttpResponse(json.dumps(_data), mimetype='application/json')


@login_required(login_url='/login/')
def get_lighting_current_status(request):
    print "Getting current status of thermostat"
    if request.method == 'POST':
        data_recv = request.body
        data_recv = json.loads(data_recv)
        device_info = data_recv['device_info']
        # same as the thermostat load method
        info_required = "current status"

        device_info = device_info.split('/')  # e.g. 999/lighting/1NST18b43017e76a
        # TODO fix building name -> should be changeable from 'bemoss'
        lighting_update_send_topic = '/ui/agent/' + device_info[1] + '/device_status/bemoss/' + device_info[0] + '/' + \
                                     device_info[2]
        print lighting_update_send_topic

        zmq_pub.requestAgent(lighting_update_send_topic, info_required, "text/plain", "UI")
        json_result = {'status': 'sent'}

        if request.is_ajax():
            return HttpResponse(json.dumps(json_result), mimetype='application/json')