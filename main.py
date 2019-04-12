
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
from kivy.properties import StringProperty, BooleanProperty, DictProperty

class ViewTasksElem(BoxLayout):
	taskName = StringProperty()
	taskTime = StringProperty()
	taskDuration = StringProperty()
	taskNumber = StringProperty()

class ViewAllTasksScreen(Screen):
	def on_enter(self):
		self.updateTasksList()

	def updateTasksList(self):
		self.ids.allTasksRv.data = self.getRecycleDataTasks()

	def getRecycleDataTasks(self):
		recycleData = []

		tasksData = timeTrackingApp.getDataEntries(timeTrackingApp, dataEntriesType='task')

		for taskKey in tasksData.keys():
			task = tasksData[taskKey]
			taskRvData = {"viewclass"	 : "ViewTasksElem",
						  "taskName"	 : task['name'],
						  "taskTime"	 : task['taskTime'],
						  "taskDuration" : task['taskDuration'],
						  "taskNumber"	 : taskKey}
			recycleData.append(taskRvData)

		if not recycleData:	
			recycleData = [{"viewclass": "Label", "text": "Not tasks"}]

		return recycleData

class ChangedTaskPopup(Popup):
	
	taskFormError = BooleanProperty()

	def getChangesInfo(self):
		infoString = "Save changes? This action will create a task with new parameters."
		errorString = "Task has been changed with errors. Correct mistakes or cancel changes."
		return errorString if self.taskFormError else infoString

	def getActionButtonText(self):
		return "To fix" if self.taskFormError else "Save"

class ViewTaskScreen(Screen):

	taskNumber = StringProperty()
	previousScreen = StringProperty()
	taskData = DictProperty()
	taskForm = DictProperty()

	def on_enter(self):
		if self.taskNumber != "0":
			self.taskData = timeTrackingApp.getStorageEntry(timeTrackingApp, self.taskNumber)

			self.ids.taskName.text = self.taskData['name']
			self.ids.prioritySpinner.text = self.getPriorityText(self.taskData['priority'])
			self.showSelectedkWeekdays(self.taskData['weekdays'])
			self.ids.taskTime.text = self.taskData['taskTime']
			self.ids.taskDuration.text = self.taskData['taskDuration']
			
			self.ids.taskActionBtn.text = "Delete task"
		else:
			self.eraseTaskForm()
			self.ids.taskActionBtn.text = "Save task"

	def taskAction(self):
		if self.taskNumber != "0":
			self.deleteTask()
			self.eraseTaskForm()
		else:
			self.saveTask()

	def saveTask(self):
		if self.checkTaskForm():
			timeTrackingApp.addStorageEntry(timeTrackingApp, self.taskForm)
			self.eraseTaskForm()

	colorRight = (1, 1, 1, 1)
	colorWrong = (1, 0, 0, 1)

	def checkTaskForm(self):
		self.taskForm = {'type':'task'}

		if self.ids.taskName.text:
			self.taskForm['name'] = self.ids.taskName.text
			self.ids.taskNameLabel.color = self.colorRight
		else:
			self.taskForm['name'] = None
			self.ids.taskNameLabel.color = self.colorWrong

		self.taskForm['priority'] = self.getSelectedPriority()

		if self.getSelectedWeekdays():
			self.taskForm['weekdays'] = self.getSelectedWeekdays()
			self.errorSelectedWeekdays(clear=True)
		else:
			self.taskForm['weekdays'] = None
			self.errorSelectedWeekdays()
		
		if self.ids.taskTime.text:
			self.taskForm['taskTime'] = self.ids.taskTime.text
			self.ids.taskTimeLabel.color = self.colorRight
		else:
			self.taskForm['taskTime'] = None
			self.ids.taskTimeLabel.color = self.colorWrong
		
		if self.ids.taskDuration.text:
			self.taskForm['taskDuration'] = self.ids.taskDuration.text
			self.ids.taskDurationLabel.color = self.colorRight
		else:
			self.taskForm['taskDuration'] = None
			self.ids.taskDurationLabel.color = self.colorWrong

		return True if not [item for item in self.taskForm if self.taskForm[item] == None] else False

	def deleteTask(self):
		self.taskData['type'] = 'deleted'
		timeTrackingApp.saveStorageEntry(timeTrackingApp, self.taskNumber, self.taskData)
		print("Just exit")

	def checkTaskChanges(self):
		if self.taskNumber != "0":
			if self.checkTaskForm():
				if self.taskForm != self.taskData:
					ChangedTaskPopup.taskFormError = False
					Factory.ChangedTaskPopup().open()
				else:
					print("Just exit")
			else:
				ChangedTaskPopup.taskFormError = True
				Factory.ChangedTaskPopup().open()
		else:
			print("Just exit")

	def choiceForChanges(self, choice):
		if choice == 'process':
			if not [item for item in self.taskForm if self.taskForm[item] == None]:
				self.deleteTask()
				timeTrackingApp.addStorageEntry(timeTrackingApp, self.taskForm)
			else:
				# When pressed button "To fix"
				return
		
		self.clearAllWrongs()
		self.eraseTaskForm()
		print("Just exit")

	def clearAllWrongs(self):
		self.ids.taskNameLabel.color = self.colorRight
		self.errorSelectedWeekdays(clear=True)
		self.ids.taskTimeLabel.color = self.colorRight
		self.ids.taskDurationLabel.color = self.colorRight

	priorityRanks = ["Normal", "High"]

	def getSelectedPriority(self):
		return self.priorityRanks.index(self.ids.prioritySpinner.text)

	def getPriorityText(self, priorityRank = 0):
		return self.priorityRanks[priorityRank]

	selectButtons = ["MON", "TUE", "WEN", "THU", "FRI", "SAT", "SUN"]

	def getSelectedWeekdays(self):
		weekdaysNumbers = []
		for button in self.ids.selectWeekdays.children:
			if button.state == 'down':
				weekdaysNumbers.append(self.selectButtons.index(button.text))

		return weekdaysNumbers

	def showSelectedkWeekdays(self, weekdays):
		buttonsDays = [self.selectButtons[day] for day in weekdays]
		for button in self.ids.selectWeekdays.children:
			if button.text in buttonsDays:
				button.state = 'down'

	def errorSelectedWeekdays(self, clear=False):
		textColor = self.colorRight if clear else self.colorWrong

		for button in self.ids.selectWeekdays.children:
			button.color = textColor

	def eraseTaskForm(self):
		self.ids.taskName.text = ""
		self.ids.prioritySpinner.text = self.getPriorityText()
		for button in self.ids.selectWeekdays.children:
			button.state = 'normal'
		self.ids.taskTime.text = ""
		self.ids.taskDuration.text = ""

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

class TaskElem(BoxLayout):
	taskName = StringProperty()
	taskTime = StringProperty()
	taskDuration = StringProperty()
	taskNumber = StringProperty()

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
				if datetime.datetime.today().weekday() in currentTask['weekdays']:
					taskData = {"viewclass"		: "TaskElem",
								"taskName"		: currentTask['name'],
								"taskTime"		: currentTask['taskTime'], 
								"taskDuration" 	: currentTask['taskDuration'],
								"taskNumber"	: taskNumber}
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

	def saveStorageEntry(self, entryNumber, dataForSave):
		self.storeData.put(str(entryNumber), **dataForSave)

	def getStorageEntry(self, entryNumber):
		return self.storeData.get(entryNumber)

	def getLastEntryNumber(self):
		if (self.storeData):
			return max([int(number) for number in self.storeData.keys()])
		else:
			return 0

	def deleteEntry(self, entryNmb):
		self.storeData.delete(entryNmb)

	def getDataEntries(self, dataEntriesType):
		dataEntriesKeys = [number for number in self.storeData.keys() if self.storeData.get(number)['type'] == dataEntriesType]
		return {key: self.storeData.get(key) for key in dataEntriesKeys}

if __name__ == "__main__":
    timeTrackingApp().run()
