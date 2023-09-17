import customtkinter as ctk

def start_count_down():
    print('Hello')

def stop_count_down():
    print('Hello')

main_window = ctk.CTk()
main_window.geometry("1250x750")
main_window.title('Raven Procedures')
ctk.set_appearance_mode("dark") # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Options Frame
options_frame = ctk.CTkFrame(main_window, width=140)
options_frame.pack(side = ctk.LEFT, fill = ctk.Y)

# Options label
option_label = ctk.CTkLabel(options_frame, text='Options', font=ctk.CTkFont(size=20, weight='bold'))
option_label.pack(padx = 20, pady=(20,10))


# Main Procedures Button
main_pro_button = ctk.CTkButton(options_frame,text="Main Procedures", command=start_count_down, width=(150), height=(30))  
main_pro_button.pack(padx = 20, pady = 10)


# Engine Pre Procedures Button
engine_pro_button = ctk.CTkButton(options_frame,text="Engine Pre Procedures", command=start_count_down, width=(150), height=(30))  
engine_pro_button.pack(padx = 20, pady = 10)


# Electronic Pre Procedures Button
electronic_pro_button = ctk.CTkButton(options_frame,text="Electronic Pre Procedures", command=start_count_down, width=(150), height=(30))  
electronic_pro_button.pack(padx = 20, pady = 10)
#start_button.grid(row = 2, column = 2)

# Countdown frame
countdown_frame = ctk.CTkFrame(main_window, width=900, height=300)
countdown_frame.pack(side = ctk.TOP, pady = 10)

# Countdown Clock as label
clock = ctk.CTkLabel(countdown_frame, text='count_down', font=ctk.CTkFont(size=50, weight='bold'))
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
