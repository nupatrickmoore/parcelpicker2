# Print .eds file on can device
# for obj in node.object_dictionary.values():
    # print('0x%X: %s' % (obj.index, obj.name))

# if isinstance(obj, canopen.objectdictionary.Record):
    # for subobj in obj.values():
        # print(' %d: %s' % (subobj.subindex, subobj.name))

# Print nodes in network
# for node_id in network:
#     print(network[node_id])

# testing of SDOs
# for node_id in network:
#     print(network[node_id])

# for sdo in node.sdo:
#     print(sdo)
#
# print(node.sdo[4096])
# # print(node)
# # print(network[1].sdo[0x1000])
# device_type = network[1].sdo[0x1000]
# print("The device type is 0x%X" % device_type.raw)

# read statusword
# statusword = network[1].tpdo[1]['0x6041'].raw
# print(statusword)