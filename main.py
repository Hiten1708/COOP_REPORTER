from os import replace
from tkinter import *
from tkinter import messagebox
import smtplib
from datetime import datetime
import sqlite3

placeholders = ["~[DATE]~", "~[JOB_BOARD]~", "~[JOBS]~"]
mail = "hp19mx@brocku.ca"
pswd = ""
to_send = "hp19mx@brocku.ca"

conn = sqlite3.connect("jobs.db")
c = conn.cursor()

# c.execute("""
#             CREATE TABLE jobs_applied (
#                 date text,
#                 last text,
#                 jobs text
#             )
#         """)


def sender():
    if len(date.get()) == 0 or len(jobs.get()) == 0 or len(board.get()) == 0:
        messagebox.showerror(
            title="Opps", message="Please don't leave any fields")
    else:
        is_ok = messagebox.askokcancel(title="Making sure", message=f"Because you are crackhead, is the data entered: \nDATE: {date.get()}\n"
                                                                    f"JOB BOARD: {board.get()}\n JOBS: {jobs.get()}\n Okay to send?")
        if is_ok:
            inputs = [date.get(), board.get(), jobs.get().replace(",", "\n")]
            with open("letter.txt", "r") as letter:
                letter_contents = letter.read()
                for ph in range(len(placeholders)):
                    letter_contents = letter_contents.replace(
                        placeholders[ph], inputs[ph])
            c.execute(
                "INSERT INTO jobs_applied VALUES (date.get(),board.get(),jobs.get())")
            conn.commit()
            conn.close()

            with smtplib.SMTP("smtp-mail.outlook.com", port=587) as sender:
                sender.starttls()
                sender.login(user=mail, password=pswd)
                sender.sendmail(
                    from_addr=mail,
                    to_addrs=to_send,
                    msg=f"Subject:About co-op job Update \n\n{letter_contents}"
                )
            date.delete(0, END)
            jobs.delete(0, END)
            board.delete(0, END)


def enter_date():
    is_ok = messagebox.askokcancel(
        title="Making sure", message=f"Just to let you know that it will delete the current entry")
    if is_ok:
        date.delete(0, END)
        date.insert(0, datetime.today().strftime("%Y-%m-%d"))


window = Tk()
window.title("REPORTER")
window.minsize(height=700, width=700)

canvas = Canvas(window, width=300, height=300)
canvas.pack()
img = PhotoImage(file="andrew_pic.png")
canvas.create_image(150, 150, image=img)

date_label = Label(text="Date")
date_label.pack()
date = Entry(width=50)
date.pack()
today_date = Button(text="Set today's date", command=enter_date)
today_date.pack()

board_label = Label(text="Job Board")
board_label.pack()
board = Entry(width=50)
board.pack()

jobs_label = Label(text="Jobs applied")
jobs_label.pack()
jobs = Entry(width=50)
jobs.pack()

note_label = Label(
    text="Note: \n Please fill the 'Jobs' input without \nspaces around commas like this:\n [COMPANY]: [POSITION],[COMPANY]: [POSITION],....  ", fg="red")
note_label.pack()


send_msg = Button(text="Send", command=sender)
send_msg.pack()

window.mainloop()
