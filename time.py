import datetime

if input().lower().strip() == "what's the time" or "the time is" or "current time":
    print(datetime.datetime.now().strftime('%H:%M:%S'))

# this code works too
# from speech import takecommand()
# from speech import speak
#  def time():
#    now = datetime.datetime.now()
#    speak(f"The current time is {now.strftime('%H:%M:%S')}, sir.")
#    speak(f"It's {now.strftime('%I:%M %p')} right now.")