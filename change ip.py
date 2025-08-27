from geopy.geocoders import Nominatim 
import geocoder
import os
import platform

# you can add speak function by from j and replacing print with speak
query = input("Do you want to change your IP address or track your location? ").strip().lower()

def track_location():
    g = geocoder.ip('me')
    location = g.latlng
    if location:
        latitude, longitude = location
        geolocator = Nominatim(user_agent="ME")
        location_info = geolocator.reverse((latitude, longitude), language='en')
        if location_info:
            address = location_info.address
            print(f"Your current location is {address}")
        else:
            print("Unable to fetch detailed location information.")
    else:
        print("Unable to determine your location.")   
           

def change_ip():
    """Change IP address using a suitable method for the operating system."""
    if platform.system() == "Windows":
        os.system("ipconfig /release")
        os.system("ipconfig /renew")
        print("IP address changed successfully.")

if __name__ == "__main__":
    if query == "change" or "ip":
        change_ip()
    elif query == "track" or  "location":
        track_location()
    else:
        print("sorry I didn't understand that.")
