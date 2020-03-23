import canopen
from canopen.profiles.p402 import BaseNode402
# define network
network = canopen.Network()
# establish connection
network.connect(channel='vcan0', bustype='socketcan')  # start communication (virtual port)

# # standard way to add node to network, there is an alternative to scan for the nodes
# node = network.add_node(6, 'C5-E-1-09.eds')
# local_node = canopen.LocalNode(1, 'C5-E-1-09.eds')
# network.add_node(local_node)

# add node to network with device profile for motor controller
node = canopen.BaseNode402(3, 'C5-E-1-09.eds')
network = canopen.Network()
network.add_node(node)

# .eds Test block
# node = network.add_node(6, 'C5-E-1-09.eds')
# for obj in node.object_dictionary.values():
#     print('0x%X: %s' % (obj.index, obj.name))
# if isinstance(obj, canopen.objectdictionary.Record):
#     for subobj in obj.values():
#         print(' %d: %s' % (subobj.subindex, subobj.name))

# # Send NMT start to all nodes (exclude for virtual port
# network.send_message(0x0, [0x1, 0])
# node.nmt.wait_for_heartbeat()
# assert node.nmt.state == 'OPERATIONAL' # PDOs can only be used in this state

# run the setup routine for TPDO1 and it's callback
node.setup_402_state_machine()

# command to go to 'READY TO SWITCH ON' from 'NOT READY TO SWITCH ON' or 'SWITCHED ON'
node.sdo[0x6040].raw = 0x06

# Read the state of the Statusword
node.sdo[0x6041].raw

# disconnect after use
# network.disconnect()