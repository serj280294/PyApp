
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
from kivy.factory import Factory

Builder.load_string('''
#:kivy 1.10.1

<AppScreens@ScreenManager>:
	MainScreen:
		id: mainScr
	ViewScreen:
		id: viewScr

<ViewScreen>:
	name: "viewScr"

	BoxLayout:
		orientation: "vertical"
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_press: app.screen.current = "mainScr"

		Label:
			font_size: 30
			size_hint_y: None
			height: dp(50)
			text: "All states"

		#Label:
		#	font_size: 40
		#	text: "test"

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'

            RecycleBoxLayout:
                default_size: None, dp(20)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

<MainScreen>:
	name: "mainScr"
	BoxLayout:
		orientation: 'vertical'

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(50)

			Button:
				text: "View all states"
				on_press: app.screen.current = 'viewScr'
			Button:
				text: "Statistic"

		Label:
			size_hint_y: .1
			id: time
			name: "time"
			text_size: self.size
			halign: 'center'
    		valign: 'bottom'
			font_size: 30
			text: root.getTimeDate(self.name)

		Label:
			size_hint_y: .1
			id: date
			name: "date"
			text_size: self.size
			halign: 'center'
    		valign: 'top'
			font_size: 16
			text: root.getTimeDate(self.name)

		Label:
			id: lastStateLabel
			size_hint_y: .05
			text_size: self.size
			halign: 'center'
    		valign: 'center'
			font_size: 16
			text: root.getLastState()
			
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
				text: "At home"
				on_press: root.pressed(self.text)

			Button:
				text: "Sleep"
				on_press: root.pressed(self.text)

''')

class ViewScreen(Screen):
	def __init__(self, **kwargs):
		super(ViewScreen, self).__init__(**kwargs)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		for entryNmb in self.store:
			entry = self.store.get(entryNmb)
			infoStr = entryNmb + ' ' + entry['date'] + ' ' + entry['time'] + ' ' + entry['state']
			data = {"viewclass": "Label", "text": infoStr}
			if data not in self.ids.rv.data:
				self.ids.rv.data.append(data)

class MainScreen(Screen):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		Clock.schedule_interval(self.dateTimeUpdate, 1)
		self.store = timeTrackingApp.storeData

	def getTimeDate(self, labelName=None):
		if labelName == "time":
			return datetime.datetime.today().strftime("%H:%M:%S")
		elif labelName == "date":
			return datetime.datetime.today().strftime("%d.%m.%Y")
		else:
			return datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")


	def dateTimeUpdate(self, *args):
		timeAndDate = self.getTimeDate()
		self.ids.time.text, self.ids.date.text = timeAndDate

	def pressed(self, stateText):
		lastEntryNumber = self.getLastEntryNumber()
		nextNumber = lastEntryNumber+1

		state = stateText
		date, time = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")

		self.store.put(str(nextNumber), date=date, time=time, state=state)
		
		self.updateLastState(nextNumber)

	def getLastState(self):
		lastEntryNumber = self.getLastEntryNumber()
		if lastEntryNumber == 0:
			return "Last state: not exist"
		else:
			return "Last state: " + self.store.get(str(lastEntryNumber))['state']

	def updateLastState(self, entryNumber):
		self.ids.lastStateLabel.text = "Last state: " + self.store.get(str(entryNumber))['state']

	def getLastEntryNumber(self):
		if (self.store):
			return max([int(number) for number in self.store.keys()])
		else:
			return 0

class timeTrackingApp(App):
	
	storeData = JsonStore("data.json")

	def build(self):
		
		self.screen = Factory.AppScreens()
		return self.screen

if __name__ == "__main__":
    timeTrackingApp().run()
