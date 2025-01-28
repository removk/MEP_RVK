import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from datetime import datetime
from JSON_Commands import *

### Projektinformationen und ArchiCAD-Verbindung ###
def ProjectInformation():
    response = ExecuteJSONCommands("GetProjectInfo")
    ExitIfResponseNotAsExpected(response, ["projectLocation", "projectPath", "isTeamwork"])
    return response

projectInfo = ProjectInformation()

### Variablen vorbereiten ###
publisherSetNames = []
publishSubfolderPrefix = ''
publishSubfolderDatePostfixFormat = '%Y-%m-%d_%H-%M-%S'
selected_date = None
selected_time = None

### Publish-Funktion ###
def Publish():
    AcConnection = ConnectArchicad()
    if not AcConnection:
        messagebox.showerror("Fehler", "Keine Verbindung zu Archicad!")
        return

    progressLabel.config(text="Publishing...")
    try:
        if projectInfo['isTeamwork']:
            response = ExecuteJSONCommands('TeamworkReceive')
            ExitIfError(response)

        for publisherSetListIndex in publisherSetList.curselection():
            publisherSetName = publisherSetNames[publisherSetListIndex]
            parameters = {
                'publisherSetName': publisherSetName,
                'outputPath': os.path.join(
                    outputPathEntry.get(),
                    publisherSetName
                ),
            }
            response = ExecuteJSONCommands('Publish', parameters)
            ExitIfError(response)

        progressLabel.config(text="Publishing abgeschlossen.")
    except Exception as e:
        progressLabel.config(text="Publishing Fehler!")
        print(f"Fehler: {e}")

### Planung der Veröffentlichung ###
def SchedulePublish():
    global selected_date, selected_time
    if not selected_date or not selected_time:
        messagebox.showerror("Fehler", "Bitte wählen Sie ein Datum und eine Uhrzeit!")
        return

    try:
        target_datetime = datetime.strptime(f"{selected_date} {selected_time}", "%Y-%m-%d %H:%M")
    except ValueError:
        messagebox.showerror("Fehler", "Ungültiges Datum oder Uhrzeit!")
        return

    now = datetime.now()
    if target_datetime <= now:
        messagebox.showerror("Fehler", "Das ausgewählte Datum liegt in der Vergangenheit!")
        return

    time_delta = (target_datetime - now).total_seconds()

    # Planung des Publizierens
    progressLabel.config(text=f"Geplant für: {selected_date} um {selected_time}")
    print(f"Publishing geplant in {time_delta} Sekunden.")
    userInterface.after(int(time_delta * 1000), lambda: ExecutePublishing())

def ExecutePublishing():
    try:
        progressLabel.config(text="Publishing läuft...")
        Publish()
    except Exception as e:
        progressLabel.config(text="Publishing Fehler!")
        print(f"Fehler beim Publishing: {e}")

### GUI-Initialisierung ###
def ShowPublisherSetList():
    global publisherSetNames
    publisherSetNames = ConnectArchicad().commands.GetPublisherSetNames()
    publisherSetNames.sort()

    if publisherSetNames:
        for publisherSetName in publisherSetNames:
            publisherSetList.insert(tk.END, publisherSetName)
        publisherSetList.select_set(0)
        publisherSetList.event_generate("<<ListboxSelect>>")

def ReplaceEntryValue(entry, text):
    entry.delete(0, tk.END)
    entry.insert(0, text)

def SavePath():
    chosenPath = filedialog.askdirectory()
    if chosenPath:
        outputPathEntry['state'] = tk.NORMAL
        ReplaceEntryValue(outputPathEntry, chosenPath)
        outputPathEntry['state'] = tk.DISABLED

def OpenTimePopup():
    def ConfirmTime():
        global selected_time
        hour = hour_var.get()
        minute = minute_var.get()
        if hour.isdigit() and minute.isdigit() and 0 <= int(hour) < 24 and 0 <= int(minute) < 60:
            selected_time = f"{int(hour):02}:{int(minute):02}"
            time_popup.destroy()
        else:
            messagebox.showerror("Fehler", "Bitte eine gültige Uhrzeit eingeben!")

    time_popup = tk.Toplevel(userInterface)
    time_popup.title("Uhrzeit auswählen")
    tk.Label(time_popup, text="Stunde:").grid(row=0, column=0, padx=5, pady=5)
    hour_var = tk.StringVar()
    tk.Entry(time_popup, textvariable=hour_var, width=5).grid(row=0, column=1, padx=5, pady=5)
    tk.Label(time_popup, text="Minute:").grid(row=1, column=0, padx=5, pady=5)
    minute_var = tk.StringVar()
    tk.Entry(time_popup, textvariable=minute_var, width=5).grid(row=1, column=1, padx=5, pady=5)
    tk.Button(time_popup, text="OK", command=ConfirmTime).grid(row=2, column=0, columnspan=2, pady=10)

def OnDateSelect(event):
    global selected_date
    selected_date = calendar.get_date()
    OpenTimePopup()

### GUI erstellen ###
userInterface = tk.Tk()
userInterface.title("Automatisierte Planausgabe")
userInterface.geometry("350x600")

def UserName (projectLocation):
	return re.compile (r'.*://(.*):.*@.*').match (projectLocation).group (1)

### Funktionen für GUI ###
def ConfGui():
    ShowPublisherSetList()
    ReplaceEntryValue(projectEntry, projectInfo['projectPath'])
    if projectInfo['isTeamwork']:
        ReplaceEntryValue(projectEntry, f"{projectEntry.get()} (Teamwork project)")
        ReplaceEntryValue(taskworkUsernameEntry, UserName(projectInfo['projectLocation']))
    projectEntry['state'] = tk.DISABLED
    outputPathEntry['state'] = tk.DISABLED
    taskworkUsernameEntry['state'] = tk.DISABLED

### UI-Elemente definieren ###
projectLabel = tk.Label(userInterface, text="Projekt")
projectEntry = tk.Entry(userInterface)

taskworkUsernameLabel = tk.Label(userInterface, text="Benutzername")
taskworkUsernameEntry = tk.Entry(userInterface)

publisherSetLabel = tk.Label(userInterface, text="Publisher-Sets")
publisherSetList = tk.Listbox(userInterface, selectmode=tk.MULTIPLE)

calendarLabel = tk.Label(userInterface, text="Planausgabe planen:")
calendar = Calendar(userInterface, date_pattern="yyyy-mm-dd", selectmode="day")
calendar.bind("<<CalendarSelected>>", OnDateSelect)

outputPathLabel = tk.Label(userInterface, text="Ablageordner")
outputPathEntry = tk.Entry(userInterface)
outputPathBrowseButton = tk.Button(userInterface, text="Suchen", command=SavePath)

progressLabel = tk.Label(userInterface, text="Warten auf Planausgabe...")
executeButton = tk.Button(userInterface, text="Planen", command=SchedulePublish)
exitButton = tk.Button(userInterface, text="Abbrechen", command=userInterface.destroy)

### UI-Elemente anordnen ###
projectLabel.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
projectEntry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky=tk.EW)

taskworkUsernameLabel.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
taskworkUsernameEntry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky=tk.EW)

publisherSetLabel.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
publisherSetList.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky=tk.NSEW)

calendarLabel.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
calendar.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky=tk.NSEW)

outputPathLabel.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
outputPathEntry.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky=tk.EW)
outputPathBrowseButton.grid(row=6, column=3, padx=10, pady=5, sticky=tk.EW)

progressLabel.grid(row=7, column=0, columnspan=4, padx=10, pady=5, sticky=tk.W)
executeButton.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky=tk.EW)
exitButton.grid(row=8, column=2, columnspan=2, padx=10, pady=10, sticky=tk.EW)

### GUI initialisieren ###
ConfGui()
userInterface.mainloop()
