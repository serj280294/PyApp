
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
from kivy.uix.popup import Popup

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
				on_release: 
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
			font_size: sp(30)
			text: root.getTimeDate(self.name)

		Label:
			size_hint_y: .1
			id: date
			name: "date"
			text_size: self.size
			halign: 'center'
    		valign: 'top'
			font_size: sp(16)
			text: root.getTimeDate(self.name)

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(50)
			spacing: dp(20)
			
			Button:
				size_hint_x: None
				width: dp(50)
				font_size: sp(30)
				text: "+"
				on_release: 
					app.screen.transition.direction = 'right'; \
					app.screen.current = "newTaskScr"
			
			Label:
				id: lastStateLabel
				text_size: self.size
				halign: 'left'
    			valign: 'center'
				font_size: sp(18)
				text: root.getLastState()
			
		RecycleView:
			id: mainrv
			key_viewclass: 'viewclass'
			data: root.getRecycleDataTasks()

			RecycleBoxLayout:
				default_size: None, dp(50)
				default_size_hint: 1, None
				size_hint_y: None
				height: self.minimum_height
				orientation: 'vertical'

<TaskElem>:
	taskKeyNumber: ""
	on_release: app.screen.get_screen("mainScr").pressed(self.taskKeyNumber)

<ViewScreen>:
	name: "viewScr"

	BoxLayout:
		orientation: "vertical"
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_release:
				app.screen.transition.direction = 'right'; \
				app.screen.current = "mainScr"

		Label:
			font_size: sp(30)
			size_hint_y: None
			height: dp(50)
			text: "All states"

		Button:
			id: selectDateBtn
			size_hint_y: None
			height: dp(50)
			text: root.currentDate
			on_release:
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
	entryKeyNmb: ""

	Label:
		text: root.state

	Button:
		size_hint_x: None
		width: dp(70)
		#on_release: root.initWin.delState(root.entryKey)
		on_release: root.editState(root.entryKeyNmb)
		text: "Edit"

<EditStatePopup>:
	title: "Edit entry " + self.editEntryNumber

	BoxLayout:
		orientation: 'vertical'

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(30)

			Label:
				text: "Task name:"

			TextInput:
				id: taskName
				disabled: True

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(30)

			Label:
				text: "State date:"

			TextInput:
				id: stateDate
				disabled: True

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(30)

			Label:
				text: "State time:"

			TextInput:
				id: stateTime

		Label:

		Button:
			size_hint_y: None
			height: dp(50)
			text: "Delete entry"
			on_release: app.deleteEntry(root.editEntryNumber); 				 \
						app.screen.get_screen('viewScr').updateStatesList(); \
						root.dismiss()
		
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Save and close"
			on_release: root.saveChanges(); \
						app.screen.get_screen('viewScr').updateStatesList(); \
						root.dismiss()

<DateSelectScreen>:
	name: "dateSelectScr"

	BoxLayout:
		orientation: "vertical"
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_release:
				app.screen.transition.direction = 'right'; \
				app.screen.current = "viewScr"

		Label:
			font_size: sp(30)
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
	on_release:
		app.screen.get_screen('viewScr').currentDate = self.text; \
		app.screen.transition.direction = 'right'; \
		app.screen.current = "viewScr"

<NewTaskScreen>:
	name: "newTaskScr"

	BoxLayout:
		orientation: 'vertical'
		spacing: dp(10)
		
		Button:
			size_hint_y: None
			height: dp(50)
			text: "Back"
			on_release:
				app.screen.transition.direction = 'left'; \
				app.screen.current = "mainScr"

		BoxLayout:
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(30)
			Label:
				size_hint_x: .3
				text: "Task name:"

			TextInput:
				id: taskName
				size_hint_x: .7
				multiline: False
				padding_y: self.height / 2 - self.line_height / 2

		BoxLayout:
			id: selectWeekdays
			orientation: 'horizontal'
			size_hint_y: None
			height: dp(50)
			
			ToggleButton:
				text: "MON"
			ToggleButton:
				text: "TUE"
			ToggleButton:
				text: "WEN"
			ToggleButton:
				text: "THU"
			ToggleButton:
				text: "FRI"
			ToggleButton:
				text: "SAT"
			ToggleButton:
				text: "SUN"

		BoxLayout:
			orientation: 'vertical'
			size_hint_y: None
			height: dp(80)
			
			Label:
				text: "Task time"

			TextInput:
				id: taskTime
				size_hint_y: None
				height: dp(50)
				multiline: False
				padding_y: self.height / 2 - self.line_height / 2
				font_size: sp(30)
				padding_x: self.center[0] - self._get_text_width(self.text, self.tab_width, self._label_cached) / 2
				
		Label:
			font_size: sp(30)
			#size_hint_y: None
			#height: dp(50)
			#text: "New task screen"

		Button:
			size_hint_y: None
			height: dp(50)
			text: "Save task"
			on_press: root.saveTask()
''')

class NewTaskScreen(Screen):
	def saveTask(self):
		taskFormError = 0

		taskForm = {'type':'task'}

		taskForm['name'] = self.ids.taskName.text
		if not taskForm['name']:
			taskFormError = 1
			#self.ids.taskNameLabel.
			print("Empty task name")

		taskForm['weekdays'] = self.getSelectedWeekdays()
		if not taskForm['weekdays']:
			taskFormError = 1
			print("Weekdays not selected")

		taskForm['taskTime'] = self.ids.taskTime.text
		if not taskForm['taskTime']:
			taskFormError = 1
			print("Empty task time")

		if taskFormError:
			return

		timeTrackingApp.addStorageEntry(timeTrackingApp, taskForm)

		self.ids.taskName.text = ""
		for button in self.ids.selectWeekdays.children:
			button.state = 'normal'
		self.ids.taskTime.text = ""

	def getSelectedWeekdays(self):
		weekdaysNumbers = []

		selectButtons = {"MON": 1, "TUE": 2, "WEN": 3, "THU": 4, "FRI": 5, "SAT": 6, "SUN": 7}
		for button in self.ids.selectWeekdays.children:
			if button.state == 'down':
				weekdaysNumbers.append(selectButtons[button.text])

		return weekdaysNumbers

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

		entrysKeys = [key for key in self.store.keys() if self.store.get(key)['type'] == 'entry']

		for key in entrysKeys:
			date = self.store.get(key)['date']
			if date not in entrysDates:
				entrysDates.append(date)
		
		self.ids.dateSelectList.data = [{"viewclass": "DateSelectItem", "text": date} for date in sorted(entrysDates, reverse=True)]

class EditStatePopup(Popup):
	
	editEntryNumber = 0

	def __init__(self, **kwargs):
		super(EditStatePopup, self).__init__(**kwargs)
		self.store = timeTrackingApp.storeData

	def on_open(self):
		entryData = self.store.get(self.editEntryNumber)

		self.ids['taskName'].text = entryData['state']
		self.ids['stateDate'].text = entryData['date']
		self.ids['stateTime'].text = entryData['time']

	def saveChanges(self):
		entryData = self.store.get(self.editEntryNumber)

		if self.ids['stateTime'].text != entryData['time']:
			entryData['time'] = self.ids['stateTime'].text
			self.store.put(self.editEntryNumber, **entryData)

class StateElem(BoxLayout):
	def editState(self, entryNmb):
		EditStatePopup.editEntryNumber = entryNmb
		Factory.EditStatePopup().open()

class ViewScreen(Screen):

	currentDate = ""

	def __init__(self, **kwargs):
		super(ViewScreen, self).__init__(**kwargs)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		self.updateCurrentDateButton()
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

		entrysNumbers = [number for number in self.store.keys() if self.store.get(number)['type'] == 'entry']

		if not entrysNumbers:
			self.ids.rv.data = [{"viewclass": "Label", "text": "No marks for all time."}]
			self.ids.selectDateBtn.disabled = True
		else:
			self.ids.selectDateBtn.disabled = False
			
			for entryNmb in entrysNumbers:
				entry = self.store.get(entryNmb)
				
				if entry['date'] == self.currentDate:
					infoStr = entryNmb + ' ' + entry['date'] + ' ' + entry['time'] + ' ' + entry['state']
					data = {"viewclass": "StateElem", "state": infoStr, "entryKeyNmb": entryNmb}
					self.ids.rv.data.append(data)
			
			if not self.ids.rv.data:	
				self.ids.rv.data = [{"viewclass": "Label", "text": "No marks on this day"}]

class TaskElem(Button):
	pass

class MainScreen(Screen):
	def __init__(self, **kwargs):
		super(MainScreen, self).__init__(**kwargs)
		Clock.schedule_interval(self.dateTimeUpdate, 1)
		self.store = timeTrackingApp.storeData

	def on_enter(self):
		self.updateLastState()
		self.updateTasksList()

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

	def pressed(self, taskNumber):
		entryData = {'type':'entry'}

		entryData['state'] = self.store.get(taskNumber)['name']
		entryData['time'], entryData['date'] = datetime.datetime.today().strftime("%H:%M:%S %d.%m.%Y").split(" ")

		timeTrackingApp.addStorageEntry(timeTrackingApp, entryData)
		
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
		entrysKeys = [int(number) for number in self.store.keys() if self.store.get(number)['type'] == 'entry']
		if (entrysKeys):
			return max(entrysKeys)
		else:
			return 0

	def updateTasksList(self):
		if self.ids:
			self.ids.mainrv.data = self.getRecycleDataTasks()

	def getRecycleDataTasks(self):
		recycleData = []

		tasksNumbers = [number for number in self.store.keys() if self.store.get(number)['type'] == 'task']

		if not tasksNumbers:
			recycleData = [{"viewclass": "Label", "text": "No tasks for all time."}]
		else:
			for taskNumber in tasksNumbers:
				currentTask = self.store.get(taskNumber)
				if datetime.datetime.today().isoweekday() in currentTask['weekdays']:
					taskString = "{} ({})".format(currentTask['name'], currentTask['taskTime'])
					taskData = {"viewclass": "TaskElem", "text": taskString, "taskKeyNumber": taskNumber}
					recycleData.append(taskData)

			if not recycleData:	
				recycleData = [{"viewclass": "Label", "text": "Not tasks for today"}]

		return recycleData

class timeTrackingApp(App):
	
	storeData = JsonStore("data.json")

	def build(self):
		self.screen = Factory.AppScreens()
		return self.screen

	def addStorageEntry(self, dataForSave):
		lastEntryNumber = self.getLastEntryNumber(self)
		nextNumber = lastEntryNumber+1

		self.storeData.put(str(nextNumber), **dataForSave)

	def getLastEntryNumber(self):
		if (self.storeData):
			return max([int(number) for number in self.storeData.keys()])
		else:
			return 0

	def deleteEntry(self, entryNmb):
		self.storeData.delete(entryNmb)

if __name__ == "__main__":
    timeTrackingApp().run()
