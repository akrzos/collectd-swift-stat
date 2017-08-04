#!/usr/bin/env python
#   Copyright 2017 Alex Krzos
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
"""Collectd python plugin to read swift stat on an OpenStack Controller."""
from swiftclient.client import Connection
import collectd
import os
import time

SWIFT_STATS = {
    'x-account-object-count': 'objects',
    'x-account-container-count': 'containers',
    'x-account-bytes-used': 'bytes'}


def configure(configobj):
    global INTERVAL

    config = {c.key: c.values for c in configobj.children}
    INTERVAL = 10
    if 'interval' in config:
        INTERVAL = config['interval'][0]
    collectd.info('swift_stat: Interval: {}'.format(INTERVAL))
    collectd.register_read(read, INTERVAL)


def read(data=None):
    starttime = time.time()

    stats = swift_conn.head_account()

    for m_instance, name in SWIFT_STATS.iteritems():
        if m_instance in stats:
            metric = collectd.Values()
            metric.plugin = 'swift_stat'
            metric.interval = INTERVAL
            metric.type = 'gauge'
            metric.type_instance = m_instance
            metric.values = [stats[m_instance]]
            metric.dispatch()
        else:
            collectd.error('swift_stat: Can not find: {}'.format(m_instance))

    timediff = time.time() - starttime
    if timediff > INTERVAL:
        collectd.warning(
            'swift_stat: Took: {} > {}'.format(round(timediff, 2), INTERVAL))


def create_swift_session():
    return Connection(
        authurl=swiftstat_authurl, user=swiftstat_username,
        key=swiftstat_password, tenant_name=swiftstat_project,
        auth_version='2.0')

swiftstat_user = os.environ.get('SWIFTSTAT_USER')
swiftstat_password = os.environ.get('SWIFTSTAT_PASSWORD')
swiftstat_project = os.environ.get('SWIFTSTAT_PROJECT')
swiftstat_authurl = os.environ.get('SWIFTSTAT_AUTHURL')

collectd.info(
    'swift_stat: Connecting with user={}, password={}, tenant={}, auth_url={}'
    .format(
        swiftstat_user, swiftstat_password, swiftstat_project,
        swiftstat_authurl))

swift_conn = create_swift_session()
collectd.register_config(configure)
