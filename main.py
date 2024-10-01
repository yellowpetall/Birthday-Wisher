import random
from tkinter import *
import pandas
import smtplib
import datetime as dt
import os

BACKGROUND = "#E6E6FA"
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("EMAIL_PASSWORD")

print(f"Email: {my_email}, Password: {password}")


def add_person():
    add_name = name_entry.get()
    add_email = email_entry.get()
    add_year = year_entry.get()
    add_month = month_entry.get()
    add_day = day_entry.get()
    with open("birthdays.csv", "a") as birthdays_file:
        birthdays_file.write(f"\n{add_name},{add_email},{add_year},{add_month},{add_day}")

    name_entry.delete(0, END)
    email_entry.delete(0, END)
    year_entry.delete(0, END)
    month_entry.delete(0, END)
    day_entry.delete(0, END)


def send_email():
    birthdays = pandas.read_csv("birthdays.csv")
    data = pandas.DataFrame(birthdays)
    today = dt.datetime.now()
    sending_to = data[(data["month"] == today.month) & (data["day"] == today.day)]
    sending_list = sending_to.to_dict(orient="records")
    folder_path = 'letter_templates'
    files = os.listdir(folder_path)
    random_file = random.choice(files)
    file_path = os.path.join(folder_path, random_file)
    for items in sending_list:
        with open(file_path, "r") as original_letter:
            original_lines = original_letter.read()
        modified_line = original_lines.replace("[NAME]", items["name"])
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=items["email"],
                msg=f"Subject:Happy Birthday!\n\n{modified_line}")


window = Tk()
window.title("Birthday Wisher")
window.config(bg=BACKGROUND, padx=10, pady=10)
cake_image = PhotoImage(file="cake.png")
canvas = Canvas(width=380, height=400, background=BACKGROUND, highlightthickness=0)
canvas.create_image(190, 190, image=cake_image)
canvas.create_text(190, 370, text="Happy Birthday!", font=("Comic Sans MS", 20), fill="#FFC300")
canvas.grid(row=0, column=0, columnspan=4)

name = Label(text="Name: ", font=("Comic Sans MS", 15), fg="#FFC300", bg=BACKGROUND, highlightthickness=0)
name.grid(row=1, column=0)
email = Label(text="Email: ", font=("Comic Sans MS", 15), fg="#FFC300", bg=BACKGROUND, highlightthickness=0)
email.grid(row=2, column=0)
date = Label(text="Date of Birth: ", font=("Comic Sans MS", 15), fg="#FFC300", bg=BACKGROUND, highlightthickness=0)
date.grid(row=3, column=0)

name_entry = Entry(width=40)
name_entry.grid(row=1, column=1, columnspan=3)
email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=3)
year_entry = Entry(width=12)
year_entry.grid(row=3, column=1)
month_entry = Entry(width=12)
month_entry.grid(row=3, column=2)
day_entry = Entry(width=12)
day_entry.grid(row=3, column=3)

add = Button(text="Add Person", font=("Comic Sans MS", 10), width=45, bg="#FFF0F5", command=add_person)
add.grid(row=4, column=0, columnspan=4)
send = Button(text="Send Today's Birthday Wishes!", font=("Comic Sans MS", 10), width=45, bg="#FFF0F5",
              command=send_email)
send.grid(row=5, column=0, columnspan=4)

window.mainloop()
