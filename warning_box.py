import customtkinter as ctk

def show_warning(message):
    warning_box = ctk.CTkToplevel() 

    warning_box.title("Warning")

    warning_box.grab_set()           
    warning_box.focus()              
    warning_box.lift()

    screen_width = warning_box.winfo_screenwidth()
    screen_height = warning_box.winfo_screenheight()
    window_width = 400
    window_height = 150
    position_top = int(screen_height / 2 - window_height / 2)
    position_right = int(screen_width / 2 - window_width / 2)
    warning_box.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}') 
   
    label = ctk.CTkLabel(warning_box, text=message, font=("Arial", 14))
    label.pack(pady=20)
    
    button = ctk.CTkButton(warning_box, text="OK", command=warning_box.destroy)
    button.pack(pady=10)
