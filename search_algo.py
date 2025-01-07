import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class SearchableComboBox():
    def __init__(self, parent, db_manager, row, col,ALL=False) -> None:
        self.dropdown_id = None
        self.db_manager=db_manager
        self.options = ["All",*db_manager.get_fabrics_list()] if ALL else db_manager.get_fabrics_list()
        self.parent = parent
        self.selected_option=None
        self.row=row
        self.col=col

        # Create a Text widget for the entry field
        wrapper = tk.Frame(self.parent, padx=0, pady=0)
        wrapper.grid(row=self.row, column=self.col)

        self.entry = tk.Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown) 
        self.entry.pack(side=tk.LEFT)
        # Dropdown icon/button
        self.icon = ImageTk.PhotoImage(Image.open("dropdown_arrow.png").resize((16,16)))
        tk.Button(wrapper, image=self.icon, command=self.show_dropdown).pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(self.parent, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        for option in self.options:
            self.listbox.insert(tk.END, option)

        if ALL:
            self.entry.insert(0,"All")
            self.selected_option="All"

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip()
        if not typed_value:
                # If the entry is empty, display all options
                self.listbox.delete(0, tk.END)
                for option in self.options:
                    self.listbox.insert(tk.END, option)
        try:
            typed_value=int(typed_value)
            elem=self.db_manager.get_fabric_name_by_id(typed_value)
            if elem  is  not None:
                self.listbox.delete(0, tk.END)
                self.listbox.insert(tk.END,elem)
            else:
                messagebox.showerror("Error", "No fabric found with the id provided")
                self.listbox.delete(0, tk.END)
                for option in self.options:
                    self.listbox.insert(tk.END, option)
                self.entry.delete(0,tk.END)

        except ValueError:
            typed_value=event.widget.get().strip().lower()
            # Filter options based on the typed value
            self.listbox.delete(0, tk.END)
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        except:
            messagebox.showerror("Error", "Enter a valid search key")
        self.show_dropdown()
    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)

            self.selected_option=selected_option
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)
    def update_listView(self,ALL=False):
        self.options = ["All",*self.db_manager.get_fabrics_list()] if ALL else self.db_manager.get_fabrics_list()
        self.listbox.delete(0, tk.END)
        self.entry.delete(0,tk.END)
        for option in self.options:
            self.listbox.insert(tk.END, option)
        if ALL:
            self.entry.insert(0,"All")
            self.selected_option="All"
            

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(4000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()
