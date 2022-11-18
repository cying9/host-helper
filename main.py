#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Contact :   liuyuqi.gov@msn.cn
@Time    :   2019/08/03 16:15:54
@License :   Copyright © 2017-2022 liuyuqi. All Rights Reserved.
@Desc    :   main function
'''
from github_host.github import Github

if __name__ == '__main__':
    github = Github()
    github.updateHost()
