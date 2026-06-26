import customtkinter
import tkinter as tk
import subprocess
import os
import signal
import sys
from tkinter import filedialog

process = None
PID_FILE = "remaps.pid"
filepath = r""


class App(customtkinter.CTk):
    width = '400' 
    height = '350'
    customtkinter.set_default_color_theme("green")
    def __init__(self):
        super().__init__()


        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False,False)


        self.frame = customtkinter.CTkFrame(self,fg_color='#3a3a3c',border_width=3,corner_radius=3,border_color='#585858')
        self.frame.grid(padx=25, pady=25) 
        self.frame.configure(width=350, height=300)


        self.drop = tk.Menu(self)

        theme_menu = tk.Menu(self.drop,tearoff=0)
        theme_menu.add("command",label="Dark",command=lambda: customtkinter.set_appearance_mode("Dark")
                       )
        theme_menu.add("command",label="Light",command=lambda: customtkinter.set_appearance_mode("Light")
                       )
        theme_menu.add("command",label="Color_theme Green", command=lambda: self.change_theme("green")
                       )
        theme_menu.add("command",label="Color_theme dark blue", command=lambda: self.change_theme("dark-blue")
                       )
        theme_menu.add("command",label="Color_theme blue", command=lambda: self.change_theme("blue")
                       )
        

        options_menu = tk.Menu(self.drop,tearoff=0)
        options_menu.add("command",label="Exit",command=lambda: sys.exit()
                         )
        options_menu.add_command(label="Opacity", command=self.set_opacity
                                 )
        options_menu.add_command(label="Change file",command=self.get_new_file
                                 )


        self.drop.add_cascade(label="Options", menu=options_menu)
        self.drop.add_cascade(label="Themes", menu=theme_menu)

        self.config(menu=self.drop)


        self.btn_terminate = customtkinter.CTkButton(self.frame,text='Stop the script',corner_radius=32,border_width=2,font=('Arial Bold Italic',12),command=self.stop)
        self.btn_terminate.place(relx=0.5,rely=0.85,anchor="center")

        self.btn = customtkinter.CTkButton(self.frame,text='Remap Keys',corner_radius=32,border_width=2,font=('Arial Bold Italic',12),command=self.remap)
        self.btn.place(relx=0.5,rely=0.55,anchor="center")

        self.btn_clear = customtkinter.CTkButton(self.frame,text="Clear Remaps",corner_radius=32,border_width=2,font=('Arial Bold Italic',12),command=self.clear)
        self.btn_clear.place(relx=0.3,rely=0.65)

        self.label = customtkinter.CTkLabel(self.frame,text='Enter Keys To Remap',font=('Arial Bold Italic',20))
        self.label.place(relx=0.5,rely=0.2,anchor="center")

        self.entry1 = customtkinter.CTkEntry(self.frame)
        self.entry1.place(relx=0.05,rely=0.35)

        self.entry2 = customtkinter.CTkEntry(self.frame)
        self.entry2.place(relx=0.55,rely=0.35)

    def remap(self):
        global process
        if not os.path.exists(filepath):
            with open(filepath,"w") as f:
                f.write('')
        key1 = self.entry1.get()
        key2 = self.entry2.get()
        self.entry1.delete(0, 'end')
        self.entry2.delete(0, 'end')


        with open(filepath) as file:
            lines = file.readlines()
        lines = lines[1:-1]

        with open(filepath, 'w') as f:
            f.write("import keyboard\n")
            if len(key1) > 1 and len(key2) > 1:
                f.writelines(lines)  
                f.write(f"keyboard.remap_hotkey('{key1}', '{key2}')\n")
                f.write(f"keyboard.remap_hotkey('{key2}', '{key1}')\n")
            else:
                f.writelines(lines)
                f.write(f"keyboard.remap_key('{key1}', '{key2}')\n")
                f.write(f"keyboard.remap_key('{key2}', '{key1}')\n")
            f.write("keyboard.wait()\n")

        process = subprocess.Popen(['python', filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        with open(PID_FILE, 'w') as pid_file:
            pid_file.write(str(process.pid))

    def stop(self):
        global process
        pid = None

        if os.path.exists(PID_FILE):
            with open(PID_FILE, 'r') as pid_file:
                pid = pid_file.read().strip()
                
        if pid:
            os.kill(int(pid), signal.SIGINT)
            if process:
                process.wait()

            process = None
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)


    def clear(self):
        with open(filepath,'w') as f:
            f.write('')

    def set_opacity(self):

        opacity_window = customtkinter.CTkToplevel(self)
        opacity_window.configure(width=260, height=100)
        opacity_window.title("Set Opacity")
        opacity_window.attributes("-topmost", True)

        label_op = customtkinter.CTkLabel(opacity_window,text="Set opacity")
        label_op.place(relx=0.5,rely=0.1,anchor="center")

        scale = customtkinter.CTkSlider(opacity_window, from_=0, to=100)
        scale.set(100)
        scale.place(relx=0.45,rely=0.5,anchor="center")


        def update_opacity(value):
            value = scale.get()            
            self.attributes("-alpha", float(value)/100)
            label_amount.configure(text=f'{round(float(value),2)}%')


        label_amount = customtkinter.CTkLabel(opacity_window, text="100%")
        label_amount.place(relx=0.9, rely=0.5, anchor="center")


        scale.configure(command=update_opacity)

    def get_new_file(self):
        global filepath
        filepath = filedialog.askopenfilename()
        return filepath
    
    def change_theme(self,theme):
            customtkinter.set_default_color_theme(theme)
            self.rebuild_widgets()

    def rebuild_widgets(self):

        self.frame.destroy()
        self.frame = customtkinter.CTkFrame(self, fg_color='#3a3a3c', border_width=3, corner_radius=3, border_color='#585858')
        self.frame.grid(padx=25, pady=25)
        self.frame.configure(width=350, height=300)

        self.btn_terminate = customtkinter.CTkButton(self.frame, text='Stop the script', corner_radius=32, border_width=2, font=('Arial Bold Italic', 12), command=self.stop)
        self.btn_terminate.place(relx=0.5, rely=0.85, anchor="center")

        self.btn = customtkinter.CTkButton(self.frame, text='Remap Keys', corner_radius=32, border_width=2, font=('Arial Bold Italic', 12), command=self.remap)
        self.btn.place(relx=0.5, rely=0.55, anchor="center")

        self.btn_clear = customtkinter.CTkButton(self.frame, text="Clear Remaps", corner_radius=32, border_width=2, font=('Arial Bold Italic', 12), command=self.clear)
        self.btn_clear.place(relx=0.3, rely=0.65)

        self.label = customtkinter.CTkLabel(self.frame, text='Enter Keys To Remap', font=('Arial Bold Italic', 20))
        self.label.place(relx=0.5, rely=0.2, anchor="center")

        self.entry1 = customtkinter.CTkEntry(self.frame)
        self.entry1.place(relx=0.05, rely=0.35)

        self.entry2 = customtkinter.CTkEntry(self.frame)
        self.entry2.place(relx=0.55, rely=0.35)


if __name__ == "__main__":
    app = App()
    app.mainloop()


