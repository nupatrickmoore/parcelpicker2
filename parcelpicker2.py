import canopen
import can

# define bus instance
# bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=250000)
# define network
network = canopen.Network()
# establish connection
network.connect(channel='vcan0', bustype='socketcan')  # start communication

# standard way to add node to network, there is an alternative to scan for the node
# node = network.add_node(6, '/path/to/object_dictionary.eds')
# local_node = canopen.LocalNode(1, '/path/to/master_dictionary.eds')
# network.add_node(local_node)

# once .eds is provided, we can test if it can be read here
# node = network.add_node(6, 'od.eds')
# for obj in node.object_dictionary.values():
#     print('0x%X: %s' % (obj.index, obj.name))
# if isinstance(obj, canopen.objectdictionary.Record):
#     for subobj in obj.values():
#         print(' %d: %s' % (subobj.subindex, subobj.name))

network.disconnect() # disconnect after use



