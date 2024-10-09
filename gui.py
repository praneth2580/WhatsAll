
import tkinter
import tkinter.messagebox
import customtkinter as ct
from whatsapp import Whatsapp, Message
import pyqrcode

height = 500
width = 600

ct.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ct.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ct.CTk):

    whatsapp_instances = []
    current_instance = None
    qr_label = None

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Whatsapp Broadcast")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ct.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ct.CTkLabel(self.sidebar_frame, text="Whatsapp Accounts", font=ct.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(5, 10))
        
        # new ccount creation button
        self.new_account_btn = ct.CTkButton(self.sidebar_frame, width= 100, corner_radius=5, text='NEW', command=self.newWhatsappInstance)
        self.new_account_btn.grid(row=1, column=0, padx=10, pady=(5, 10))

        self.appearance_mode_label = ct.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ct.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = ct.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ct.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # set default values
        self.appearance_mode_optionemenu.set("Light")
        self.scaling_optionemenu.set("100%")

    def newWhatsappInstance(self):
        self.current_instance = Whatsapp()
        self.current_instance.QR_CHANGE_LISTENER = self.show_QR
        msg = Message(msg='HI', phone_no='7506738809')
        self.current_instance.addMSG(message=msg)
        self.whatsapp_instances.append(self.current_instance)

    def show_QR(self, qr):
        if self.qr_label:
            self.qr_label.destroy()
        if qr != None:
            qr_code = pyqrcode.create(qr)
            qr_code_xbm = qr_code.xbm(scale=5)
            print(qr)
            code_bmp = tkinter.BitmapImage(data=qr_code_xbm)
            code_bmp.config(background="white")
            self.qr_label = ct.CTkLabel(self,image=code_bmp)
            self.qr_label.grid(row=2, column=1, padx=20, pady=(10, 20))

    def open_input_dialog_event(self):
        dialog = ct.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ct.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()