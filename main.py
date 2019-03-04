
# add the following 2 lines to solve OpenGL 2.0 bug
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.uix.screenmanager import ScreenManager, Screen

#Config.set('graphics', 'resizable', '0')
#Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'height', '640')
Config.set('graphics', 'width', '360')

from kivy.lang import Builder

from kivy.clock import Clock
import datetime

from kivy.storage.dictstore import DictStore

Builder.load_string('''
#:kivy 1.10.1

<MainScreen>:
	BoxLayout:
		orientation: "vertical"

		Label:
			id: time
			size_hint_y: None
			size: self.texture_size
			font_size: 30
			text: "00:00:00"

		Label:
			id: date
			size_hint_y: None
			size: self.texture_size
			font_size: 16
			text: "00.00.0000"

		Button:
			text: "Test"
			on_press: root.pressed()

''')

class MainScreen(Screen):

	store = DictStore("app.txt")

	def dateTimeUpdate(self, *args):
		timeAndDate = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")
		self.ids.time.text, self.ids.date.text = timeAndDate


	def pressed(self):
		entrysIds= [int(entID) for entID in self.store.keys()]
		print(entrysIds)
		#newID =  entrysIds.max() if entrysIds else 0


		#self.store.put(self.newID, time=datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y"))
		
		#print(self.store.get('tito'))

class timeTrackingApp(App):
	def build(self):
		startScreen = MainScreen()
		Clock.schedule_interval(startScreen.dateTimeUpdate, 1)
		return startScreen

if __name__ == "__main__":
    timeTrackingApp().run()
