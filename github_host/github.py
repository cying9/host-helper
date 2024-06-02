#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   icsying@outlook.com
@Time    :   2022-11-18 20:45:12
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   refeash github host everyday
'''
import datetime
import logging
import os

from github_host.get_ip_utils import REGISTRY_IP


class Github(object):

    def __init__(self):
        self.sites = [x.replace('\n', '') for x in open("sites.txt", "r").readlines()]
        self.addr2ip = {}
        self.hostLocation = "hosts"
        self.seq = ['ipapi', 'chinaz', 'ipaddress']

    def dropDuplication(self, line):
        flag = False
        if "#*******" in line:
            return True
        for site in self.sites:
            if site in line:
                flag = flag or True
            else:
                flag = flag or False
        return flag

    # 更新host, 并刷新本地DNS
    def updateHost(self):
        today = datetime.date.today()
        for site in self.sites[:]:
            for k in self.seq:
                trueip = REGISTRY_IP[k](site)
                if trueip:
                    self.addr2ip[site] = trueip
                    print(site + "\t" + trueip)
                    break
        
        for site in self.sites:
            if site not in self.addr2ip:
                logging.warn(f"Missing: {site}")

        with open(self.hostLocation, "r") as f1:
            f1_lines = f1.readlines()
            with open("temphost", "w") as f2:
                for line in f1_lines:
                    if self.dropDuplication(line) == False:
                        f2.write(line)
                f2.write("#*********************github " + str(today) +
                         " update********************\n")
                for key in self.addr2ip:
                    f2.write(self.addr2ip[key] + "\t" + key + "\n")
        os.remove(self.hostLocation)
        os.rename("temphost", self.hostLocation)
