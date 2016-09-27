#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class UploadFileForm(forms.Form):
    LEVEL_CHOICES = (
    ('3', '很低'),
    ('4', '低'),
    ('5', '中'),
    ('6', '高'),
    ('7', '很高'),
    )

    CHANNEL_CHOICES = (
    ('旅游', '旅游'),
    ('科技', '科技'),
    ('汽车', '汽车'),
    ('游戏', '游戏'),
    ('生活', '生活'),
    ('搞笑', '搞笑'),
    ('时尚', '时尚'),
    ('美女', '美女'),
    ('健康', '健康'),
    ('母婴', '母婴'),
    ('教育', '教育'),
    ('体育', '体育'),
    )

    ORIGIN_CHOICES = (
    ('yk', '优酷'),
    ('td', '土豆'),
    ('56', '56'),
    ('k6', '酷6'),
    )

    url = forms.URLField(label='url')
    title = forms.CharField(label='标题')
    tag = forms.CharField(label='标签')
    description = forms.CharField(label='描述')
    level = forms.ChoiceField(label='优先级', choices=LEVEL_CHOICES)
    channel = forms.ChoiceField(label='频道', choices=CHANNEL_CHOICES)
    #origin = forms.ChoiceField(label='来源', choices=ORIGIN_CHOICES)
