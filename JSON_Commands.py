import subprocess
from archicad import ACConnection as ACC
from tkinter import messagebox

#####################################################################

### 1.0 JSON Kommandos von Addon benutzen ###

#####################################################################

def ExecuteJSONCommands(commandName, inputParameters = None):
    AcConection = ConnectArchicad()
    command = AcConection.types.AddOnCommandId ('AdditionalJSONCommands', commandName)
    CheckCommandsAvailability (AcConection, [command])
    return AcConection.commands.ExecuteAddOnCommand (command, inputParameters)

####################################################################

### 1.1 Verbindung mit einer laufenden ArchiCAD-Instanz aufbauen ###

####################################################################

ArchicadNotFound = "Could not find or connect to a running ArchiCAD file!"

def ReconnectToArchicad ():
    return ACC.connect()


def ConnectArchicad():
    connection = ReconnectToArchicad ()
    if not connection:  
        messagebox.showerror (ArchicadNotFound)
        exit()
    return connection

#def ConnectArchicad():
    #return ACC.connect ()

####################################################################

### 1.2 Fehlermeldung wenn Addon nicht installiert ist ###

####################################################################

JSONCommandsNotFound = "Could not find Additional JSON Commands!"
JSONCommandsNotFoundDetails = "These Commands are not available: \n{}\n\n "

def CheckCommandsAvailability (acConnection, additionalJSONCommands):
    notAvailableCommands = [commandId.commandName + ' (Namespace: ' + commandId.commandNamespace + ')' for commandId in additionalJSONCommands if not acConnection.commands.IsAddOnCommandAvailable (commandId)]
    if notAvailableCommands:
        messagebox.showerror (JSONCommandsNotFound, JSONCommandsNotFoundDetails.format ('\n'.join (notAvailableCommands)))
        exit ()

####################################################################

### 2.0 Speicherort der ArchiCAD-Datei finden ###

####################################################################

def ArchicadLocation():
    response = ExecuteJSONCommands ('GetArchicadLocation')
    ExitIfResponseNotAsExpected (response, ['archicadLocation'])
    return response['archicadLocation']

####################################################################

### 2.1 Fehlermeldung wenn Befehl fehlgeschlagen ###

####################################################################

def ExitIfError(response):
    ExitIfResponseNotAsExpected (response)

ArchicadCommandExecutionFailed = "Could not Execute ArchiCAD Command!"

def ExitIfResponseNotAsExpected (response, requiredFields = None):
    missingFields = []
    if requiredFields:
        for i in requiredFields:
            if i not in response:
               missingFields.append(i)
    if (len(response) > 0 and 'error' in response) or (len(missingFields) >0):
        messagebox.showerror (ArchicadCommandExecutionFailed, response)
        exit()

####################################################################

### 3.0 ArchiCAD schliessen ###

####################################################################

def ShutdownArchicad():
    return ExecuteJSONCommands('Quit')


####################################################################

### 3.1 ArchiCAD öffnen und Projekt öffnen ###

####################################################################

def RunArchicad(archicadLocation, projectLocation):
	acConnection = ReconnectToArchicad ()
	if not acConnection:
		subprocess.Popen (f"{EliminateSpaces (archicadLocation)} {EliminateSpaces (projectLocation)}", start_new_session=True)
	while not acConnection:
		acConnection = ReconnectToArchicad () 

####################################################################

### 3.2 Leerzeichen in Dateinamen konvertieren ###

####################################################################

def EliminateSpaces(path):
    return f"{path}"