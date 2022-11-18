#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   icsying@outlook.com
@Time    :   2022-11-18 20:44:52
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   get ip from ip address
'''

import requests
from bs4 import BeautifulSoup
import re, json

REGISTRY_IP = dict()
ECHO = False


def register(name):
    def _thunk(func):
        REGISTRY_IP[name] = func
        return func

    return _thunk


@register("ipaddress")
def getIpFromIpaddress(site):
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Host': 'www.ipaddress.com'
    }
    url = "https://ipaddress.com/site/" + site
    trueip = list()
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find(
            'table',
            class_="panel-item table table-border-row table-v faq").find_all(
                "div")
        for ipv4s in filter(lambda tag: "IPv4" in tag.text, table):
            ips = ipv4s.find_all("strong")
            for ip in ips:
                tmp = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", ip.text)
                if tmp:
                    trueip = tmp[0]
                    break
    except Exception as e:
        if ECHO: print("<IPAddress> 查询" + site + " 失败")
    return trueip


@register("chinaz")
def getIpFromChinaz(site):
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ip.tool.chinaz.com'
    }
    url = "http://ip.tool.chinaz.com/" + site
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        result = soup.find_all('span', class_="Whwtdhalf w15-0 lh45")
        for c in result:
            ip = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", c.text)
            if len(ip) != 0:
                trueip = ip[0]
    except Exception as e:
        if ECHO: print("<ChinaZ>查询" + site + " 失败")
    return trueip


@register("ipapi")
def getIpFromipapi(site):
    '''
    return trueip: None or ip
    '''
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebkit/737.36(KHTML, like Gecke) Chrome/52.0.2743.82 Safari/537.36',
        'Host': 'ip-api.com'
    }
    url = "http://ip-api.com/json/%s?lang=zh-CN" % (site)
    trueip = None
    try:
        res = requests.get(url, headers=headers, timeout=5)
        res = json.loads(res.text)
        if (res["status"] == "success"):
            trueip = res["query"]
    except Exception as e:
        if ECHO: print("<IPAPI>查询" + site + " 失败")
    return trueip
