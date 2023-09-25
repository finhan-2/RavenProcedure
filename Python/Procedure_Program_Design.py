import customtkinter as ctk
from datetime import datetime, timedelta
countdown_time = 1800
countdown_on = False

def count_down():
    global countdown_time
    if countdown_on:
        # tt = datetime.fromtimestamp(countdown_time)
        # string = tt.strftime("%H:%M:%S")
        # display = string
        # clock['text'] = display
        time = timedelta(seconds=countdown_time)
        clock.configure(text='T-'+ str(time))

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






main_window = ctk.CTk()
main_window.title('Raven Procedures')
#main_window.eval("tk::PlaceWindow . center")
x = main_window.winfo_screenwidth() // 8
y = int(main_window.winfo_screenheight() * 0.05)
main_window.geometry("1250x750+" + str(x) + '+' + str(y))
ctk.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Options Frame
options_frame = ctk.CTkFrame(main_window, width=140)
options_frame.pack(side = ctk.LEFT, fill = ctk.Y)

# Options label
option_label = ctk.CTkLabel(options_frame, text='Procedure Options', font=ctk.CTkFont(size=20, weight='bold'))
option_label.pack(padx = 20, pady=(20,10))


# Add Procedures Button
add_pro_button = ctk.CTkButton(options_frame,text="Add Procedures", command=start_count_down, width=(150), height=(30))  
add_pro_button.pack(padx = 20, pady = 10)


# Change Procedures Button
change_pro_button = ctk.CTkButton(options_frame,text="Change Procedures", command=start_count_down, width=(150), height=(30))  
change_pro_button.pack(padx = 20, pady = 10)


# View Procedures Button
view_pro_button = ctk.CTkButton(options_frame,text="View Procedures", command=start_count_down, width=(150), height=(30))  
view_pro_button.pack(padx = 20, pady = 10)
#start_button.grid(row = 2, column = 2)

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
