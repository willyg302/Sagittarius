"""This code is a mess and very unpythonic, but hey it's my first rodeo."""
__author__ = "William Gaul"
__copyright__ = "Copyright 2013 WillyG Productions"


from Tkinter import *
import ttk
from PIL import ImageTk
import webbrowser, httplib, urllib

import encrypt

WIZARD_HELP_URL = 'http://willyg302.github.io/Sagittarius/wizard.html'
headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}


class WizardButton(Button):

    def __init__(self, butID, master=None, **kw):
        Button.__init__(self, master, kw)
        self.data = ''
        self.butID = butID

    def getData(self):
        return self.data

    def setData(self, newData):
        self.data = newData

    def getID(self):
        return self.butID


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

    def __init__(self, isapp=True, name='sagittariuswizard'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=True, fill=BOTH)
        self.master.title('Sagittarius Wizard')
        self.master.resizable(False, False)
        self.master.wm_protocol("WM_DELETE_WINDOW", self._on_delete) # Intercept window closing
        self.isapp = isapp

        # GLOBAL VARIABLES!!!
        self.appID = StringVar()
        self.password = StringVar()
        self.availableButtons = []
        self.recipeButtons = []
        self.currentRecipe = 'Untitled'
        self.loadFile()

        # Actual initialization of view
        self.initMenu()
        self.createView()

    def _on_delete(self):
        self.saveFile()
        raise SystemExit

    def loadFile(self):
        self.recipes = {}
        with open('recipes.dat', 'a+') as f:
            for line in f:
                if line.find('<appid>') != -1:
                    self.appID.set(line[7:].rstrip('\n'))
                elif line.find('<password>') != -1:
                    self.password.set(line[10:].rstrip('\n'))
                elif line.find('<recipe>') != -1:
                    self.recipes[line.split('<recipe>')[0]] = line.split('<recipe>')[1].rstrip('\n')

    def saveFile(self):
        with open('recipes.dat', 'w') as f:
            if self.appID.get() != '':
                f.write("<appid>" + self.appID.get() + "\n")
            if self.password.get() != '':
                f.write("<password>" + self.password.get() + "\n")
            for key, value in self.recipes.iteritems():
                f.write(key + "<recipe>" + value + "\n")

    def initMenu(self):
        menubar = Menu(self.master)
        self.master.config(menu=menubar)
        
        # File menu
        fileMenu = Menu(menubar, tearoff=False)
        fileMenu.add_command(label="Save Recipe", accelerator="Ctrl+S", command=lambda: self.handleCommand(None, 'Save'))
        fileMenu.add_command(label="Save Recipe As...", accelerator="Alt+S", command=lambda: self.handleCommand(None, 'SaveAs'))
        fileMenu.add_command(label="Load Recipe", accelerator="Ctrl+O", command=lambda: self.handleCommand(None, 'Load'))
        fileMenu.add_separator()
        fileMenu.add_command(label="Clear Recipe", accelerator="Ctrl+N", command=lambda: self.handleCommand(None, 'Clear'))
        fileMenu.add_command(label="Delete Recipe", command=lambda: self.handleCommand(None, 'Delete'))
        menubar.add_cascade(label="File", menu=fileMenu)

        # Help menu
        helpMenu = Menu(menubar, tearoff=False)
        helpMenu.add_command(label="Visit Help Online", accelerator="F1", command=lambda: self.handleCommand(None, 'Help'))
        menubar.add_cascade(label="Help", menu=helpMenu)

        # Configure global keybindings
        self.bind_all("<Control-s>", lambda event: self.handleCommand(event, 'Save'))
        self.bind_all("<Alt-s>", lambda event: self.handleCommand(event, 'SaveAs'))
        self.bind_all("<Control-o>", lambda event: self.handleCommand(event, 'Load'))
        self.bind_all("<Control-n>", lambda event: self.handleCommand(event, 'Clear'))
        self.bind_all("<F1>", lambda event: self.handleCommand(event, 'Help'))

    def handleCommand(self, event, command):
        #print(command)
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
            button = self.recipeButtons.pop()
            button.destroy()
        self.validateAvailableButtons()

    def saveAsBox(self):
        top = self.getBoxTop('Save Recipe As')
        label = Label(top, text='Recipe Name:', font=('TkDefaultFont', 14))
        label.grid(row=0, padx=5, pady=5)
        entry = Entry(top, font=('TkDefaultFont', 14))
        entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)
        save = Button(top, text='Save', command=lambda: self.saveRecipeAs(top, entry.get()))
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

    def saveRecipeAs(self, box, key):
        self.currentRecipe = key
        self.recipes[self.currentRecipe] = self.getEncodedRecipe()
        box.destroy()

    def loadRecipe(self, box, key):
        self.currentRecipe = key
        self.clearRecipeBox() # Get rid of currently loaded recipe, if any
        if self.recipes[key] == '':
            return
        buttons = []
        try:
            buttons = self.recipes[key].split('<button>')
        except ValueError:
            buttons = [self.recipes[key]]
        for button in buttons:
            (butID, data) = button.split('<data>')
            self._recipe_button(butID).setData(data)
        box.destroy()

    def getEncodedRecipe(self):
        encoding = ''
        delim = ''
        for button in self.recipeButtons:
            encoding += (delim + button.getID() + "<data>" + button.getData())
            delim = '<button>'
        return encoding

    def createView(self):
        self.img_cache = [] # So that the images don't get garbage-collected
        self._create_main_panel()
        self.validateAvailableButtons()

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
        self._available_button(lf, 'get', 'Get')
        self._available_button(lf, 'add', 'Add')
        self._available_button(lf, 'mod', 'Modify')
        self._available_button(lf, 'del', 'Delete')
        self._available_button(lf, 'filter', 'Add Filter')
        self._available_button(lf, 'project', 'Add Projection')
        self._available_button(lf, 'attribute', 'Add Attribute')
        self._available_button(lf, 'modification', 'Modify Attribute')
        self._available_button(lf, 'limit', 'Set Limit')
        self._available_button(lf, 'offset', 'Set Offset')
        self._available_button(lf, 'returns', 'Returns Results')
        return lf

    def _recipe_pane(self, parent):
        self.recipeRow = LabelFrame(parent, text='Recipe', font=('TkDefaultFont', 14), height=106)
        self.getButton(self.recipeRow, 'submit', RIGHT, self.submitRecipe)
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
        # We don't want to trash the ACTION unless it's the only thing there sooo....
        if self.recipeButtons.index(button) == 0 and len(self.recipeButtons) > 1:
            return
        self.recipeButtons.remove(button)
        button.destroy()
        self.validateAvailableButtons()

    def getButton(self, parent, butID, side, command):
        colorDict = {'submit': '#90A959', 'get': '#6A9FB5', 'add': '#6A9FB5', 'mod': '#6A9FB5', 'del': '#6A9FB5', 'filter': '#AA759F', 'project': '#AA759F', 'attribute': '#75B5AA', 'modification': '#75B5AA', 'limit': '#D28445', 'offset': '#F4BF75', 'returns': '#8F5536'}
        img = ImageTk.PhotoImage(file=butID + ".png")
        self.img_cache.append(img)
        color = colorDict[butID]
        button = WizardButton(butID, parent, compound=TOP, width=64, height=64, image=img, bg=color, activebackground=color, command=command)
        button.pack(side=side, padx=5, pady=5)
        return button

    def validateAvailableButtons(self):
        actionIndex = -1
        bHasLimit = False
        bHasOffset = False
        bHasReturnsResults = False

        # Determine allowable buttons using current recipe
        for button in self.recipeButtons:
            if actionIndex == -1:
                try:
                    actionIndex = ['get', 'add', 'mod', 'del'].index(button.getID())
                except ValueError:
                    pass
            if button.getID() == 'limit' and not bHasLimit:
                bHasLimit = True
            if button.getID() == 'offset' and not bHasOffset:
                bHasOffset = True
            if button.getID() == 'returns' and not bHasReturnsResults:
                bHasReturnsResults = True

        # Set available buttons now!
        self.availableButtons[0]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[1]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[2]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[3]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[4]['state'] = 'active' if (actionIndex == 0 or actionIndex == 2 or actionIndex == 3) else 'disabled'
        self.availableButtons[5]['state'] = 'active' if (actionIndex == 0 or actionIndex == 2 or actionIndex == 3) else 'disabled'
        self.availableButtons[6]['state'] = 'active' if actionIndex == 1 else 'disabled'
        self.availableButtons[7]['state'] = 'active' if actionIndex == 2 else 'disabled'
        self.availableButtons[8]['state'] = 'disabled' if (bHasLimit or actionIndex == -1 or actionIndex == 1) else 'active'
        self.availableButtons[9]['state'] = 'disabled' if (bHasOffset or actionIndex == -1 or actionIndex == 1) else 'active'
        self.availableButtons[10]['state'] = 'disabled' if (bHasReturnsResults or actionIndex < 2) else 'active'

    def getButtonData(self, button):
        data = button.getData()
        if data.startswith('~'):
            if button.getID() == 'project':
                return data[1:3] + "~" + data[3:]
            else:
                return data[1:3] + encrypt.encrypt(data[3:], self.password.get())
        else:
            return data

    def submitRecipe(self):
        # Determine action (and return if one is not added!)
        if not self.recipeButtons or self.appID.get() == '':
            return
        dest = "/db" + self.recipeButtons[0].getID()
        self.text.insert(END, "Submitting to " + dest + " with App ID: " + self.appID.get() + " and password: " + self.password.get() + "\n")
        URLString = ''
        delim = ''
        for but in self.recipeButtons:
            bIsAction = True
            try:
                ['get', 'add', 'mod', 'del'].index(but.getID())
            except ValueError:
                bIsAction = False
            if bIsAction:
                continue
            URLString += (delim + (self.getButtonData(but) if (but.getID() != 'returns') else 'rres=true'))
            delim = '&'
        self.text.insert(END, "URL String: " + URLString + "\n")

        # Initialize connection!
        conn = httplib.HTTPConnection(self.appID.get() + ".appspot.com:80")
        conn.request("POST", dest, URLString, headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()

        # Print response
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

    def getEncryptButton(self, owner, row, initial):
        var = IntVar()
        var.set(initial)
        check = Checkbutton(owner, text="Encrypt", variable=var, font=('TkDefaultFont', 14))
        check.grid(row=row, column=1, padx=5, columnspan=2)
        check.var = var
        return check

    def getBoxButtons(self, owner, row, submitter):
        submit = Button(owner, text='Submit', command=submitter)
        submit.grid(row=row, column=1, padx=5, pady=5, sticky=W+E)
        cancel = Button(owner, text='Cancel', command=lambda: owner.destroy())
        cancel.grid(row=row, column=2, padx=5, pady=5, sticky=W+E)

    def getFieldValueBox(self, button, title, urlLetter):
        top = self.getBoxTop(title)
        field = ''
        value = ''
        check = 0
        data = button.getData()
        if data.startswith('~'):
            check = 1
            data = data[1:]
        if '::' in data:
            field = data.split('::')[0][2:]
            value = data.split('::')[1]
        fieldEntry = self.getBoxEntry(top, 'Field:', 0, field)
        valueEntry = self.getBoxEntry(top, 'Value:', 1, value)
        checkEntry = self.getEncryptButton(top, 2, check)
        self.getBoxButtons(top, 3, lambda: self.submitBox(button, ("~" if checkEntry.var.get() == 1 else "") + urlLetter + "=" + fieldEntry.get() + "::" + valueEntry.get(), top))

    def filterBox(self, button):
        self.getFieldValueBox(button, 'Add Filter', 'f')

    def projectBox(self, button):
        top = self.getBoxTop('Add Projection')
        project = ''
        check = 0
        data = button.getData()
        if data.startswith('~'):
            check = 1
            data = data[1:]
        if data != '':
            project = data[2:]
        projectEntry = self.getBoxEntry(top, 'Project:', 0, project)
        checkEntry = self.getEncryptButton(top, 1, check)
        self.getBoxButtons(top, 2, lambda: self.submitBox(button, ("~" if checkEntry.var.get() == 1 else "") + "p=" + projectEntry.get(), top))

    def attributeBox(self, button):
        self.getFieldValueBox(button, 'Add Attribute', 'a')

    def modifyBox(self, button):
        self.getFieldValueBox(button, 'Modify Attribute', 'm')

    def limitBox(self, button):
        top = self.getBoxTop('Set Limit')
        limit = ''
        if button.getData() != '':
            limit = button.getData()[5:]
        limitEntry = self.getBoxEntry(top, 'Limit:', 0, limit)
        self.getBoxButtons(top, 1, lambda: self.submitBox(button, "rlim=" + limitEntry.get(), top))

    def offsetBox(self, button):
        top = self.getBoxTop('Set Offset')
        offset = ''
        if button.getData() != '':
            offset = button.getData()[5:]
        offsetEntry = self.getBoxEntry(top, 'Offset:', 0, offset)
        self.getBoxButtons(top, 1, lambda: self.submitBox(button, "roff=" + offsetEntry.get(), top))

    def submitBox(self, button, data, box):
        button.setData(data)
        box.destroy()


if __name__ == '__main__':
    SagittariusWizard().mainloop()