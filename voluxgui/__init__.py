from volux import VoluxModule
import tkinter as tk
from tkinter import ttk

class VoluxGui(VoluxModule):
    def __init__(self, shared_modules=[], *args, **kwargs):
        super().__init__(
            module_name="Volux GUI",
            module_attr="gui",
            module_get=self.get,
            module_set=self.set,
            shared_modules=shared_modules
        )

        self.root = tk.Tk()
        self.mainApp = MainApplication(self.root,self,style="mainApp.TFrame")
        self.example_val = 0

    def get(self):

        return self.decoy_val

    def set(self, new_val):

        self.example_val = new_val

    def init_window(self):

        self.gui_style = ttk.Style()
        self.gui_style.configure('mainApp.TFrame', background="#19191B")

        self.mainApp.pack(side="top", fill=tk.BOTH, expand=True)
        self.root.title("Volux")
        screen_size = (self.root.winfo_screenwidth(), self.root.winfo_screenheight())
        self.root.geometry("{}x{}+{}+{}".format(
            800,
            500,
            1920-800,
            1080-500
        )) # define the size of the window
        self.mainApp._update_loop()
        self.root.mainloop()

class MainApplication(ttk.Frame):
    def __init__(self,parent,module_root,*args,**kwargs):
        ttk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent = parent
        self.module_root = module_root
        self.ext_modules = self.module_root._shared_modules

        print("(VoluxGUI) shared modules:",self.ext_modules)

        self.wip_notice = ttk.Label(self,text="NOTE: GUI IS A WORK-IN-PROGRESS",anchor=tk.CENTER)
        self.wip_notice.pack(side="top",fill=tk.X)

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(side="left",fill=tk.Y,padx="14px",pady="14px")

        self.input_label = ttk.Label(self.input_frame,text="INPUTS")
        self.input_label.pack(side="top",fill=tk.BOTH)

        self.input_listbox = tk.Listbox(self.input_frame, selectmode=tk.SINGLE, exportselection=False)
        self.input_listbox.pack()

        self.input_testget = ttk.Button(self.input_frame,text="Get Test",command=self._get_test)
        self.input_testget.pack()

        self.output_frame = ttk.Frame(self)
        self.output_frame.pack(side="left",fill=tk.Y,padx="14px",pady="14px")

        self.output_label = ttk.Label(self.output_frame,text="OUTPUTS")
        self.output_label.pack(side="top",fill=tk.BOTH)

        self.output_listbox = tk.Listbox(self.output_frame, selectmode=tk.SINGLE, exportselection=False)
        self.output_listbox.pack()

        self.output_testset = ttk.Button(self.output_frame,text="Set Test",command=self._set_test)
        self.output_testset.pack()

        self.output_testset_data = ttk.Entry(self.output_frame)
        self.output_testset_data.pack()

        self._update_input_listbox()
        self._update_output_listbox()

    def _update_loop(self):

        pass

    def _get_test(self):

        i = self.input_listbox.curselection()[0]
        get_result = self.ext_modules[i].get()
        print("(VoluxGui) get method response:",get_result)

    def _set_test(self):

        i = self.output_listbox.curselection()[0]
        get_result = self.ext_modules[i].set(int(self.output_testset_data.get()))
        print("(VoluxGui) set method response:",get_result)

    def _update_input_listbox(self):

        for i in range(len(self.ext_modules)):

            module = self.ext_modules[i]

            if hasattr(module,'get'):

                self.input_listbox.insert(tk.END,module._module_name)

    def _update_output_listbox(self):

        for i in range(len(self.ext_modules)):

            module = self.ext_modules[i]

            if hasattr(module,'set'):

                self.output_listbox.insert(tk.END,module._module_name)

    def _get_selected_mdevices(self):
        devices_to_return = [self.parent.mlifx.managed_devices[device_i] for device_i in device_indexes]
        return devices_to_return # return a tuple of indexes for selected items
