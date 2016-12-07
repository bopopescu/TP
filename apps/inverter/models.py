# -*- coding: utf-8 -*-

# Database models for inverter
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.dashboard.models import Building_Zone, DeviceMetadata

# Inverter information
class Inverter(models.Model):
    inverter = models.ForeignKey(DeviceMetadata, primary_key=True, max_length=50)

    # Grid
    grid_voltage = models.FloatField(null=True, blank=True)
    grid_current = models.FloatField(null=True, blank=True)
    grid_activepower = models.FloatField(null=True, blank=True)
    grid_reactivepower = models.FloatField(null=True, blank=True)
    grid_apparentpower = models.FloatField(null=True, blank=True)

    # Load
    load_voltage = models.FloatField(null=True, blank=True)
    load_current = models.FloatField(null=True, blank=True)
    load_activepower = models.FloatField(null=True, blank=True)
    load_reactivepower = models.FloatField(null=True, blank=True)
    load_apparentpower = models.FloatField(null=True, blank=True)

    # Inverter = Solar + Battery
    inverter_voltage = models.FloatField(null=True, blank=True)
    inverter_current = models.FloatField(null=True, blank=True)
    inverter_activepower = models.FloatField(null=True, blank=True)
    inverter_reactivepower = models.FloatField(null=True, blank=True)
    inverter_apparentpower = models.FloatField(null=True, blank=True)

    # Other parameters
    energy_use_mode = models.PositiveIntegerField(null=True, blank=True)
    battery_voltage = models.FloatField(null=True, blank=True)
    battery_power = models.FloatField(null=True, blank=True)
    battery_low_return_voltage = models.FloatField(null=True, blank=True)

    # accumulated parameters
    accumulated_pv_sell_power = models.FloatField(null=True, blank=True)
    accumulated_discharge_power = models.FloatField(null=True, blank=True)
    accumulated_sell_power = models.FloatField(null=True, blank=True)
    accumulated_charger_power = models.FloatField(null=True, blank=True)
    accumulated_buy_power = models.FloatField(null=True, blank=True)
    accumulated_load_power = models.FloatField(null=True, blank=True)
    accumulated_self_use_power = models.FloatField(null=True, blank=True)
    accumulated_grid_charger_power = models.FloatField(null=True, blank=True)

    # specific parameters
    ip_address = models.IPAddressField(null=True, blank=True)
    nickname = models.CharField(max_length=30, null=True, blank=True)
    zone = models.ForeignKey(Building_Zone, null=True, blank=True)
    network_status = models.CharField(max_length=7, null=True, blank=True)
    other_parameters = models.CharField(max_length=200, null=True, blank=True)
    last_scanned_time = models.DateTimeField(null=True, blank=True)
    last_offline_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "inverter"

    def __unicode__(self):
        return self.inverter_id

    # TODO has to revise this method
    def data_as_json(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.lighting_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.lighting_id,
            status=self.status,
            brightness=self.brightness,
            color=self.color,
            multiple_on_off=self.multiple_on_off,
            zone=zone_req,
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            device_type=metadata['device_type'].encode('utf-8') if metadata['device_type'] else '',
            device_model_id=metadata['device_model_id'],
            identifiable=metadata['identifiable'],
            device_model=metadata['device_model'].encode('utf-8') if metadata['device_model'] else '',
            vendor_name=metadata['vendor_name'].encode('utf-8') if metadata['vendor_name'] else '',
            # bemoss=metadata['bemoss'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])

    # TODO has to revise this method
    def device_status(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.lighting_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            id=self.lighting_id,
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

    # TODO has to revise this method
    def data_dashboard(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.lighting_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.lighting_id,
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

    # TODO has to revise this method
    def data_side_nav(self):
        zone_req = Building_Zone.as_json(self.zone)
        device_info = DeviceMetadata.objects.get(device_id=self.lighting_id)
        metadata = DeviceMetadata.data_as_json(device_info)
        return dict(
            device_id=self.lighting_id,
            device_model_id=metadata['device_model_id'],
            mac_address=metadata['mac_address'].encode('utf-8') if metadata['mac_address'] else '',
            nickname=self.nickname.encode('utf-8').title() if self.nickname else '',
            zone_id=zone_req['id'],
            #bemoss=metadata['bemoss'],
            zone_nickname=zone_req['zone_nickname'],
            network_status=self.network_status.capitalize(),
            approval_status=metadata['approval_status'],
            approval_status_choices=metadata['approval_status_choices'])