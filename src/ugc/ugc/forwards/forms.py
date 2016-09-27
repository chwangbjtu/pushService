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
    ('美女', '美女'),
    ('搞笑', '搞笑'),
    ('娱乐', '娱乐'),
    ('游戏', '游戏'),
    ('体育', '体育'),
    ('汽车', '汽车'),
    ('科技', '科技'), 
    ('军事', '军事'),
    ('音乐', '音乐'),
    ('生活', '生活'),
    ('时尚', '时尚'),
    ('旅游', '旅游'),
    ('母婴', '母婴'),
    ('健康', '健康'),
    ('公开课', '公开课'),
    ('纪录片', '纪录片'),
    ('广告', '广告'),
    ('微电影', '微电影'),
    ('广场舞', '广场舞'),
    ('生活百科', '生活百科'),
    ('电影片花', '电影片花'),
    ('电视片花', '电视片花'),
    ('综艺片花', '综艺片花'),
    ('动漫片花', '动漫片花'),
    ('片花', '片花'),
    #('新闻', '新闻'),
    #('资讯', '资讯'),
    #('拍客', '拍客'),
    #('第一财经', '第一财经'),
    #('美容', '美容'),
    #('婚嫁', '婚嫁'),
    #('美食', '美食'),
    #('宠物', '宠物'),
    #('达人', '达人'),
    #('舞蹈', '舞蹈'),
    #('原创', '原创'),
    #('相声', '相声'),
    #('明星', '明星'),
    #('网剧', '网剧'),
    )

    ORIGIN_CHOICES = (
    ('yk', '优酷'),
    ('td', '土豆'),
    ('56', '56'),
    ('k6', '酷6'),
    )

    single = forms.CharField(label='single', widget=forms.HiddenInput(), required=False)
    url = forms.URLField(label='url')
    title = forms.CharField(label='标题')
    tag = forms.CharField(label='标签')
    description = forms.CharField(label='描述', widget=forms.Textarea)
    level = forms.ChoiceField(label='优先级', choices=LEVEL_CHOICES)
    channel = forms.ChoiceField(label='频道', choices=CHANNEL_CHOICES)
    #origin = forms.ChoiceField(label='来源', choices=ORIGIN_CHOICES)
class BatchForwardForm(forms.Form):
    LEVEL_CHOICES = (
    ('3', '很低'),
    ('4', '低'),
    ('5', '中'),
    ('6', '高'),
    ('7', '很高'),
    )
    batch = forms.CharField(label='batch', widget=forms.HiddenInput(), required=False)
    level = forms.ChoiceField(label='优先级', choices=LEVEL_CHOICES)
    links = forms.CharField(label='链接列表', widget=forms.Textarea, required=True)
    
    #origin = forms.ChoiceField(label='来源', choices=ORIGIN_CHOICES)
