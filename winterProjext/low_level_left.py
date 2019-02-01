# Example of low level interaction with a BLE UART device that has an RX and TX
# characteristic for receiving and sending data.  This doesn't use any service
# implementation and instead just manipulates the services and characteristics
# on a device.  See the uart_service.py example for a simpler UART service
# example that uses a high level service implementation.
# Author: Tony DiCola
import logging
import time
import uuid

import Adafruit_BluefruitLE


# Enable debug output.
#logging.basicConfig(level=logging.DEBUG)

# Define service and characteristic UUIDs used by the UART service.
UART_SERVICE_UUID = uuid.UUID('47452000-0f63-5b27-9122-728099603712')
TX_CHAR_UUID      = uuid.UUID('47452006-0f63-5b27-9122-728099603712')
RX_CHAR_UUID      = uuid.UUID('47452006-0f63-5b27-9122-728099603712')
SERVO_A_UUID      = uuid.UUID('47452001-0f63-5b27-9122-728099603712')
SERVE_B_UUID      = uuid.UUID('47452002-0f63-5b27-9122-728099603712')
SERVE_C_UUID      = uuid.UUID('47452003-0f63-5b27-9122-728099603712')
SERVE_D_UUID      = uuid.UUID('47452004-0f63-5b27-9122-728099603712')
SERVE_E_UUID      = uuid.UUID('47452005-0f63-5b27-9122-728099603712')
SERVE_F_UUID      = uuid.UUID('47452006-0f63-5b27-9122-728099603712')
SERVE_G_UUID      = uuid.UUID('47452008-0f63-5b27-9122-728099603712')
SERVE_RESET_UUID      = uuid.UUID('47452007-0f63-5b27-9122-728099603712')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
timestamp = 0.6

def ready(servoA,servoB,servoC,servoE,servoF,servoG):
    servoA.write_value(b'\x26')
    time.sleep(timestamp)
    servoB.write_value(b'\x66')
    time.sleep(timestamp)
    servoC.write_value(b'\x1D')
    time.sleep(timestamp)
    servoE.write_value(b'\x10')
    time.sleep(timestamp)
    servoF.write_value(b'\x3F')
    time.sleep(timestamp)
    servoG.write_value(b'\x00')
    time.sleep(timestamp)

def getbook(servoB,servoG,servoF):
    servoB.write_value(b'\x20')
    time.sleep(timestamp)
    servoG.write_value(b'\x2D')
    time.sleep(timestamp)
    servoB.write_value(b'\x78')
    time.sleep(timestamp)
    servoF.write_value(b'\x00')
    time.sleep(timestamp)
    servoG.write_value(b'\x00')
    time.sleep(timestamp)


def main2():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    ble.disconnect_devices([UART_SERVICE_UUID])

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = ble.find_device(service_uuids=[UART_SERVICE_UUID])
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for at least the specified
        # service and characteristic UUID lists.  Will time out after 60 seconds
        # (specify timeout_sec parameter to override).
        print('Discovering services...')
        device.discover([UART_SERVICE_UUID], [TX_CHAR_UUID, RX_CHAR_UUID])

        # Find the UART service and its characteristics.
        uart = device.find_service(UART_SERVICE_UUID)
        rx = uart.find_characteristic(RX_CHAR_UUID)
        tx = uart.find_characteristic(TX_CHAR_UUID)

        servoA = uart.find_characteristic(SERVO_A_UUID)
        servoB = uart.find_characteristic(SERVE_B_UUID)
        servoC = uart.find_characteristic(SERVE_C_UUID)
        servoD = uart.find_characteristic(SERVE_D_UUID)
        servoE = uart.find_characteristic(SERVE_E_UUID)
        servoF = uart.find_characteristic(SERVE_F_UUID)
        servoG = uart.find_characteristic(SERVE_G_UUID)
        servoR = uart.find_characteristic(SERVE_RESET_UUID)




        # Write a string to the TX characteristic.
        print('Sending message to device...')
        ready(servoA,servoB,servoC,servoE,servoF,servoG)
        getbook(servoB,servoG,servoF)

        # Function to receive RX characteristic changes.  Note that this will
        # be called on a different thread so be careful to make sure state that
        # the function changes is thread safe.  Use queue or other thread-safe
        # primitives to send data to other threads.
        def received(data):
            print('Received: {0}'.format(data))

        # Turn on notification of RX characteristics using the callback above.
        print('Subscribing to RX characteristic changes...')
        rx.start_notify(received)

        # Now just wait for 30 seconds to receive data.
        print('Waiting 60 seconds to receive data from the device...')
        time.sleep(3)
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()

def start():
    # Initialize the BLE system.  MUST be called before other BLE calls!
    ble.initialize()

    # Start the mainloop to process BLE events, and run the provided function in
    # a background thread.  When the provided main function stops running, returns
    # an integer status code, or throws an error the program will exit.
    ble.run_mainloop_with(main2)

start()