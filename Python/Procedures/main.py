import customtkinter as ctk
from datetime import datetime, timedelta
import sqlite3
from PIL import ImageTk, Image # Add package to folder
import csv

countdown_time = 10
countdown_on = False
register_form = None
new_time_form = None
label_list = []
checkbox_lst = []
procedure_frame_list = []

selected_checkbox = []

#------------------------
# Countdown Clock Functions
#-----------------------

def count_down():
    global countdown_time
    if countdown_on:
        if countdown_time >=0:
            time = timedelta(seconds=countdown_time)
            clock.configure(text='T-'+ str(time))
        elif countdown_time <0:
            time = timedelta(seconds=abs(countdown_time)) # Use abs to convert to possitive
            clock.configure(text='T+'+ str(time))        

        clock.after(1000, count_down)
        countdown_time -=1

def start_count_down():
    global countdown_on
    countdown_on = True
    start_button.configure(state='disabled')
    count_down()

def stop_count_down():
    global countdown_on
    countdown_on = False
    start_button.configure(state='normal')

#--------------------------------------------
# Add procedure from CSV          
#--------------------------------------------
def add_csv():

    # Open CSV document and loop through each row, and call apply_data to add to db
    with open('procedure.csv','r') as file:
        
        # Read file, set delimiter at ;
        csv_reader = csv.reader(file, delimiter=';')
        
        # Skip first row (rubrics)
        next(csv_reader)

        # Read each row
        for row in csv_reader:
            apply_data(row[0], row[1], row[2], row[3])
           


#---------------------------------------------
#Window to enter information for new procedure
#---------------------------------------------
def add_procedure():
    global register_form
    # Initiate form to register new procedures to db
    register_form = ctk.CTkToplevel(main_window)
    register_form.title("Register procedure")
    register_form.geometry("300x400")

    # Create labels and entry fields
    procedure_label = ctk.CTkLabel(register_form, text="Procedure:")
    procedure_label.pack(pady = (20,0))
    procedure_entry = ctk.CTkEntry(register_form)
    procedure_entry.pack()

    hour_label = ctk.CTkLabel(register_form, text="Hour (From start):")
    hour_label.pack(pady = (10,0))
    hour_entry = ctk.CTkEntry(register_form)
    hour_entry.pack()

    minute_label = ctk.CTkLabel(register_form, text="Remaining minutes:")
    minute_label.pack(pady = (10,0))
    minute_entry = ctk.CTkEntry(register_form)
    minute_entry.pack()

    second_label = ctk.CTkLabel(register_form, text="Remaining seconds:")
    second_label.pack(pady = (10,0))
    second_entry = ctk.CTkEntry(register_form)
    second_entry.pack()

    register_button = ctk.CTkButton(register_form, text="Register Data", command=lambda: apply_data(procedure_entry.get(), hour_entry.get(), minute_entry.get(), second_entry.get()))
    register_button.pack(pady = (20,0))

    csv_button = ctk.CTkButton(register_form, text="From CSV", command=add_csv)
    csv_button.pack(pady = (20,0))


#-----------------------------
#Register entered data to db
#-----------------------------

def apply_data(name, hour, minute, second):
    global register_form
    # Connect to db (or create one)
    conn = sqlite3.connect('proceduresdata.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS procedures (
            id INTEGER PRIMARY KEY,
            procedure TEXT,
            hour INTEGER, 
            minute INTEGER, 
			second INTEGER,
            total INTEGER
        )
    ''')
    # Try to assign all entered info as integers
    try:
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        total = second + minute*60 + hour*3600

        # Insert data to db
        cursor.execute('INSERT INTO procedures (procedure, hour, minute, second, total) VALUES (?, ?, ?, ?, ?)', (name, hour, minute, second, total))
        conn.commit()

    except ValueError:
        print("UwU enter integer please omg")

    # Close the registration window
    if register_form is not None:
        register_form.destroy()
 
    # Close db connection
    conn.close()


#-------------------
# Edit a procedure
#-------------------
def edit_procedure():
    print('Hello')

#-------------------
# Remove a procedure
#-------------------
def remove_procedure():
    print('Helloooo')

#-----------------------
# Register new start time
#-----------------------
def new_time():
    global new_time_form

    # Initiate form to register new procedures to db
    new_time_form = ctk.CTkToplevel(main_window)
    new_time_form.title("Enter new time")
    new_time_form.geometry("250x300")

    hour_label = ctk.CTkLabel(new_time_form, text="Hours:", text_color = "white")
    hour_label.pack()
    hour_entry = ctk.CTkEntry(new_time_form, fg_color = "white", text_color = "black")
    hour_entry.pack()

    minute_label = ctk.CTkLabel(new_time_form, text="Minutes:", text_color = "white")
    minute_label.pack()
    minute_entry = ctk.CTkEntry(new_time_form, fg_color = "white", text_color = "black")
    minute_entry.pack()

    second_label = ctk.CTkLabel(new_time_form, text="Seconds:", text_color = "white")
    second_label.pack()
    second_entry = ctk.CTkEntry(new_time_form, fg_color = "white", text_color = "black")
    second_entry.pack()

    register_button = ctk.CTkButton(new_time_form, text="Register new time", command=lambda: apply_new_time(hour_entry.get(), minute_entry.get(), second_entry.get()))
    register_button.pack(pady=(40,0))

#-----------------------
# Apply new time
#-----------------------

def apply_new_time(hours, minutes, seconds):
    global new_time_form, countdown_time
    try: 
        seconds = int(seconds)
        minutes = int(minutes)
        hours = int(hours)
        
        # if seconds.isdigit():
        #     seconds = 0    
        # if minutes.isdigit():
        #     minutes = 0
        # if hours.isdigit():
        #     hours = 0
            

# Does only work if you enter something into every field

        countdown_time = seconds + minutes * 60 + hours * 3600 
        clock.configure(text='T-'+str(timedelta(seconds=countdown_time)))

    except ValueError:
        print("UwU enter integer please omg")

    # Close the registration window
    if new_time_form is not None:
        new_time_form.destroy()

#-----------------------------
# View all objects in database  You can only press it once, pressing it again breaks it 
#-----------------------------
def view_procedure():
    conn = sqlite3.connect('proceduresdata.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM procedures WHERE procedure IS NOT NULL AND procedure != "" ORDER BY total DESC')
    data = cursor.fetchall()

    for label in label_list:
        label.destroy()

    for frame in procedure_frame_list:
        frame.destroy()
    procedure_frame_list.clear()

    for procedure_check_box in checkbox_lst:
        procedure_check_box.destroy()
    checkbox_lst.clear()

    for int_var in selected_checkbox:
        int_var.destroy() 
    selected_checkbox.clear()


    for i, row in enumerate(data):       

        procedure_text_frame = ctk.CTkFrame(procedure_frame)
        procedure_text_frame.pack(side=ctk.TOP)
        procedure_frame_list.append(procedure_text_frame)

        select = ctk.IntVar(value=1)
        selected_checkbox.append(select)
        selected_checkbox[-1].set(0)

        label = ctk.CTkLabel(procedure_text_frame, text=f'{row[1]}\t\t T- {row[2]}h {row[3]}m {row[4]}s', bg_color='orange', text_color = 'black', width=400, height=30)
        label.pack(pady=5, side=ctk.LEFT)
        label_list.append(label)

        # Make corresponding check boxes for each procedure
        procedure_check_box = ctk.CTkCheckBox(procedure_text_frame, text='', variable=selected_checkbox[-1], command= checkbox, onvalue=1, offvalue=0)
        procedure_check_box.var = selected_checkbox[-1]
        procedure_check_box._onvalue=1
        procedure_check_box._offvalue=0
        procedure_check_box.deselect()
        procedure_check_box.pack(padx=5, side=ctk.RIGHT)
        checkbox_lst.append(procedure_check_box)

    conn.close()

def checkbox():

# Write comment
    for i in range(0, len(selected_checkbox)):
        checkbox = selected_checkbox[i].get()

        if checkbox == 1:
            label_list[i].configure(bg_color ='grey')
            print('Uppdating')
        else:
            label_list[i].configure(bg_color ='orange')
            print('Not working')
        


#-----------------------
# Main Application
#-----------------------

# Main Window
main_window = ctk.CTk()
main_window.title('Raven Procedures')
main_window.iconbitmap(r"raven.ico")
x = main_window.winfo_screenwidth() // 8
y = int(main_window.winfo_screenheight() * 0.05)
main_window.geometry("1250x750+" + str(x) + '+' + str(y))
ctk.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Options Frame
options_frame = ctk.CTkFrame(main_window, width=140)
options_frame.pack(side = ctk.LEFT, fill = ctk.Y)

#Create a canvas
canvas = ctk.CTkCanvas(options_frame, width = 130, height = 130, highlightthickness=0, background='#212121')
canvas.pack(side=ctk.TOP, pady=(20,0)) 

# Create an object of tkinter ImageTk
img = Image.open("raven.png")
resized_image= img.resize((130,130))
new_image= ImageTk.PhotoImage(resized_image)
canvas.create_image(0,0, image=new_image, anchor=ctk.NW)

# Options label
option_label = ctk.CTkLabel(options_frame, text='Procedure Options', font=ctk.CTkFont(size=20, weight='bold'))
option_label.pack(padx = 20, pady=(20,10))

# Add Procedures Button
add_pro_button = ctk.CTkButton(options_frame,text="Add Procedures", command=add_procedure, width=(150), height=(30))  
add_pro_button.pack(padx = 20, pady = 10)

# Edit Procedures Button
edit_procedure_window_button = ctk.CTkButton(options_frame, text="Edit Procedure", command=edit_procedure, width=(150), height=(30))  
edit_procedure_window_button.pack(padx = 20, pady = 10)

# Remove Procedures Button
remove_procedure_window_button = ctk.CTkButton(options_frame, text="Remove Procedure", command=remove_procedure, width=(150), height=(30))  
remove_procedure_window_button.pack(padx = 20, pady = 10)

# Enter new start time Button
new_time_button = ctk.CTkButton(options_frame, text="New Start Time", command=new_time, width=(150), height=(30))  
new_time_button.pack(padx = 20, pady = 10)

# View Procedures Button
view_procedure_window_button = ctk.CTkButton(options_frame, text="View Procedures", command=view_procedure, width=(150), height=(30))  
view_procedure_window_button.pack(padx = 20, pady = 40)

# Countdown frame
countdown_frame = ctk.CTkFrame(main_window, width=900, height=300)
countdown_frame.pack(side = ctk.TOP, pady = 10)

# Countdown Clock as label
clock = ctk.CTkLabel(countdown_frame, text='T-'+str(timedelta(seconds=countdown_time)), font=ctk.CTkFont(size=50, weight='bold'))
clock.pack(pady=(40))
#clock.grid(row = 0, column = 2)

# Start Button
start_button = ctk.CTkButton(countdown_frame,text="Start", command=start_count_down, width=(200), height=(50))  
start_button.pack(side = ctk.LEFT, anchor = ctk.NW, padx = (200, 10))
#start_button.grid(row = 2, column = 2)

# Stop Button
stop_button = ctk.CTkButton(countdown_frame,text="Stop", command=stop_count_down, width=(200), height=(50))
stop_button.pack(anchor = ctk.NE, padx = (10, 200))
#stop_button.grid(row = 2, column = 2) 

# Procedure window
procedure_frame = ctk.CTkScrollableFrame(main_window, width=900, height=490)
procedure_frame.pack(fill = ctk.BOTH)
#procedure_frame.grid(row = 3, column = 2)


main_window.mainloop()