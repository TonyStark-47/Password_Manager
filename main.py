from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B',
        'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []

    password_list += [
        random.choice(letters) for _ in range(random.randint(8, 10))
    ]
    password_list += [
        random.choice(symbols) for _ in range(random.randint(2, 4))
    ]
    password_list += [
        random.choice(numbers) for _ in range(random.randint(2, 4))
    ]

    random.shuffle(password_list)

    generated_password = "".join(char for char in password_list)

    # update/populate the password entry box
    password.delete(0, END)
    password.insert(END, string=generated_password)

    # copy to clipboard
    pyperclip.copy(generated_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """ Saves the input details."""

    website = website_name.get().title()
    username = email.get()
    passwd = password.get()
    new_data = {
        website: {
            "email": username,
            "password": passwd,
        }
    }

    # confirming the data
    #checking if any fields are empty..
    if website != '' and username != '' and passwd != '':
        is_ok = messagebox.askokcancel(
            title=f"{website}",
            message=
            f"Confirm your details: \nEmail: {username} \nPassword: {passwd}\n"
        )
        if is_ok:
            # saving the form data
            try:
                with open(file="data.json", mode='r') as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open(file="data.json", mode='w') as data_file:
                    json.dump(new_data, data_file,
                              indent=4)  #indent make the data easy to read.
            else:
                # updating old data with new data
                data.update(new_data)
                with open(file="data.json", mode='w') as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                # clearing the form data from box except email.
                website_name.delete(first=0,
                                    last=END)  # first index to last index
                password.delete(first=0, last=END)
                website_name.focus()
    else:
        # empty fields warning
        messagebox.showwarning(title="Oops!",
                               message="Please don't leave any fields empty!")


# --------------------------- FIND PASSWORD --------------------------- #
def find_password():
    user_entry = website_name.get().title()
    try:
        with open("data.json", 'r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found!")
    else:
        if user_entry in data:
            user_email = data[user_entry]['email']
            user_passwd = data[user_entry]['password']
            messagebox.showinfo(
                title=f"{user_entry}",
                message=f"email: {user_email} \nPassword: {user_passwd}")
        else:
            messagebox.showwarning(
                title="Nope!", message=f"No details for {user_entry} exists.")


# ---------------------------- UI SETUP ------------------------------- #
# Display
window = Tk()
window.title("Password Manager")
window.configure(padx=60, pady=60)

# Logo
logo_path = "logo.png"
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file=logo_path)
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Label
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password")
password_label.grid(row=3, column=0)

# Entry
website_name = Entry(width=25)
website_name.grid(row=1, column=1)
website_name.focus()

email = Entry(width=45)
email.insert(index=0,
             string="tonystark@gmail.com")  # default email when filling.
email.grid(row=2, column=1,
           columnspan=2)  # columnspan = no. of cols widgets going to use.

password = Entry(width=25)
password.grid(row=3, column=1)

# Button
generate_passwd_button = Button(text="Generate Password",
                                command=generate_password)
generate_passwd_button.grid(row=3, column=2)

add_button = Button(text="Add", width=42, command=save)
add_button.grid(row=4, column=1, columnspan=2)

search_button = Button(text="Search", width=16, command=find_password)
search_button.grid(row=1, column=2)

window.mainloop()
