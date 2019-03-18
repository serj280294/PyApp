
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

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string('''
#:kivy 1.10.1

<AppScreens@ScreenManager>:
	MainScreen:
		id: mainScr
	ViewScreen:
		id: viewScr
	DateSelectScreen:
		id: dateSelectScr
	NewTaskScreen:
		id: newTaskScr

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
				on_press: 
					app.screen.transition.direction = 'left'; \
					app.screen.current = 'viewScr'
					app.screen.get_screen('viewScr').currentDate = ""

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

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(50)
			spacing: dp(20)
			
			Button:
				size_hint_x: None
				width: dp(50)
				font_size: 30
				text: "+"
				on_press: 
					app.screen.transition.direction = 'right'; \
					app.screen.current = "newTaskScr"
			
			Label:
				id: lastStateLabel
				text_size: self.size
				halign: 'left'
    			valign: 'center'
				font_size: 18
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

<ViewScreen>:
	name: "viewScr"

	BoxLayout:
		orientation: "vertical"
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_press:
				app.screen.transition.direction = 'right'; \
				app.screen.current = "mainScr"

		Label:
			font_size: 30
			size_hint_y: None
			height: dp(50)
			text: "All states"

		Button:
			id: selectDateBtn
			size_hint_y: None
			height: dp(50)
			text: root.currentDate
			on_press:
				app.screen.transition.direction = 'left'; \
				app.screen.current = "dateSelectScr"

        RecycleView:
            id: rv
            key_viewclass: 'viewclass'

            RecycleBoxLayout:
                default_size: None, dp(50)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
<StateElem>:
	orientation: 'horizontal'
	state: ""
	entryKey: ""

	Label:
		text: root.state

	Button:
		size_hint_x: .3
		on_press: root.initWin.delState(root.entryKey)
		text: "Del"

<DateSelectScreen>:
	name: "dateSelectScr"

	BoxLayout:
		orientation: "vertical"
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_press:
				app.screen.transition.direction = 'right'; \
				app.screen.current = "viewScr"

		Label:
			font_size: 30
			size_hint_y: None
			height: dp(50)
			text: "Select entrys day"

		RecycleView:
            id: dateSelectList
            key_viewclass: 'viewclass'

            RecycleBoxLayout:
                default_size: None, dp(50)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'

<DateSelectItem>:
	on_press:
		app.screen.get_screen('viewScr').currentDate = self.text; \
		app.screen.transition.direction = 'right'; \
		app.screen.current = "viewScr"

<NewTaskScreen>:
	name: "newTaskScr"

	BoxLayout:
		orientation: 'vertical'

		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_press:
				app.screen.transition.direction = 'left'; \
				app.screen.current = "mainScr"

		Label:
			font_size: 30
			#size_hint_y: None
			#height: dp(50)
			text: "New task screen"
''')

class NewTaskScreen(Screen):
	pass

class DateSelectItem(Button):
	pass

class DateSelectScreen(Screen):
	def __init__(self, **kwargs):
		super(DateSelectScreen, self).__init__(**kwargs)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		self.updateDatesList()

	def updateDatesList(self):
		#self.ids.dateSelectList.data = []

		entrysDates = []
		for key in self.store:
			date = self.store.get(key)['date']
			if date not in entrysDates:
				entrysDates.append(date)
		
		self.ids.dateSelectList.data = [{"viewclass": "DateSelectItem", "text": date} for date in sorted(entrysDates, reverse=True)]

class StateElem(BoxLayout):
	pass

class ViewScreen(Screen):

	currentDate = ""

	def __init__(self, **kwargs):
		super(ViewScreen, self).__init__(**kwargs)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		self.updateCurrentDateButton()
		self.updateStatesList()

	def delState(self, entryKey):
		#print(self.store.keys())
		self.store.delete(entryKey)	
		self.updateStatesList()

	def updateCurrentDateButton(self):
		if not self.currentDate:
			self.currentDate = datetime.datetime.today().strftime("%d.%m.%Y")

		selectedDateStr = self.currentDate

		if selectedDateStr == datetime.datetime.today().strftime("%d.%m.%Y"):
			selectedDateStr += " (today)"

		self.ids.selectDateBtn.text = selectedDateStr

	def updateStatesList(self):
		self.ids.rv.data = []

		if not self.store:
			self.ids.rv.data = [{"viewclass": "Label", "text": "No marks for all time."}]
			self.ids.selectDateBtn.disabled = True
		else:
			self.ids.selectDateBtn.disabled = False
			
			for entryNmb in self.store:
				entry = self.store.get(entryNmb)
				
				if entry['date'] == self.currentDate:
					infoStr = entryNmb + ' ' + entry['date'] + ' ' + entry['time'] + ' ' + entry['state']
					data = {"viewclass": "StateElem", "state": infoStr, "entryKey": entryNmb, "initWin": self}
					self.ids.rv.data.append(data)
			
			if not self.ids.rv.data:	
				self.ids.rv.data = [{"viewclass": "Label", "text": "No marks on this day"}]

class MainScreen(Screen):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		Clock.schedule_interval(self.dateTimeUpdate, 1)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		self.updateLastState()

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
		time, date = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")

		self.store.put(str(nextNumber), date=date, time=time, state=state)
		
		self.updateLastState()

	def updateLastState(self):
		if self.ids:
			self.ids.lastStateLabel.text = self.getLastState()

	def getLastState(self):
		lastEntryNumber = self.getLastEntryNumber()

		if lastEntryNumber == 0:
			return "No states in database"
		
		if self.store.get(str(lastEntryNumber))['date'] == datetime.datetime.today().strftime("%d.%m.%Y"):
			return "Last state today: " + self.store.get(str(lastEntryNumber))['state']
		else:
			return "Last state today: not exist"

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
