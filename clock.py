from kivy.config import Config
Config.set("graphics", "resizeable",False)
from kivy.app import App
from kivy.clock import Clock
from time import strftime
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from datetime import datetime, timedelta
from playsound import playsound
from time import strftime
import re


Window.size = (444,444)

class ClockApp(App):
    stopwatch_started = False
    stopwatch_seconds = 0

    alarm_time= " "

    running = False

   

    def on_start(self):
        Clock.schedule_interval(self.update, 0)

    def update(self,tick):
        self.root.ids.time.text = strftime("[size=69]%I:%M:%S %p[/size]\n %a,%B %d")
        if self.stopwatch_started:
            self.stopwatch_seconds += tick

        m, s = divmod(self.stopwatch_seconds,60)

        self.root.ids.stopwatch.text = ("%02d:%02d.[size=40]%02d[/size]"%(int(m),int(s),int(s*100%100)))

        if self.alarm_time == strftime('%I:%M %p'):

            if strftime('%S') == '00' and strftime('%S') < '09':
                self.root.ids.check_time.text = "[size=60]BANGUN BRO![/size]"
                self.sound = SoundLoader.load('./bangun.mp3')
                self.sound.play()
        
    def start_stop(self):
        self.root.ids.start_stop.text = 'start' if  self.stopwatch_started else 'stop'
        self.stopwatch_started = not self.stopwatch_started
    def reset(self):
        if self.stopwatch_started:
            self.root.ids.start_stop.text = 'start'
            self.stopwatch_started = False
            
        self.stopwatch_seconds = 0
        
     def stop_alarm(self):
        if hasattr(self, 'sound') and self.sound:
            self.sound.stop()
            self.reset()

    def set_alarm(self, alarm_time):
        if len(alarm_time) != 8:
            self.root.ids.check_time.text = "Invalid time format!\nTry add a zero before the hour \n if it's less than 10 and or add PM/AM"
        else:
            if int(alarm_time[0:2]) > 12:
                self.root.ids.check_time.text = "Invalid HOUR format! Please try again..."
            elif int(alarm_time[3:5]) > 59:
                self.root.ids.check_time.text = "Invalid MINUTE format! Please try again..."
            else:
                self.alarm_time = alarm_time
                self.root.ids.check_time.text = "Setting the alarm now..."
            
    def start(self):       
        cd_time = self.root.ids.text_input.text 
        check = re.findall("[a-zA-Z]", cd_time)
        if cd_time == '' or len(cd_time) != 8 or check:
            self.root.ids.show.text = 'Please enter the time like this "00:00:05"'     
        elif cd_time == '00:00:00':
            Clock.unschedule(self.begin)
        elif self.root.ids.button.text == 'Reset':
            self.reset()
            
        else:
            self.root.ids.button.text = 'Reset'
            h = cd_time[0:2]
            m = cd_time[3:5]
            s = cd_time[6:8]
            h = int(h)
            m = int(m)
            s = int(s)
        
            self.delta = datetime.now() + timedelta(hours=h, minutes=m, seconds = s)
            if not self.running:
                    self.running = True
                    Clock.schedule_interval(self.begin, 0.05)
                      
    def resett(self): 
        
        self.root.ids.button.text = 'Start' 
        self.root.ids.show.text = 'Enter the time to countdown in this format "HH:MM:SS"\n For example,00:00:30'
        self.root.ids.text_input.text = '00:00:00'
            
        if self.running:  
            self.running = False
            Clock.unschedule(self.begin)
            
    def pause(self):
        if self.running:  
            self.running = False
            Clock.unschedule(self.begin) 

    def begin(self, cd_start):
        delta = self.delta - datetime.now()
        delta = str(delta)
        self.root.ids.show.text = '[size=50] 0' + delta[0:7] + '[/size]'
        
        if delta[0:7]  == "0:00:00":
           
            '0' + delta[0:7]
            self.sound = SoundLoader.load('./bangun.mp3')
            self.sound.play()
            self.reset()
    def toggle(self):
        if self.running:
            self.resett()
        else:
            self.start()  


        
if __name__ == "__main__":
    ClockApp().run()