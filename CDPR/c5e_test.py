import c5e
import canopen

network = canopen.Network()     # define network
network.connect(channel='PCAN_USBBUS1', bustype='pcan', bitrate=1000000)  # establish communication
network.check()

driver = c5e.Driver(network, 1)
driver.enable()

print("Moving")
driver.goto(3000, speed=50)
print("Done")

driver.shutdown()
network.sync.stop()
network.disconnect()      # disconnect after use