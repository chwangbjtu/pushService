#!/bin/env python
# coding=utf-8

from django.db import models

class Door(models.Model):
    class Meta:
        app_label = "ugc"
        permissions = (
                       ("can_operate_audit_space","Can_view_and_operate_its_video"),
                       ("can_access_manage_space","Can_access_managment_workspace"),
                       ("can_access_global_space","Can_access_global_workspace"),
                       ("can_operate_forwards","Can_operate_forwards"),
                       ("can_operate_upload","Can_operate_upload"),
        )
        managed=False