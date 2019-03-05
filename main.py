
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

from kivy.storage.jsonstore import JsonStore

Builder.load_string('''
#:kivy 1.10.1

<MainScreen>:
	BoxLayout:
		orientation: "vertical"

		Label:
			size_hint_y: .1
			id: time
			text_size: self.size
			halign: 'center'
    		valign: 'bottom'
			font_size: 30
			text: "00:00:00"

		Label:
			size_hint_y: .1
			id: date
			text_size: self.size
			halign: 'center'
    		valign: 'top'
			font_size: 16
			text: "00.00.0000"

		BoxLayout:
			orientation: 'vertical'
				
			Button:
				text: "Awoke"
				on_press: root.pressed(self.text)
		
			Button:
				text: "Go to work"
				on_press: root.pressed(self.text)
	
			Button:
				text: "At work"
				on_press: root.pressed(self.text)

			Button:
				text: "Go home"
				on_press: root.pressed(self.text)

			Button:
				text: "In home"
				on_press: root.pressed(self.text)

			Button:
				text: "Sleep"
				on_press: root.pressed(self.text)

''')

class MainScreen(Screen):

	store = JsonStore("data.json")
	
	def dateTimeUpdate(self, *args):
		timeAndDate = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")
		self.ids.time.text, self.ids.date.text = timeAndDate


	def pressed(self, stateText):
		entryNumbers = [number for number in self.store.keys()]
		nextNumber = max(entryNumbers)+1 if entryNumbers else 0

		state = stateText
		date, time = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")

		self.store.put(nextNumber, date=date, time=time, state=state)
		
		#print(nextNumber, self.store.get(nextNumber))

		#for data  in self.store:
		#	print(data, self.store.get(data))

class timeTrackingApp(App):
	def build(self):
		startScreen = MainScreen()
		Clock.schedule_interval(startScreen.dateTimeUpdate, 1)
		return startScreen

if __name__ == "__main__":
    timeTrackingApp().run()
