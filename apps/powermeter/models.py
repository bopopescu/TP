# -*- coding: utf-8 -*-
from django.db import models
from apps.dashboard.models import Building_Zone, DeviceMetadata

#powermeter device information - for all powermeter controllers in BEMOSS
class Powermeter(models.Model):
    powermeter = models.ForeignKey(DeviceMetadata, primary_key=True, max_length=50)
    status = models.CharField(max_length=3, null=True, blank=True)
    power = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "powermeter"

    def __unicode__(self):
        return self.powermeter_id

    def get_zone(self):
        zone_req = Building_Zone.as_json(self.zone)
        return zone_req

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.powermeter_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.powermeter_id,
            status=self.status,
            power=self.power,
            energy=self.energy,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            device_type=metadata['device_type'].encode('utf-8') if metadata['device_type'] else '',
            device_model_id=metadata['device_model_id'],
            # bemoss=metadata['bemoss'],
            identifiable=metadata['identifiable'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            vendor_name=metadata['vendor_name'].encode('utf-8') if metadata['vendor_name'] else '',
            device_model=metadata['device_model'].encode('utf-8') if metadata['device_model'] else '',
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.powermeter_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.powermeter_id,
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            #bemoss=metadata['bemoss'],
            network_status=self.network_status.capitalize(),
            zone_nickname=zone_req['zone_nickname'],
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time,
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.powermeter_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.powermeter_id,
            device_type=metadata['device_type'].encode('utf-8') if metadata['device_type'] else '',
            vendor_name=metadata['vendor_name'].encode('utf-8') if metadata['vendor_name'] else '',
            device_model=metadata['device_model'].encode('utf-8') if metadata['device_model'] else '',
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            date_added=metadata['date_added'],
            identifiable=metadata['identifiable'],
            zone_id=zone_req['id'],
            #bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.powermeter_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.powermeter_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            zone_id=zone_req['id'],
            #bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])


