import canopen
import time
network = canopen.Network() # define network
network.connect(channel='PCAN_USBBUS1', bustype='pcan')  # establish communication

# Add node to network TODO: scan for and add node

node = network.add_node(1, 'C5-E-1-09.eds')
local_node = canopen.LocalNode(1, 'C5-E-1-09.eds')
network.add_node(local_node)
local_node = network[1]

local_node.rpdo.read()
local_node.tpdo.read()

# Enter operational state (NMT command)
# PDOs must be configured in the "Pre-Operational" NMT state
local_node.nmt.send_command(0x01)     # enter operational state (required for PDOs)


# Set mode of operation to profile position
# change 0x6060 register from 0 to 1 (dec)

local_node.pdo['0x6060'].set_data(b'\x01')

print(local_node.pdo['0x6060'].get_data())

# # test to see if command worked by reading 0x6061 (1 for profile position) (may have to be tdpo)
operation_mode = local_node.sdo[0x6061].get_data()
print(operation_mode)

# Set position type to relative
# change bit 6 of 0x6040 to 1

local_node.pdo['0x6040'].set_data(bytes([0x02, 0x00]))
print(local_node.pdo['0x6040'].get_data())

# set velocity value (int)
# Target velocity is stored in 0x60FF
# local_node.sdo['0x60FF'].set_data(1)

# set position value (int)
# target position is stored in 0x607A
# relative position is stored in 0x60F2
local_node.sdo['0x607F'].set_data(1)
# Start travel command
# carried out on the transition of bit 4 of 0x6040 from 0 to 1

# Change set point immediately
# bit 5 of 0x6040 controls whether the travel command starts immediately or waits for previous to complete

network.disconnect()      # disconnect after use
