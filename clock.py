from kivy.config import Config
Config.set("graphics", "resizeable",False)
from kivy.app import App
from kivy.clock import Clock
from time import strftime
from kivy.core.window import Window

Window.size = (400,400)

class ClockApp(App):
    stopwatch_started = False
    stopwatch_seconds = 0

    def on_start(self):
        Clock.schedule_interval(self.update, 0)
    def update(self,tick):
        self.root.ids.time.text = strftime("[size=69]%I:%M%p[/size]\n %a,%B %d")
        if self.stopwatch_started:
            self.stopwatch_seconds += tick
        m, s = divmod(self.stopwatch_seconds,60)
        
        self.root.ids.stopwatch.text = ("%02d:%02d.[size=40]%02d[/size]"%(int(m),int(s),int(s*100%100)))
    def start_stop(self):
        self.root.ids.start_stop.text = 'start' if  self.stopwatch_started else 'stop'
        self.stopwatch_started = not self.stopwatch_started
    def reset(self):
        if self.stopwatch_started:
            self.root.ids.start_stop.text = 'start'
            self.stopwatch_started = False
        self.stopwatch_seconds = 0


        
if __name__ == "__main__":
    ClockApp().run()