import bleak
import geocoder 
from io import BytesIO
from j import takeCommand , speak , query

takeCommand()
if "check the heartbeat" or "what's my heartbeat" or "heartbeat" or "heart" in query:

    def heartbeatDetection():
        device_address = 'XX:XX:XX:XX:XX:XX'  # Replace with your smartwatch's address
        port = 1
        try:
            client = bleak.BleakClient(device_address)
            client.connect()
            print(f"Connected to your smartwatch ({device_address}) for heartbeat detection.")
            speak("I'm checking your heartbeat. Please hold still for a moment.")
            heartbeat_data = client.read_gatt_char('00002a37-0000-1000-8000-00805f9b34fb')
            heartbeat = int.from_bytes(heartbeat_data, byteorder='little')

            speak(f"boss Your current heartbeat is {heartbeat} beats per minute.")

            if heartbeat < 30:
              g = geocoder.ip('me')
              location = g.latlng
              print(f"Medical emergency! Sending help to {location}.")
              speak("Your heartbeat is very low. I'm sending help to your location now.")
        except Exception as e:
           print(f"Error: {e}")
           speak("Error connecting to the smartwatch or receiving heartbeat data. Please try again ,boss .")
 
        finally:
            try:
               client.disconnect()
            except:
                pass
