import canopen
import time
import logging

# logging.basicConfig(level=logging.DEBUG)
network = canopen.Network()     # define network
network.connect(channel='PCAN_USBBUS1', bustype='pcan', bitrate=1000000)  # establish communication
network.check()
# Add node to network TODO: scan for and add node
node = canopen.RemoteNode(1, 'C5-E-1-09.eds')
network.add_node(node)
network.sync.start(0.1)

node.tpdo.read()                # checks if configured properly
node.rpdo.read()

node.sdo[0x6040].raw = 6    # ready to switch state
time.sleep(0.1)
node.sdo[0x6060].raw = 1    # Set mode of operation to profile position
time.sleep(0.1)
node.sdo[0x6040].raw = 7    # switched on
time.sleep(0.1)
node.sdo[0x6040].raw = 15   # operation enabled
time.sleep(0.1)

node.sdo[0x607A].raw = 3000     # target position is stored in 0x607A
node.sdo[0x6081].raw = 50       # target velocity is stored in 0x60FF
time.sleep(0.1)


node.sdo[0x6040].raw = 95  # bit 4 = 1 new travel command problem
time.sleep(0.1)


network.sync.stop()
network.disconnect()      # disconnect after use
