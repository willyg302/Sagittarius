"""This code is a mess and very unpythonic, but hey it's my first rodeo."""
__author__ = "William Gaul"
__copyright__ = "Copyright 2013 WillyG Productions"


from Tkinter import *
import ttk
from PIL import ImageTk
import webbrowser

WIZARD_HELP_URL = 'http://willyg302.github.io/Sagittarius/wizard.html'


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


class SagittariusWizard(ttk.Frame):

    def __init__(self, isapp=True, name='sagittariuswizard'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=True, fill=BOTH)
        self.master.title('Sagittarius Wizard')
        self.master.resizable(False, False)
        self.isapp = isapp

        # GLOBAL VARIABLES!!!
        self.appID = StringVar()
        self.password = StringVar()
        self.availableButtons = []
        self.recipeButtons = []

        # Actual initialization of view
        self.initMenu()
        self.createView()

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
        print(command)
        if command == 'Help':
            webbrowser.open_new(WIZARD_HELP_URL)




    def createView(self):
        self.img_cache = []
        self._create_main_panel()
        self.allBtns = self.availableButtons

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

        self._available_button(lf, 'get', '#6A9FB5', lambda: self._recipe_button('get', '#6A9FB5'))
        self._available_button(lf, 'add', '#6A9FB5', lambda: self._recipe_button('add', '#6A9FB5'))
        self._available_button(lf, 'mod', '#6A9FB5', lambda: self._recipe_button('mod', '#6A9FB5'))

        self._available_button(lf, 'filter', '#AA759F', lambda: self._recipe_button('filter', '#AA759F'))
        self._available_button(lf, 'project', '#AA759F', lambda: self._recipe_button('project', '#AA759F'))

        self._available_button(lf, 'limit', '#D28445', lambda: self._recipe_button('limit', '#D28445'))
        self._available_button(lf, 'offset', '#F4BF75', lambda: self._recipe_button('offset', '#F4BF75'))
        return lf

    def _recipe_pane(self, parent):
        self.recipeRow = LabelFrame(parent, text='Recipe', font=('TkDefaultFont', 14), height=106)
        self.getButton(self.recipeRow, 'submit', RIGHT, '#90A959', self.submitRecipe)
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

    def _available_button(self, parent, imgURL, color, command):
        self.availableButtons.append(self.getButton(parent, imgURL, LEFT, color, command))

    def _recipe_button(self, imgURL, color):
        newButton = self.getButton(self.recipeRow, imgURL, LEFT, color, lambda: self.openBox(newButton))
        # Bind the destroy button event to right-click
        newButton.bind('<Button-3>', lambda event: self._trash_recipe_button(event, newButton))
        self.recipeButtons.append(newButton)
        self.validateAvailableButtons()

    def _trash_recipe_button(self, event, button):
        # We don't want to trash the ACTION unless it's the only thing there sooo....
        if self.recipeButtons.index(button) == 0 and len(self.recipeButtons) > 1:
            return
        self.recipeButtons.remove(button)
        button.destroy()
        self.validateAvailableButtons()

    def getButton(self, parent, butID, side, color, command):
        img = ImageTk.PhotoImage(file=butID + ".png")
        self.img_cache.append(img)
        button = WizardButton(butID, parent, compound=TOP, width=64, height=64, image=img, bg=color, activebackground=color, command=command)
        button.pack(side=side, padx=5, pady=5)
        return button

    def validateAvailableButtons(self):
        actionIndex = -1
        bHasLimit = False
        bHasOffset = False

        # Determine allowable buttons using current recipe
        for button in self.recipeButtons:
            if actionIndex == -1:
                try:
                    actionIndex = ['get', 'add', 'mod'].index(button.getID())
                except ValueError:
                    pass
            if button.getID() == 'limit' and not bHasLimit:
                bHasLimit = True
            if button.getID() == 'offset' and not bHasOffset:
                bHasOffset = True

        # Set available buttons now!
        self.availableButtons[0]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[1]['state'] = 'disabled' if actionIndex != -1 else 'active'
        self.availableButtons[2]['state'] = 'disabled' if actionIndex != -1 else 'active'

        self.availableButtons[3]['state'] = 'active' if actionIndex == 0 else 'disabled'
        self.availableButtons[4]['state'] = 'active' if actionIndex == 0 else 'disabled'

        self.availableButtons[5]['state'] = 'disabled' if (bHasLimit or actionIndex == -1) else 'active'
        self.availableButtons[6]['state'] = 'disabled' if (bHasOffset or actionIndex == -1) else 'active'

    def submitRecipe(self):
        self.text.insert(END, "Submitting with App ID: " + self.appID.get() + " and password: " + self.password.get() + "\n")
        for but in self.recipeButtons:
            self.text.insert(END, but.getID() + " value: " + but.getData())


    def openBox(self, button):
        if button.getID() == 'filter':
            self.filterBox(button)

    def filterBox(self, button):
        top = Toplevel(self, width=300, height=300)
        top.title('Filter')
        top.resizable(False, False)
        top.grab_set() # Make sure focus is given to the dialog box only!

        fieldLabel = Label(top, text='Field:', font=('TkDefaultFont', 14))
        fieldLabel.grid(row=0, padx=5, pady=5)
        fieldEntry = Entry(top, font=('TkDefaultFont', 14))
        fieldEntry.insert(0, button.getData())
        fieldEntry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

        valueLabel = Label(top, text='Value:', font=('TkDefaultFont', 14))
        valueLabel.grid(row=1, padx=5, pady=5)
        valueEntry = Entry(top, font=('TkDefaultFont', 14))
        valueEntry.insert(0, button.getData())
        valueEntry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

        button2 = Button(top, text='Submit', command=lambda: self.submitBox(button, fieldEntry.get(), top))
        button2.grid(row=2, column=1, padx=5, pady=5, sticky=W+E)
        button3 = Button(top, text='Cancel', command=lambda: top.destroy())
        button3.grid(row=2, column=2, padx=5, pady=5, sticky=W+E)

    def submitBox(self, button, data, box):
        button.setData(data)
        box.destroy()


if __name__ == '__main__':
    SagittariusWizard().mainloop()