"""A helper wizard for the Sagittarius Online Game Service."""
__author__ = "William Gaul"
__copyright__ = "Copyright 2013 WillyG Productions"


import ttk, webbrowser, httplib, urllib, json
from Tkinter import *
from PIL import ImageTk

import encrypt

WIZARD_HELP_URL = 'http://willyg302.github.io/Sagittarius/wizard.html'
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

buttonDict = {
'submit': '#90A959',
'dbget': '#6A9FB5', 'dbadd': '#6A9FB5', 'dbmod': '#6A9FB5', 'dbdel': '#6A9FB5', 'mail': '#6A9FB5', 'ldbds': '#6A9FB5',
'filter': '#AA759F', 'project': '#AA759F',
'attribute': '#75B5AA', 'modification': '#75B5AA',
'limit': '#D28445', 'offset': '#F4BF75',
'returns': '#8F5536',
'generic': '#AC4142'}


class WizardButton(Button):

	def __init__(self, butID, master=None, **kw):
		Button.__init__(self, master, kw, compound=TOP, width=64, height=64)
		self.data = {'butID': butID}

	def getData(self):
		return self.data

	def setData(self, data):
		self.data = data;

	def setDataElement(self, key, value):
		self.data[key] = value

	def getDataElement(self, key):
		return self.data[key]

	def getID(self):
		return self.data['butID']


class DestinationButton(WizardButton):

	def setDestination(self, dest):
		self.setDataElement('dest', dest)


class ParameterButton(WizardButton):

	def __init__(self, butID, master=None, **kw):
		WizardButton.__init__(self, butID, master, **kw)
		self.setParameter('', '', False)

	def setParameter(self, param, value, encrypt):
		self.setDataElement('param', param)
		self.setDataElement('value', value)
		self.setDataElement('enc', encrypt)


class ToolTip(object):

	def __init__(self, widget):
		self.widget = widget
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0

	def showtip(self, text):
		self.text = text
		if self.tipwindow or not self.text:
			return
		x, y, cx, cy = self.widget.bbox("insert")
		x = x + self.widget.winfo_rootx() + 27
		y = y + cy + self.widget.winfo_rooty() + 27
		self.tipwindow = tw = Toplevel(self.widget)
		tw.wm_overrideredirect(1)
		tw.wm_geometry("+%d+%d" % (x, y))
		try:
			# For Mac OS
			tw.tk.call("::tk::unsupported::MacWindowStyle", "style", tw._w, "help", "noActivates")
		except TclError:
			pass
		label = Label(tw, text=self.text, justify=LEFT, background="#ffffe0", relief=SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw:
			tw.destroy()


def createToolTip(widget, text):
	toolTip = ToolTip(widget)
	def enter(event):
		if widget['state'] != 'disabled':
			toolTip.showtip(text)
	def leave(event):
		toolTip.hidetip()
	widget.bind('<Enter>', enter)
	widget.bind('<Leave>', leave)


class SagittariusWizard(ttk.Frame):

	def setupMenuOption(self, menu, shortcode, label, accelerator, binding=""):
		menu.add_command(label=label, accelerator=accelerator, command=lambda: self.handleCommand(shortcode))
		if binding:
			self.bind_all(binding, lambda event: self.handleCommand(shortcode))

	def getBoxTop(self, title):
		top = Toplevel(self)
		top.title(title)
		top.resizable(False, False)
		top.grab_set() # Make sure focus is given to the dialog box only!
		return top

	def getBoxEntry(self, owner, text, row, initial):
		label = Label(owner, text=text, font=('TkDefaultFont', 14))
		label.grid(row=row, padx=5, pady=5)
		entry = Entry(owner, font=('TkDefaultFont', 14))
		entry.insert(0, initial)
		entry.grid(row=row, column=1, padx=5, pady=5, columnspan=2)
		return entry

	def cacheImages(self):
		self.img_cache = {}
		for key in buttonDict.keys():
			self.img_cache[key] = ImageTk.PhotoImage(file=key + ".png")

	def __init__(self, name='sagittariuswizard'):
		ttk.Frame.__init__(self, name=name)
		self.pack(expand=True, fill=BOTH)
		self.master.title('Sagittarius Wizard')
		self.master.resizable(False, False)
		self.master.wm_protocol("WM_DELETE_WINDOW", self._on_delete) # Intercept window closing

		# GLOBAL VARIABLES!!!
		self.appID = StringVar()
		self.password = StringVar()
		self.availableButtons = []
		self.recipeButtons = []
		self.recipes = {}
		self.currentRecipe = 'Untitled'

		# Actual initialization of view
		self.cacheImages() # So that images don't get garbage-collected!
		self.loadFile()
		self.initMenu()
		self._create_main_panel()
		self.validateAvailableButtons()

	def _on_delete(self):
		self.saveFile()
		raise SystemExit

	def loadFile(self):
		with open('recipes.dat', 'a+') as f:
			data = f.read() # The savefile may have not been created yet
			if data:
				savefile = json.loads(data)
				self.appID.set(savefile['appID'])
				self.password.set(savefile['password'])
				self.recipes = savefile['recipes']

	def saveFile(self):
		with open('recipes.dat', 'w') as f:
			savefile = {'appID': self.appID.get(), 'password': self.password.get(), 'recipes': self.recipes}
			f.write(json.dumps(savefile, separators=(',',':')))

	def initMenu(self):
		menubar = Menu(self.master)
		self.master.config(menu=menubar)
		
		# File menu
		fileMenu = Menu(menubar, tearoff=False)
		self.setupMenuOption(fileMenu, 'Save', 'Save Recipe', 'Ctrl+S', '<Control-s>')
		self.setupMenuOption(fileMenu, 'SaveAs', 'Save Recipe As...', 'Alt+S', '<Alt-s>')
		self.setupMenuOption(fileMenu, 'Load', 'Load Recipe', 'Ctrl+O', '<Control-o>')
		fileMenu.add_separator()
		self.setupMenuOption(fileMenu, 'Clear', 'Clear Recipe', 'Ctrl+N', '<Control-n>')
		self.setupMenuOption(fileMenu, 'Delete', 'Delete Recipe', '')
		menubar.add_cascade(label="File", menu=fileMenu)

		# Help menu
		helpMenu = Menu(menubar, tearoff=False)
		self.setupMenuOption(helpMenu, 'Help', 'Visit Help Online', 'F1', '<F1>')
		menubar.add_cascade(label="Help", menu=helpMenu)

	def handleCommand(self, command):
		if command == 'Save':
			if self.currentRecipe == 'Untitled':
				self.saveAsBox()
			else:
				self.recipes[self.currentRecipe] = self.getEncodedRecipe()
		elif command == 'SaveAs':
			self.saveAsBox()
		elif command == 'Load':
			self.loadBox()
		elif command == 'Clear':
			self.clearRecipeBox()
		elif command == 'Delete':
			if self.currentRecipe in self.recipes:
				del self.recipes[self.currentRecipe]
				self.currentRecipe = 'Untitled'
		elif command == 'Help':
			webbrowser.open_new(WIZARD_HELP_URL)

	def clearRecipeBox(self):
		while self.recipeButtons:
			self.recipeButtons.pop().destroy()
		self.validateAvailableButtons()

	def saveAsBox(self):
		top = self.getBoxTop('Save Recipe As')
		label = Label(top, text='Recipe Name:', font=('TkDefaultFont', 14))
		label.grid(row=0, padx=5, pady=5)
		entry = Entry(top, font=('TkDefaultFont', 14))
		entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
		save = Button(top, text='Save', command=lambda: self.saveRecipe(top, entry.get()))
		save.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)
		cancel = Button(top, text='Cancel', command=lambda: top.destroy())
		cancel.grid(row=1, column=2, padx=5, pady=5, sticky=W+E)

	def loadBox(self):
		if not self.recipes:
			return
		keys = self.recipes.keys()
		top = self.getBoxTop('Load Recipe')
		label = Label(top, text='Choose Recipe:', font=('TkDefaultFont', 14))
		label.grid(row=0, padx=5, pady=5)
		toLoad = StringVar()
		toLoad.set(keys[0])
		w = apply(OptionMenu, (top, toLoad) + tuple(keys))
		w.configure(font=('TkDefaultFont', 14))
		w.grid(row=0, column=1, padx=5, pady=5)
		load = Button(top, text='Load', command=lambda: self.loadRecipe(top, toLoad.get()))
		load.grid(row=1, column=0, padx=5, pady=5, sticky=W+E)
		cancel = Button(top, text='Cancel', command=lambda: top.destroy())
		cancel.grid(row=1, column=1, padx=5, pady=5, sticky=W+E)

	def saveRecipe(self, box, key):
		self.currentRecipe = key
		self.recipes[self.currentRecipe] = self.getEncodedRecipe()
		box.destroy()

	def loadRecipe(self, box, key):
		self.currentRecipe = key
		self.clearRecipeBox() # Get rid of currently loaded recipe, if any
		for button in self.recipes[key]:
			if button['butID'] == 'request':
				self.setDestination(button['dest'])
			else:
				self._recipe_button(button['butID']).setData(json.loads(json.dumps(button))) # To deep copy, no reference to self.recipes!
		box.destroy()

	def getEncodedRecipe(self):
		encoding = [self.destButton.getData()]
		for button in self.recipeButtons:
			encoding.append(button.getData())
		return encoding

	def _create_main_panel(self):
		mainPanel = ttk.Frame(self, width=1024, height=768)
		mainPanel.pack_propagate(False)
		mainPanel.pack(side=TOP, fill=BOTH, expand=True)
		optionsPane = self._options_pane(mainPanel)
		optionsPane.pack(side=TOP, expand=True, padx=10, pady=10, fill=BOTH)
		availablePane = self._available_pane(mainPanel)
		availablePane.pack(side=TOP, expand=True, padx=10, pady=10, fill=BOTH)
		recipePane = self._recipe_pane(mainPanel)
		recipePane.pack(side=TOP, expand=True, padx=10, pady=10, fill=BOTH)
		outputPane = self._output_pane(mainPanel)
		outputPane.pack(side=TOP, expand=True, padx=10, pady=10, fill=BOTH)

	def _options_pane(self, parent):
		lf = LabelFrame(parent, text='Global Options', font=('TkDefaultFont', 14), height=106)
		appIDLabel = Label(lf, text="App ID:", font=('TkDefaultFont', 14))
		appIDLabel.pack(side=LEFT, padx=10)
		appIDEntry = Entry(lf, font=('TkDefaultFont', 14), textvariable=self.appID)
		appIDEntry.pack(side=LEFT)
		passLabel = Label(lf, text="Password:", font=('TkDefaultFont', 14))
		passLabel.pack(side=LEFT, padx=10)
		passEntry = Entry(lf, font=('TkDefaultFont', 14), textvariable=self.password)
		passEntry.pack(side=LEFT)
		return lf

	def _available_pane(self, parent):
		lf = LabelFrame(parent, text='Available Buttons', font=('TkDefaultFont', 14), height=106)
		self._available_button(lf, 'filter', 'Add Filter')
		self._available_button(lf, 'project', 'Add Projection')
		self._available_button(lf, 'attribute', 'Add Attribute')
		self._available_button(lf, 'modification', 'Modify Attribute')
		self._available_button(lf, 'limit', 'Set Limit')
		self._available_button(lf, 'offset', 'Set Offset')
		self._available_button(lf, 'returns', 'Returns Results')
		self._available_button(lf, 'generic', 'Generic Parameter')
		return lf

	def _recipe_pane(self, parent):
		self.recipeRow = LabelFrame(parent, text='Recipe', font=('TkDefaultFont', 14), height=106)
		self.getButton(self.recipeRow, 'submit', RIGHT, self.submitRecipe)
		button = DestinationButton('request', self.recipeRow, bg=buttonDict['dbget'], activebackground=buttonDict['dbget'],
			command=lambda: self.openDestinationBox(button))
		button.pack(side=LEFT, padx=5, pady=5)
		self.destButton = button
		self.setDestination('dbget')
		return self.recipeRow

	def _output_pane(self, parent):
		lf = LabelFrame(parent, text='Output', font=('TkDefaultFont', 14), height=350)
		self.text = Text(lf, background='white', padx=5, pady=5)
		scroll = Scrollbar(lf)
		self.text.configure(yscrollcommand=scroll.set)
		scroll.configure(command=self.text.yview)
		self.text.pack(side=LEFT, expand=True, fill=BOTH)
		scroll.pack(side=RIGHT, fill=Y)
		return lf

	def _available_button(self, parent, butID, tooltip):
		button = self.getButton(parent, butID, LEFT, lambda: self._recipe_button(butID))
		createToolTip(button, tooltip)
		self.availableButtons.append(button)

	def _recipe_button(self, butID):
		newButton = self.getButton(self.recipeRow, butID, LEFT, lambda: self.openBox(newButton))
		# Bind the destroy button event to right-click
		newButton.bind('<Button-3>', lambda event: self._trash_recipe_button(event, newButton))
		self.recipeButtons.append(newButton)
		self.validateAvailableButtons()
		return newButton

	def _trash_recipe_button(self, event, button):
		self.recipeButtons.remove(button)
		button.destroy()
		self.validateAvailableButtons()

	def getButton(self, parent, butID, side, command):
		color = buttonDict[butID]
		button = ParameterButton(butID, parent, image=self.img_cache[butID], bg=color, activebackground=color, command=command)
		button.pack(side=side, padx=5, pady=5)
		return button

	def validateAvailableButtons(self):
		actionIndex = -1
		try:
			actionIndex = ['dbget', 'dbadd', 'dbmod', 'dbdel'].index(self.destButton.getDataElement('dest'))
		except ValueError:
			pass

		bHasLimit = False
		bHasOffset = False
		bHasReturnsResults = False

		# Determine allowable buttons using current recipe
		for button in self.recipeButtons:
			if button.getID() == 'limit' and not bHasLimit:
				bHasLimit = True
			if button.getID() == 'offset' and not bHasOffset:
				bHasOffset = True
			if button.getID() == 'returns' and not bHasReturnsResults:
				bHasReturnsResults = True

		# Set available buttons now!
		self.availableButtons[0]['state'] = 'active' if (actionIndex == 0 or actionIndex == 2 or actionIndex == 3) else 'disabled'
		self.availableButtons[1]['state'] = 'active' if (actionIndex == 0 or actionIndex == 2 or actionIndex == 3) else 'disabled'
		self.availableButtons[2]['state'] = 'active' if actionIndex == 1 else 'disabled'
		self.availableButtons[3]['state'] = 'active' if actionIndex == 2 else 'disabled'
		self.availableButtons[4]['state'] = 'disabled' if (bHasLimit or actionIndex == -1 or actionIndex == 1) else 'active'
		self.availableButtons[5]['state'] = 'disabled' if (bHasOffset or actionIndex == -1 or actionIndex == 1) else 'active'
		self.availableButtons[6]['state'] = 'disabled' if (bHasReturnsResults or actionIndex < 2) else 'active'
		self.availableButtons[7]['state'] = 'active' if actionIndex == -1 else 'disabled'

	def getButtonData(self, button):
		data = button.getDataElement('value')
		if button.getDataElement('enc'):
			data = encrypt.encrypt(data, self.password.get())
		return button.getDataElement('param') + "=" + data

	def submitRecipe(self):
		if not self.recipeButtons or self.appID.get() == '':
			return
		dest = "/" + self.destButton.getDataElement('dest')
		self.text.insert(END, "Submitting to " + dest + " with App ID: " + self.appID.get() + " and password: " + self.password.get() + "\n")
		URLString = '&'.join([(self.getButtonData(but) if (but.getID() != 'returns') else 'rres=true') for but in self.recipeButtons])
		self.text.insert(END, "URL String: " + URLString + "\n")

		# Initialize connection!
		conn = httplib.HTTPConnection(self.appID.get() + ".appspot.com:80")
		conn.request("POST", dest, URLString, headers)
		response = conn.getresponse()
		data = response.read()
		conn.close()

		# Print response (Also decrypts encrypted responses)
		try:
			parsed = ''
			for part in json.JSONEncoder().iterencode(json.loads(data)):
				parsed += (("\"" + encrypt.decrypt(part[1:-1], self.password.get()) + "\"") if part.startswith('\"~') else part)
			data = json.dumps(json.loads(parsed), indent=4) # Pretty-print the JSON
		except (ValueError, KeyError, TypeError):
			pass
		self.text.insert(END, "Received data: " + data + "\n")

	def openBox(self, button):
		if button.getID() == 'filter':
			self.filterBox(button)
		elif button.getID() == 'project':
			self.projectBox(button)
		elif button.getID() == 'attribute':
			self.attributeBox(button)
		elif button.getID() == 'modification':
			self.modifyBox(button)
		elif button.getID() == 'limit':
			self.limitBox(button)
		elif button.getID() == 'offset':
			self.offsetBox(button)
		elif button.getID() == 'generic':
			self.genericBox(button)

	def setDestination(self, dest, box=None):
		self.destButton.setDestination(dest)
		self.destButton.configure(image=self.img_cache[dest])
		if box:
			box.destroy()
		self.validateAvailableButtons()
	
	def openDestinationBox(self, button):
		# We don't want to change the box type unless it's the only one there!
		if len(self.recipeButtons) != 0:
			return
		handlers = {'Get': 'dbget', 'Add': 'dbadd', 'Modify': 'dbmod', 'Delete': 'dbdel', 'Send Mail': 'mail', 'Leaderboards': 'ldbds'}
		keys = handlers.keys()
		top = self.getBoxTop('Set Action')
		label = Label(top, text='Choose Action:', font=('TkDefaultFont', 14))
		label.grid(row=0, padx=5, pady=5)
		toLoad = StringVar()
		toLoad.set(handlers.keys()[handlers.values().index(button.getDataElement('dest'))])
		w = apply(OptionMenu, (top, toLoad) + tuple(keys))
		w.configure(font=('TkDefaultFont', 14))
		w.grid(row=0, column=1, padx=5, pady=5)
		self.getBoxButtons(top, 1, lambda: self.setDestination(handlers[toLoad.get()], top), 0)

	def getEncryptButton(self, owner, row, initial):
		var = IntVar()
		var.set(initial)
		check = Checkbutton(owner, text="Encrypt", variable=var, font=('TkDefaultFont', 14))
		check.grid(row=row, column=1, padx=5, columnspan=2)
		check.var = var
		return check

	def getBoxButtons(self, owner, row, submitter, column=1):
		submit = Button(owner, text='Submit', command=submitter)
		submit.grid(row=row, column=column, padx=5, pady=5, sticky=W+E)
		cancel = Button(owner, text='Cancel', command=lambda: owner.destroy())
		cancel.grid(row=row, column=column+1, padx=5, pady=5, sticky=W+E)

	def genericBox(self, button):
		top = self.getBoxTop('Generic Parameter')
		fieldEntry = self.getBoxEntry(top, 'Field:', 0, button.getDataElement('param'))
		valueEntry = self.getBoxEntry(top, 'Value:', 1, button.getDataElement('value'))
		checkEntry = self.getEncryptButton(top, 2, 1 if button.getDataElement('enc') else 0)
		self.getBoxButtons(top, 3, lambda: self.submitBox(button, fieldEntry.get(), valueEntry.get(), checkEntry.var.get() == 1, top))

	def getFieldValueBox(self, button, title, param):
		top = self.getBoxTop(title)
		field = ''
		value = ''
		check = 1 if button.getDataElement('enc') else 0
		data = button.getDataElement('value')
		if '::' in data:
			field = data.split('::')[0]
			value = data.split('::')[1]
		fieldEntry = self.getBoxEntry(top, 'Field:', 0, field)
		valueEntry = self.getBoxEntry(top, 'Value:', 1, value)
		checkEntry = self.getEncryptButton(top, 2, check)
		self.getBoxButtons(top, 3, lambda: self.submitBox(button, param,  fieldEntry.get() + "::" + valueEntry.get(), checkEntry.var.get() == 1, top))

	def filterBox(self, button):
		self.getFieldValueBox(button, 'Add Filter', 'f')

	def projectBox(self, button):
		top = self.getBoxTop('Add Projection')
		check = 0
		project = button.getDataElement('value')
		if project.endswith('~'):
			check = 1
			project = project[:-1]
		projectEntry = self.getBoxEntry(top, 'Project:', 0, project)
		checkEntry = self.getEncryptButton(top, 1, check)
		self.getBoxButtons(top, 2, lambda: self.submitBox(button, 'p', projectEntry.get() + ("~" if checkEntry.var.get() == 1 else ""), False, top))

	def attributeBox(self, button):
		self.getFieldValueBox(button, 'Add Attribute', 'a')

	def modifyBox(self, button):
		self.getFieldValueBox(button, 'Modify Attribute', 'm')

	def limitBox(self, button):
		top = self.getBoxTop('Set Limit')
		limitEntry = self.getBoxEntry(top, 'Limit:', 0, button.getDataElement('value'))
		self.getBoxButtons(top, 1, lambda: self.submitBox(button, 'rlim', limitEntry.get(), False, top))

	def offsetBox(self, button):
		top = self.getBoxTop('Set Offset')
		offsetEntry = self.getBoxEntry(top, 'Offset:', 0, button.getDataElement('value'))
		self.getBoxButtons(top, 1, lambda: self.submitBox(button, 'roff', offsetEntry.get(), False, top))

	def submitBox(self, button, param, value, enc, box):
		button.setParameter(param, value, enc)
		box.destroy()


if __name__ == '__main__':
	SagittariusWizard().mainloop()