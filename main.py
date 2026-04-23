import customtkinter as ctk
import re
from enum import Enum

app = ctk.CTk()
app.title("University Life")
app.geometry("500x400")
ctk.set_appearance_mode("light")

scheduleFile = "schedule.txt"
tasksFile = "tasks.txt"
eventsFile = "events.txt"
notesFile = "notes.txt"

mainContainer = ctk.CTkFrame(app, fg_color="transparent")
mainContainer.pack(pady=20, padx=20, expand=True)

class Page(Enum):
    MENU = "MENU"
    SCHEDULE = "SCHEDULE"
    TASKS = "TASKS"
    EVENTS = "EVENTS"
    NOTES = "NOTES"

currentPage = Page.MENU

menuContainer = ctk.CTkFrame(mainContainer, fg_color="transparent")
menuContainer.pack()

def makeLabel(text, container):
    label = ctk.CTkLabel(
        container,
        text=text,
        font=("Dubai", 32, "bold"),
        text_color="#1c2b48",
        corner_radius=18
    )
    label.pack(pady=5)

def makeButton(text, container, command):
    button = ctk.CTkButton(
        container,
        text=text,
        width=200,
        font=("Dubai", 20, "bold"),
        fg_color="#5f86a6",
        text_color="#e8ecef",
        hover_color="#3f5c75",
        command=command
    )
    button.pack(pady=5)

def makeTextField(placeholderText, container):
    textField = ctk.CTkEntry(
        container,
        placeholder_text=placeholderText,
        width=250,
        height=40,
        font=("Dubai", 18, "bold"),
        fg_color="#cfe3f1",
        text_color="#333333",
    )
    textField.pack(pady=5)
    return textField

def makeGoBackButton(container, command):
    button = ctk.CTkButton(
        container,
        text="Go Back",
        width=200,
        font=("Dubai", 20, "bold"),
        fg_color="transparent",
        text_color="#243a5e",
        border_color="#0b2033",
        border_width=2,
        command=command
    )
    button.pack(pady=5)

def hideAll():
    menuContainer.pack_forget()
    scheduleWindow.pack_forget()
    tasksWindow.pack_forget()
    eventsWindow.pack_forget()
    notesWindow.pack_forget()
    addClassWindow.pack_forget()
    viewScheduleWindow.pack_forget()
    deleteClassWindow.pack_forget()

def saveDataButton(container, command):
    button = ctk.CTkButton (
        container,
        text="Save!",
        width=200,
        font=("Dubai", 20, "bold"),
        fg_color="transparent",
        text_color="#243a5e",
        border_color="#0b2033",
        border_width=2,
        command=command
    )
    button.pack()


def checkInput(data, type):
    match type:
        case "text":
            return bool (re.fullmatch(r"[a-zA-Z0-9 ]+", data))
        case "numbers":
            return data.isdigit()
        case "mix":
            return bool(re.fullmatch(r"[a-zA-Z0-9 ]+", data))
        case "time":
            return bool (re.fullmatch(r"\d{2}:\d{2}", data))
        case "date":
            return bool(re.fullmatch(r"\d{2}\.\d{2}\.(\d{2}|\d{4})", data))

def showNotification(container, message, color):
    notification = ctk.CTkLabel(
        container,
        text=message,
        font=("Dubai", 14, "bold"),
        text_color="white",
        fg_color=color,
        corner_radius=8
    )
    notification.pack(pady=5)
    app.after(2000, notification.destroy)

def saveDataButtonClicked(classs, day, time, room):
    if checkInput(classs, "text") and checkInput(day, "date") and checkInput(time, "time") and checkInput(room, "mix"):
        try:
            with open(scheduleFile, 'a') as f:
                f.write(f"{classs},{day},{time},{room}\n")
            showNotification(addClassWindow, "DATA SAVED!", "#38c34a")
            classField.delete(0, "end")
            dayField.delete(0, "end")
            timeField.delete(0, "end")
            roomField.delete(0, "end")
        except Exception as e:
            showNotification(addClassWindow, f"Error: {e}", "#e74c3c")
    else:
        showNotification(mainContainer, "INVALID DATA", "#e74c3c")

def goToMenu():
    hideAll()
    menuContainer.pack()

def goToSchedule():
    hideAll()
    scheduleWindow.pack()

def buttonClicked(name):
    hideAll()
    match name:
        case "scheduleButton":
            scheduleWindow.pack()
        case "tasksButton":
            tasksWindow.pack()
        case "eventsButton":
            eventsWindow.pack()
        case "notesButton":
            notesWindow.pack()

def setSchedulesPages(page):
    hideAll()
    match page:
        case "addClassWindow":
            addClassWindow.pack()
        case "viewScheduleWindow":
            viewScheduleWindow.pack()
        case "deleteClassWindow":
            deleteClassWindow.pack()

def closeApp():
    app.destroy()


scheduleWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
tasksWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
eventsWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
notesWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
addClassWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")  
viewScheduleWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")
deleteClassWindow= ctk.CTkFrame(mainContainer, fg_color="transparent")

# Menu
makeLabel("CAMPUS LIFE PLANNER", menuContainer)
makeButton("Schedule", menuContainer, lambda: buttonClicked("scheduleButton"))
makeButton("Tasks", menuContainer, lambda: buttonClicked("tasksButton"))
makeButton("Events", menuContainer, lambda: buttonClicked("eventsButton"))
makeButton("Notes", menuContainer, lambda: buttonClicked("notesButton"))

exitButton = ctk.CTkButton(
    menuContainer, text="Exit", width=200,
    font=("Dubai", 20, "bold"), fg_color="transparent",
    text_color="#243a5e", border_color="#0b2033", border_width=2,
    command=closeApp
)
exitButton.pack(pady=5)

# Schedule Window
makeLabel("Schedule", scheduleWindow)
makeButton("Add Class", scheduleWindow, lambda: setSchedulesPages("addClassWindow"))
makeButton("View Schedule", scheduleWindow, lambda: setSchedulesPages("viewScheduleWindow"))
makeButton("Delete Class", scheduleWindow, lambda: setSchedulesPages("deleteClassWindow"))
makeGoBackButton(scheduleWindow, goToMenu)

# Add Class Window
makeLabel("Add Class", addClassWindow)

classField = makeTextField("Enter class", addClassWindow)
dayField   = makeTextField("Enter day",   addClassWindow)
timeField  = makeTextField("Enter time",  addClassWindow)
roomField  = makeTextField("Enter room",  addClassWindow)

saveDataButton(addClassWindow, lambda: saveDataButtonClicked(classField.get(), dayField.get(), timeField.get(), roomField.get()))

makeGoBackButton(addClassWindow, goToSchedule)

app.mainloop()