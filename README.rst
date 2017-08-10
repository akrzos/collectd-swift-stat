Collectd Swift Stat
===================

|collectd-swift-stat|

Overview
--------

This plugin uses the swift client in order to issue a `swift stat` against a
specific swift account.

Sample Graphs
-------------

.. figure:: https://github.com/akrzos/collectd-swift-stat/blob/master/sample-graphs-1.png
  :alt: Sample Graphs


Metrics
-------
| swift_stat/gauge-$PREFIX-bytes
| swift_stat/gauge-$PREFIX-containers
| swift_stat/gauge-$PREFIX-objects
|

$PREFIX will be the configured Prefix value in the plugin configuration in
collectd.conf

Install / Configuration
-----------------------

1. Assuming you have collectd installed already, append the following
   plugin details to your collectd.conf config file.  Adjust the
   configuration items as you see fit.  The plugin must be able to
   subprocess the ceph and rados commands.

   ::

       <LoadPlugin python>
         Globals true
       </LoadPlugin>

       <Plugin python>
         LogTraces true
         Interactive false
         Import "collectd_swift_stat"
         <Module collectd_swift_stat>
           Interval 30
           Prefix "gnocchi"
           User "gnocchi"
           Password "xxxxxxxxxxxxxxxxxxxxxxxxx"
           AuthURL "http://172.21.0.10:5000/v2.0"
           Project "service"
         </Module>
       </Plugin>

2. Install plugin

   ::

       [root@overcloud-controller-0 ~]# pip install collectd-swift-stat

3. Restart collectd

   ::

       [root@overcloud-controller-0 ~]# systemctl restart collectd

4. View metrics on the configured Swift account in your TSDB

Resources
---------

1. `wiki.openstack.org/wiki/Swift`_
2. `Collectd.org`_

.. _wiki.openstack.org/wiki/Swift: https://wiki.openstack.org/wiki/Swift
.. _Collectd.org: https://collectd.org/

.. |collectd-swift-stat| image:: https://badge.fury.io/py/collectd-swift-stat.svg
    :target: https://pypi.python.org/pypi/collectd-swift-stat
