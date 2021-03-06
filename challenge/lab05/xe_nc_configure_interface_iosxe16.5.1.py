#!/usr/bin/env python

"""NPDESI challenge lab 5 task 1: Consume NETCONF with Python

This version has been adapted for the changes to the YANG models used in IOS XE 16.5.1.
For more detail see https://github.com/YangModels/yang/tree/master/vendor/cisco/xe/1651"""

from lxml import etree
from ncclient import manager

if __name__ == "__main__":

    with manager.connect(host='csr1kv', port=830, username='cisco', password='cisco',
                         hostkey_verify=False, device_params={'name': 'csr'},
                         allow_agent=False, look_for_keys=False) as device:

        nc_filter = """
                <config>
                <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                 <interface>
                  <Loopback>
                   <name>200</name>
                   <ip>
                    <address>
                        <primary>
                            <address>10.200.20.1</address>
                            <mask>255.255.255.0</mask>
                        </primary>
                        <secondary>
                            <address>9.9.9.9</address>
                            <mask>255.255.255.0</mask>
                            <secondary/>
                        </secondary>
                        <secondary>
                            <address>11.11.11.11</address>
                            <mask>255.255.255.0</mask>
                            <secondary/>
                        </secondary>
                    </address>
                   </ip>
                  </Loopback>
                 </interface>
                </native>
                </config>
        """

        nc_reply = device.edit_config(target='running', config=nc_filter)

        get_filter = """
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <interface>
                <Loopback>
                    <name>200</name>
                </Loopback>
            </interface>
        </native>
        """
        nc_get_reply = device.get(('subtree', get_filter))
        print etree.tostring(nc_get_reply.data_ele, pretty_print=True)


