# -*- coding: utf-8 -*-

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

#Table to store device metadata for all devices in BEMOSS system
class Daily_Consumption(models.Model):

    date = models.DateField(auto_now=False, auto_now_add=True, primary_key=True)
    gridimportenergy = models.DecimalField(max_digits=19, decimal_places=2)
    gridexportenergy = models.DecimalField(max_digits=19, decimal_places=2)
    solarenergy = models.DecimalField(max_digits=19, decimal_places=2)
    loadenergy = models.DecimalField(max_digits=19, decimal_places=2)
    gridimportbill = models.DecimalField(max_digits=19, decimal_places=2)
    gridexportbill = models.DecimalField(max_digits=19, decimal_places=2)
    solarbill = models.DecimalField(max_digits=19, decimal_places=2)
    loadbill = models.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        db_table = "daily_consumption"

    def __unicode__(self):
        return self.device_id

    # def data_as_json(self):
    #     return dict(
    #         device_id=self.device_id,
    #         device_type=self.device_type.encode('utf-8') if self.device_type else '',
    #         vendor_name=self.vendor_name.encode('utf-8') if self.vendor_name else '',
    #         device_model=self.device_model.encode('utf-8') if self.device_model else '',
    #         device_model_id=self.device_model_id,
    #         mac_address=self.mac_address.encode('utf-8') if self.mac_address else '',
    #         min_range=self.min_range,
    #         max_range=self.max_range,
    #         identifiable=self.identifiable,
    #         date_added=self.date_added,
    #         #bemoss=self.bemoss,
    #         approval_status=self.get_approval_status_display().encode('utf-8') if self.get_approval_status_display() else '',
    #         approval_status_choices=self.APPROVAL_STATUS_CHOICES)
    #
    # def data_dashboard(self):
    #
    #     return dict(
    #         device_id=self.device_id,
    #         device_type=self.device_type.encode('utf-8') if self.device_type else '',
    #         vendor_name=self.vendor_name.encode('utf-8') if self.vendor_name else '',
    #         device_model=self.device_model.encode('utf-8') if self.device_model else '',
    #         device_model_id=self.device_model_id,
    #         mac_address=self.mac_address.encode('utf-8') if self.mac_address else '',
    #         min_range=self.min_range,
    #         max_range=self.max_range,
    #         identifiable=self.identifiable,
    #         #bemoss=self.bemoss,
    #         approval_status=self.approval_status,
    #         approval_status_choices=self.APPROVAL_STATUS_CHOICES)
    #
    # def device_control_page_info(self):
    #     return dict(
    #         device_id=self.device_id,
    #         device_model_id=self.device_model_id,
    #         mac_address=self.mac_address.encode('utf-8') if self.mac_address else '',
    #         device_type=self.device_type.encode('utf-8') if self.device_type else '',
    #         min_range=self.min_range,
    #         max_range=self.max_range,
    #         device_model=self.device_model,
    #         approval_status=self.approval_status)
    #
    # def device_status(self):
    #     return dict(
    #         device_model=self.device_model.encode('utf-8').capitalize() if self.device_model else '',
    #         date_added=self.date_added)
