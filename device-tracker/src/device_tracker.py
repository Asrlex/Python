from bleak import BleakScanner, BleakClient
import hid

'''
Device tracking and monitoring functionalities using bleak and hidapi.
'''
class DeviceTracker:
    def __init__(self):
        pass

    async def get_bluetooth_devices(self):
        """
        Scan for Bluetooth Low Energy (BLE) devices and retrieve their battery levels.
        """
        print("Scanning Bluetooth devices...")
        devices = []
        scanner = BleakScanner()
        ble_devices = await scanner.discover()

        for ble_device in ble_devices:
            try:
                async with BleakClient(ble_device) as client:
                    battery_level = await client.read_gatt_char("00002a19-0000-1000-8000-00805f9b34fb")
                    devices.append({
                        'id': ble_device.address,
                        'name': ble_device.name or "Unknown BLE Device",
                        'battery': int(battery_level[0]),
                        'latency': None
                    })
                    print(f"Found BLE device: {ble_device.name or 'Unknown'} with battery {int(battery_level[0])}%")
            except Exception as e:
                print(f"Failed to connect to {ble_device.name or 'Unknown'}: {e}")
        return devices

    def get_hid_devices(self):
        """
        Scan for HID devices and retrieve their battery levels (if supported).
        """
        print("Scanning HID devices...")
        devices = []
        for device_info in hid.enumerate():
            try:
                device = hid.device()
                device.open(device_info['vendor_id'], device_info['product_id'])
                device_name = device_info.get('product_string', 'Unknown HID Device')

                battery_level = None
                latency = None

                devices.append({
                    'id': f"{device_info['vendor_id']:04x}:{device_info['product_id']:04x}",
                    'name': device_name,
                    'battery': battery_level,
                    'latency': latency
                })
                device.close()
                print(f"Found HID device: {device_name}")
            except Exception as e:
                print(f"Failed to read HID device {device_info.get('product_string', 'Unknown')}: {e}")
        return devices

    async def get_connected_devices(self):
        """
        Retrieve a list of connected devices from both BLE and HID sources.
        """
        devices = []

        try:
            ble_devices = await self.get_bluetooth_devices()
            devices.extend(ble_devices)
        except Exception as e:
            print(f"Error scanning BLE devices: {e}")

        try:
            hid_devices = self.get_hid_devices()
            devices.extend(hid_devices)
        except Exception as e:
            print(f"Error scanning HID devices: {e}")

        return devices