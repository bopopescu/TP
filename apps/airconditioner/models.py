# -*- coding: utf-8 -*-
#Database models for Philips Hue and Other Lighting Devices
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.dashboard.models import Building_Zone, DeviceMetadata

#AC device information - for all airconditioner controllers in BEMOSS
class Airconditioner(models.Model):
    airconditioner = models.ForeignKey(DeviceMetadata, primary_key=True, max_length=50)
    status = models.CharField(max_length=3, null=True, blank=True)
    current_temperature = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    set_temperature = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    current_humidity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    set_humidity = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    mode = models.CharField(max_length=15, null=True, blank=True)
    fan_speed = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    fan_angle = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "airconditioner"

    def __unicode__(self):
        return self.airconditioner_id

    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.airconditioner_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.airconditioner_id,
            status=self.status,
            current_temperature=self. current_temperature,
            set_temperature=self.set_temperature,
            current_humidity=self.current_humidity,
            set_humidity=self.set_humidity,
            mode=self.mode,
            fan_speed=self.fan_speed,
            fan_angle=self.fan_angle,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            device_type=metadata['device_type'].encode('utf-8') if metadata['device_type'] else '',
            device_model_id=metadata['device_model_id'],
            identifiable=metadata['identifiable'],
            device_model=metadata['device_model'].encode('utf-8') if metadata['device_model'] else '',
            vendor_name=metadata['vendor_name'].encode('utf-8') if metadata['vendor_name'] else '',
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.airconditioner_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.airconditioner_id,
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            device_model=metadata['device_model'],
            date_added=metadata['date_added'],
            zone=zone_req,
            #bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            last_scanned=self.last_scanned_time,
            last_offline=self.last_offline_time,
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.airconditioner_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.airconditioner_id,
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
        device_info = DeviceMetadata.objects.get(device_id=self.airconditioner_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.airconditioner_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            zone_id=zone_req['id'],
            #bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])