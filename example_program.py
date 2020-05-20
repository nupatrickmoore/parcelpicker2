import canopen
import time
import logging

logging.basicConfig(level=logging.DEBUG)
network = canopen.Network()     # define network
network.connect(channel='PCAN_USBBUS1', bustype='pcan', bitrate=1000000)  # establish communication
network.check()
# Add node to network TODO: scan for and add node
node = canopen.RemoteNode(1, 'C5-E-1-09.eds')
network.add_node(node)

node.sdo[0x6040].raw = 6 #ready to switch state
time.sleep(0.1)
# node.sdo[0x6041].get_data()
# print(statusword)
time.sleep(0.1)
node.sdo[0x6060].raw = 3 #profile velocity
time.sleep(0.1)
node.sdo[0x6040].raw = 7 #ready to switch state
time.sleep(0.1)
node.sdo[0x6040].raw = 15 #operation enabled
time.sleep(0.1)
node.sdo[0x60FF].raw = 100

