import tkinter
import tkinter.messagebox
from tkinter import ttk
import customtkinter as ctk
import data_structures
import file_manager
from datetime import time
import datetime


def adjust_service_string(service, service_list):
    # str_len = len(service.name) + len(str(service.price)) + 3 + 4
    str_len = len(service.__str__())
    # print(str_len)
    max_str_len = len(max(service.__str__() for service in service_list))
    # print(max_str_len)

    # for service in service_list:
    #     print(len(service.__str__()))
    #     print(f"{service.__str__()}f")

    if str_len < max_str_len:
        # print(max_str_len - str_len)
        service.name += " " * (max_str_len - str_len - 5)
        # print(len(service.__str__()))
        # print(f"{service.__str__()}f")


class ScrollableEmployeesFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w")
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        for checkbox in self.checkbox_list:
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                return

    def fill_employees(self, employee_list):

        for checkbox in self.checkbox_list:
            checkbox.destroy()
        self.checkbox_list.clear()

        for item in employee_list:
            self.add_item(item)

    def get_checked_items(self):
        return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


class ScrollableServiceFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, item_list, command=None, **kwargs):
        super().__init__(master, **kwargs)

        self.command = command
        self.checkbox_list = []
        for i, item in enumerate(item_list):
            self.add_item(item)

    def add_item(self, item):
        checkbox = ctk.CTkCheckBox(self, text=item)
        if self.command is not None:
            checkbox.configure(command=self.command)
        checkbox.grid(row=len(self.checkbox_list), column=0, pady=(0, 10), sticky="w")
        self.checkbox_list.append(checkbox)

    def remove_item(self, item):
        # print(f"item to delete {item}")
        for checkbox in self.checkbox_list:
            # print(checkbox.cget("text"))
            if item == checkbox.cget("text"):
                checkbox.destroy()
                self.checkbox_list.remove(checkbox)
                # print("deleted")
                return

    def fill_services(self, service_list):

        for checkbox in self.checkbox_list:
            checkbox.destroy()
        self.checkbox_list.clear()

        for item in service_list:
            self.add_item(item)

    def get_checked_items(self):
        return [index for index, checkbox in enumerate(self.checkbox_list) if checkbox.get() == 1]
        # return [checkbox.cget("text") for checkbox in self.checkbox_list if checkbox.get() == 1]


# create a new window (top level)
class ServiceConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.geometry("400x300")
        self.title("Налаштування послуг")

        # making this window top level
        self.transient(self.master)
        self.grab_set()
        self.focus()

        self.services = master.service_list
        self.order_list = master.order_list

        self.main_window = master

        self.service_frame = ServicesConfigFrame(self, width=450, label_text="Виберіть послугу:")

        self.service_frame.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="ns")

        self.add_service_frame = ctk.CTkFrame(self)
        self.add_service_frame.grid(row=1, column=0, padx=(15, 10), pady=(15, 15), sticky="ns")

        self.service_name_label = ctk.CTkLabel(self.add_service_frame, text="Назва послуги:")
        self.service_name_label.grid(row=0, column=0, pady=(0, 10), padx=(15, 15), sticky="w")

        self.service_name_entry = ctk.CTkEntry(self.add_service_frame, width=180, justify=tkinter.CENTER)
        self.service_name_entry.grid(row=0, column=1, pady=(0, 10), padx=(15, 15), sticky="w")

        self.service_price_label = ctk.CTkLabel(self.add_service_frame, text="Ціна послуги:")
        self.service_price_label.grid(row=0, column=2, pady=(0, 10), padx=(10, 15), sticky="w")

        self.service_price_entry = ctk.CTkEntry(self.add_service_frame, width=50, justify=tkinter.CENTER)
        self.service_price_entry.grid(row=0, column=3, pady=(0, 10), padx=(10, 15), sticky="w")

        self.add_button = ctk.CTkButton(self.add_service_frame, text="Додати", width=100, height=24,
                                        command=self.add_button_action)
        self.add_button.grid(row=1, column=0, columnspan=4, pady=(0, 10), padx=5)

    def add_button_action(self):
        result = self.service_frame.add_service(self.service_name_entry.get(), self.service_price_entry.get())

        if result == 1:
            self.service_name_entry.delete(0, tkinter.END)
            self.service_price_entry.delete(0, tkinter.END)


class ServicesConfigFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.delete_button_list = []
        self.edit_button_list = []
        self.name_entry_list = []
        self.price_entry_list = []
        self.edit_frame_list = []
        self.master = master

        self.service_list = master.services

        for service in self.service_list:
            self.add_item(service)

    def add_item(self, item):
        label_string = f"{item.name}   {item.price} грн"

        label = ctk.CTkLabel(self, text=label_string, padx=5, anchor="w", justify="left")

        edit_frame = ctk.CTkFrame(self)

        name_entry = ctk.CTkEntry(edit_frame, width=150, justify=tkinter.CENTER)
        name_entry.insert(0, item.name)
        name_entry.grid(row=0, column=0, padx=(0, 20), sticky="w")

        price_entry = ctk.CTkEntry(edit_frame, width=50, justify=tkinter.CENTER)
        price_entry.insert(0, item.price)
        price_entry.grid(row=0, column=1, sticky="w")

        delete_button = ctk.CTkButton(self, text="Delete", width=100, height=24, fg_color="#ff3300")
        edit_button = ctk.CTkButton(self, text="Edit", width=100, height=24, fg_color="#007399")

        delete_button.configure(command=lambda: self.remove_item(item))
        edit_button.configure(command=lambda: self.edit_item_action(item, name_entry.get(), price_entry.get()))

        # label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")

        edit_frame.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        delete_button.grid(row=len(self.delete_button_list), column=1, pady=(0, 10), padx=5)
        edit_button.grid(row=len(self.edit_button_list), column=2, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.delete_button_list.append(delete_button)
        self.edit_button_list.append(edit_button)
        self.name_entry_list.append(name_entry)
        self.price_entry_list.append(price_entry)
        self.edit_frame_list.append(edit_frame)

    def check_if_service_had_orders(self, service):
        # print(f"service to delete {service.name} {service.price}")
        for order in self.master.order_list:
            if service.name.strip() in order.service_types:
                # print(f"service {service.name} {service.price} had orders")
                res = tkinter.messagebox.askquestion("Помилка",
                                                     "Послуга використовується в замовленнях!\nВидалити її з записів?")
                if res == "yes":
                    # print("yes")
                    self.remove_all_info_about_service(service)
                else:
                    # print("no")
                    return True
        return False

    def remove_all_info_about_service(self, service):
        for order in self.master.order_list:
            if service.name.strip() in order.service_types:

                order.service_types.remove(service.name.strip())

                if len(order.service_types) == 0:
                    self.master.order_list.remove(order)

        self.master.main_window.clear_treeview()
        self.master.main_window.fill_orders_treeview()

    def remove_item(self, item):

        if self.check_if_service_had_orders(item):
            return

        for label, delete_button, edit_button, name_entry, price_entry, edit_frame in zip(self.label_list,
                                                                                          self.delete_button_list,
                                                                                          self.edit_button_list,
                                                                                          self.name_entry_list,
                                                                                          self.price_entry_list,
                                                                                          self.edit_frame_list):

            if f"{item.name}   {item.price} грн" == label.cget("text"):
                label.destroy()
                delete_button.destroy()
                edit_button.destroy()
                name_entry.destroy()
                price_entry.destroy()
                edit_frame.destroy()
                self.label_list.remove(label)
                self.delete_button_list.remove(delete_button)
                self.edit_button_list.remove(edit_button)
                self.name_entry_list.remove(name_entry)
                self.price_entry_list.remove(price_entry)
                self.edit_frame_list.remove(edit_frame)
                self.remove_item_from_list(item)
                return

    def remove_item_from_list(self, item):
        # print(f"item to delete: {item.name} {item.price}")
        for service in self.service_list:
            # print(service.name, service.price)
            if service.name == item.name and service.price == item.price:
                # self.master.main_window.service_type_checkbox_frame.remove_item(service.__str__())
                self.service_list.remove(service)
                self.master.main_window.service_type_checkbox_frame.fill_services(
                    [service.__str__() for service in self.service_list])
                return

    def edit_item_action(self, item, name, price):
        if not self.edit_item(item, name, price):
            for name_entry, price_entry, label in zip(self.name_entry_list, self.price_entry_list, self.label_list):

                if f"{item.name}   {item.price} грн" == label.cget("text"):
                    name_entry.delete(0, tkinter.END)
                    name_entry.insert(0, item.name)
                    price_entry.delete(0, tkinter.END)
                    price_entry.insert(0, item.price)
                    # label.configure(text=f"{item.name}   {float(item.price)} грн")

    def edit_item(self, item, name, price):

        if self.validate_service(name, price) == 0:
            return 0

        if item.name.strip() == name.strip() and item.price == price:
            return 0

        for lable in self.label_list:

            if f"{item.name}   {item.price} грн" == lable.cget("text"):
                lable.configure(text=f"{name}   {float(price)} грн")
                # print("edited")

        item.name = name
        item.price = float(price)

        self.master.main_window.service_type_checkbox_frame.fill_services(
            [service.__str__() for service in self.service_list])

        return 1

    def check_if_already_exists(self, name, price):
        for service in self.service_list:
            if service.name.strip() == name.strip() and service.price == float(price):
                return True
        return False

    def validate_service(self, name, price):
        if name.strip() == "":
            tkinter.messagebox.showerror("Помилка", "Введіть назву послуги!")
            return 0

        if price.strip() == "":
            tkinter.messagebox.showerror("Помилка", "Введіть ціну послуги!")
            return 0

        try:
            float(price)
        except ValueError:
            tkinter.messagebox.showerror("Помилка", "Некоректна ціна! Перевірте введені дані")
            return 0

        if float(price) < 0:
            tkinter.messagebox.showerror("Помилка", "Некоректна ціна!")
            return 0

        if self.check_if_already_exists(name, price):
            tkinter.messagebox.showerror("Помилка", "Така послуга вже існує!")
            return 0

        return 1

    def add_service(self, name, price):

        if self.validate_service(name, price) == 0:
            return 0

        obj = data_structures.ServiceType(name, float(price))

        self.service_list.append(obj)

        adjust_service_string(obj, self.service_list)

        self.add_item(obj)

        self.fill_list()

        # self.master.main_window.service_type_checkbox_frame.add_item(f"{name}   {float(price)} грн")
        self.master.main_window.service_type_checkbox_frame.fill_services(
            [service.__str__() for service in self.service_list])
        return 1

    def fill_list(self):

        for i in range(len(self.label_list)):
            # print(f"i: {i}")
            self.label_list[0].destroy()
            self.delete_button_list[0].destroy()
            self.edit_button_list[0].destroy()
            self.name_entry_list[0].destroy()
            self.price_entry_list[0].destroy()
            self.edit_frame_list[0].destroy()
            self.label_list.remove(self.label_list[0])
            self.delete_button_list.remove(self.delete_button_list[0])
            self.edit_button_list.remove(self.edit_button_list[0])
            self.name_entry_list.remove(self.name_entry_list[0])
            self.price_entry_list.remove(self.price_entry_list[0])
            self.edit_frame_list.remove(self.edit_frame_list[0])

        for service in self.service_list:
            self.add_item(service)


class EmployeeConfigWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.geometry("400x300")
        self.title("Налаштування послуг")

        # making this window top level
        self.transient(self.master)
        self.grab_set()
        self.focus()

        self.employees = master.employee_list
        self.order_list = master.order_list

        self.main_window = master

        self.employee_frame = EmployeesConfigFrame(self, width=450, label_text="Виберіть працівника:")

        self.employee_frame.grid(row=0, column=0, padx=(15, 15), pady=(15, 15), sticky="ns")

        self.add_employee_frame = ctk.CTkFrame(self)
        self.add_employee_frame.grid(row=1, column=0, padx=(15, 10), pady=(15, 15), sticky="ns")

        self.employee_name_label = ctk.CTkLabel(self.add_employee_frame, text="Ім'я працівника:")
        self.employee_name_label.grid(row=0, column=0, pady=(10, 10), padx=(15, 15), sticky="w")

        self.employee_name_entry = ctk.CTkEntry(self.add_employee_frame, width=180, justify=tkinter.CENTER)
        self.employee_name_entry.grid(row=0, column=1, pady=(10, 10), padx=(15, 15), sticky="w")

        self.add_button = ctk.CTkButton(self.add_employee_frame, text="Додати", width=100, height=24,
                                        command=self.add_button_action)
        self.add_button.grid(row=0, column=2, pady=(10, 10), padx=5)

    def add_button_action(self):
        result = self.employee_frame.add_employee(self.employee_name_entry.get())

        if result == 1:
            self.employee_name_entry.delete(0, tkinter.END)


class EmployeesConfigFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.radiobutton_variable = ctk.StringVar()
        self.delete_button_list = []
        self.edit_button_list = []
        self.name_entry_list = []
        self.edit_frame_list = []
        self.master = master

        self.name_list = []

        self.employee_list = master.employees
        for employee in self.employee_list:
            self.add_item(employee)

    def add_item(self, item):

        edit_frame = ctk.CTkFrame(self)
        # print(item.name)

        name_entry = ctk.CTkEntry(edit_frame, width=150, justify=tkinter.CENTER)
        name_entry.insert(0, item.name)
        name_entry.grid(row=0, column=0, padx=(0, 20), sticky="w")

        delete_button = ctk.CTkButton(self, text="Delete", width=100, height=24, fg_color="#ff3300")
        edit_button = ctk.CTkButton(self, text="Edit", width=100, height=24, fg_color="#007399")

        delete_button.configure(command=lambda: self.remove_item(item))
        edit_button.configure(command=lambda: self.edit_item_action(item, name_entry.get()))

        edit_frame.grid(row=len(self.edit_frame_list), column=0, pady=(0, 10), sticky="w")
        delete_button.grid(row=len(self.delete_button_list), column=1, pady=(0, 10), padx=5)
        edit_button.grid(row=len(self.edit_button_list), column=2, pady=(0, 10), padx=5)

        self.delete_button_list.append(delete_button)
        self.edit_button_list.append(edit_button)
        self.name_entry_list.append(name_entry)
        self.edit_frame_list.append(edit_frame)

        self.name_list.append(item.name)

    def check_if_employee_had_orders(self, employee):
        # print(f"employee to delete {employee.name}")
        for order in self.master.order_list:
            if employee in order.employees:
                # print(f"employee {employee.name} had orders")
                res = tkinter.messagebox.askquestion("Помилка",
                                                     "Працівник виконує(виконував) замовлення!"
                                                     "\nВидалити його з записів?")
                if res == "yes":
                    # print("yes")
                    self.remove_all_info_about_employee(employee)
                else:
                    # print("no")
                    return True
        return False

    def remove_all_info_about_employee(self, employee):
        for order in self.master.order_list:
            if employee in order.employees:

                order.employees.remove(employee)

                if len(order.employees) == 0:
                    self.master.order_list.remove(order)

        self.master.main_window.clear_treeview()
        self.master.main_window.fill_orders_treeview()

    def remove_item(self, item):
        # print(f"item to delete {item}")

        if self.check_if_employee_had_orders(item):
            return

        for delete_button, edit_button, name_entry, edit_frame, name in zip(self.delete_button_list,
                                                                            self.edit_button_list, self.name_entry_list,
                                                                            self.edit_frame_list, self.name_list):

            if item.name == name:
                delete_button.destroy()
                edit_button.destroy()
                name_entry.destroy()
                edit_frame.destroy()
                self.delete_button_list.remove(delete_button)
                self.edit_button_list.remove(edit_button)
                self.name_entry_list.remove(name_entry)
                self.edit_frame_list.remove(edit_frame)
                self.remove_item_from_list(item)
                self.name_list.remove(name)
                return

    def remove_item_from_list(self, item):
        for employee in self.employee_list:
            if employee.name == item.name:
                # self.master.main_window.service_type_checkbox_frame.remove_item(service.__str__())
                self.employee_list.remove(employee)
                self.master.main_window.employee_checkbox_frame.fill_employees(
                    [employee.__str__() for employee in self.employee_list])
                return

    def edit_item_action(self, item, name):

        if not self.edit_item(item, name):
            for name_entry in self.name_entry_list:
                if item.name == name_entry.get():
                    name_entry.delete(0, tkinter.END)
                    name_entry.insert(0, item.name)
                    # label.configure(text=f"{item.name}   {item.price} грн")

    def edit_item(self, item, name):

        if self.validate_employee(name) == 0:
            return 0

        if item.name.strip() == name.strip():
            return 0

        # print(f"item name b: {item.name}")
        item.name = name
        # print(f"item name a: {item.name}")

        self.name_list.clear()
        for employee in self.employee_list:
            # print(f"1 {employee.name}")
            self.name_list.append(employee.name)

        # print(self.name_list)

        self.master.main_window.employee_checkbox_frame.fill_employees(
            [employee.__str__() for employee in self.employee_list])

        return 1

    def check_if_already_exists(self, name):
        for employee in self.employee_list:
            if employee.name.strip() == name.strip():
                return True
        return False

    def validate_employee(self, name):
        if name.strip() == "":
            tkinter.messagebox.showerror("Помилка", "Введіть ім'я працівника!")
            return 0

        if self.check_if_already_exists(name):
            tkinter.messagebox.showerror("Помилка", "Працівник з таким іменем вже існує!\nВведіть інше ім'я.")
            return 0

        return 1

    def add_employee(self, name):

        if self.validate_employee(name) == 0:
            return 0

        obj = data_structures.Employee(name)
        self.employee_list.append(obj)
        self.add_item(obj)

        self.fill_list()

        # self.master.main_window.service_type_checkbox_frame.add_item(f"{name}   {float(price)} грн")
        self.master.main_window.employee_checkbox_frame.fill_employees(
            [employee.__str__() for employee in self.employee_list])
        return 1

    def fill_list(self):

        for i in range(len(self.delete_button_list)):
            # print(f"i: {i}")
            self.delete_button_list[0].destroy()
            self.edit_button_list[0].destroy()
            self.name_entry_list[0].destroy()
            self.edit_frame_list[0].destroy()
            self.delete_button_list.remove(self.delete_button_list[0])
            self.edit_button_list.remove(self.edit_button_list[0])
            self.name_entry_list.remove(self.name_entry_list[0])
            self.edit_frame_list.remove(self.edit_frame_list[0])
            self.name_list.remove(self.name_list[0])

        self.name_list.clear()
        for employee in self.employee_list:
            self.add_item(employee)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # self.geometry("900x300")

        self.style = ttk.Style(self)

        self.tk.call("source", "forest-dark.tcl")

        self.style.theme_use("forest-dark")

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.file_manager = file_manager.FileManager('services.txt', 'employees.txt')

        self.employee_list = self.file_manager.read_employees()
        self.service_list = self.file_manager.read_services()

        self.order_list = []

        self.menu_bar_frame = ctk.CTkFrame(self, height=15)
        self.menu_bar_frame.grid(row=0, column=0, columnspan=3, sticky='nsew')

        self.add_order_frame = ctk.CTkFrame(self)
        self.add_order_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')

        self.orders_frame = ctk.CTkFrame(self)
        self.orders_frame.grid(row=1, column=2, rowspan=2, sticky='nsew')

        self.service_config_window = None
        self.employees_config_window = None
        self.profit_window = None

        # orders_frame widgets
        self.style.configure('Custom.Treeview', font=('Calibri', 14))  # Adjust the font size as needed
        self.style.configure('Custom.Treeview.Heading', font=('Calibri', 14))  # Adjust the font size as needed

        self.orders_treeview_frame = ctk.CTkFrame(self.orders_frame)
        self.orders_treeview_frame.grid(row=0, column=0, sticky='nsew')

        self.orders_treeview = ttk.Treeview(self.orders_treeview_frame, show="headings", height=20)
        self.style.map("Custom.Treeview", background=[("selected", "#007399")])

        # Apply the custom style to the Treeview
        self.orders_treeview.tag_configure('Custom.Treeview', font=('Calibri', 14))  # Adjust the font size as needed
        self.orders_treeview.configure(style='Custom.Treeview')

        # Create a vertical scrollbar
        # self.style.configure("Vertical.TScrollbar", background="green", bordercolor="red", arrowcolor="white")
        y_scrollbar = ttk.Scrollbar(self.orders_treeview_frame, orient='vertical', command=self.orders_treeview.yview)
        y_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Create a horizontal scrollbar
        x_scrollbar = ttk.Scrollbar(self.orders_treeview_frame, orient='horizontal', command=self.orders_treeview.xview)
        x_scrollbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        self.orders_treeview.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        self.orders_treeview.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

        cols = ("Час", "Ціна", "Виконавці", "Тип послуги")
        self.orders_treeview["columns"] = cols

        self.orders_treeview.column("Час", width=100, minwidth=100, anchor=tkinter.CENTER)
        self.orders_treeview.column("Ціна", width=70, minwidth=70, anchor=tkinter.CENTER)
        self.orders_treeview.column("Виконавці", width=300, minwidth=100, anchor=tkinter.CENTER)
        self.orders_treeview.column("Тип послуги", width=450, minwidth=100, anchor=tkinter.CENTER)

        # setting up treeview headings
        for col in cols:
            self.orders_treeview.heading(col, text=col)

        # add_menu_bar widgets
        self.menu_segmented_button = ctk.CTkSegmentedButton(self.menu_bar_frame,
                                                            values=["Послуги", "Працівники", "Розрахувати"],
                                                            corner_radius=0,
                                                            command=self.segmented_button_callback)
        self.menu_segmented_button.pack(side=tkinter.LEFT)

        # add_order_frame widgets

        self.time_frame = ctk.CTkFrame(self.add_order_frame)
        self.time_frame.grid(row=1, column=0, sticky='ew', pady=(5, 5), padx=(15, 15))

        self.time_label = ctk.CTkLabel(self.time_frame, text="      З: ")
        self.time_label.grid(row=0, column=0, padx=(15, 5), sticky="ns")

        self.start_hours_entry = ctk.CTkEntry(self.time_frame, width=50, justify=tkinter.CENTER)
        self.start_hours_entry.grid(row=0, column=1, padx=(0, 5), sticky="ns")

        semi_colon_label = ctk.CTkLabel(self.time_frame, text=":")
        semi_colon_label.grid(row=0, column=2, padx=(0, 5), sticky="ns")

        self.start_minutes_entry = ctk.CTkEntry(self.time_frame, width=50, justify=tkinter.CENTER)
        self.start_minutes_entry.grid(row=0, column=3, padx=(0, 5), sticky="ns")

        self.time_label = ctk.CTkLabel(self.time_frame, text="до: ")
        self.time_label.grid(row=0, column=4, padx=(0, 5), sticky="ns")

        self.end_hours_entry = ctk.CTkEntry(self.time_frame, width=50, justify=tkinter.CENTER)
        self.end_hours_entry.grid(row=0, column=5, padx=(0, 5), sticky="ns")

        semi_colon_label = ctk.CTkLabel(self.time_frame, text=":")
        semi_colon_label.grid(row=0, column=6, padx=(0, 5), sticky="ns")

        self.end_minutes_entry = ctk.CTkEntry(self.time_frame, width=50, justify=tkinter.CENTER)
        self.end_minutes_entry.grid(row=0, column=7, padx=(0, 5), sticky="ns")

        self.price_frame = ctk.CTkFrame(self.add_order_frame)
        self.price_frame.grid(row=2, column=0, sticky='ew', pady=(5, 5), padx=(15, 15))

        self.price_label = ctk.CTkLabel(self.price_frame, text="                           Ціна: ",
                                        justify=tkinter.CENTER)
        self.price_label.grid(row=0, column=0, padx=(15, 5), sticky="ns")

        self.price_entry = ctk.CTkEntry(self.price_frame, width=100, justify=tkinter.CENTER)
        self.price_entry.grid(row=0, column=1, padx=(0, 5), sticky="ns")

        self.add_button = ctk.CTkButton(self.add_order_frame, text="Додати", width=100, height=24,
                                        command=self.add_button_action)
        self.add_button.grid(row=3, column=0, padx=(15, 5), pady=(0, 5), sticky="ns")

        self.multiple_choices_frame = ctk.CTkFrame(self.add_order_frame, width=100, height=650)
        self.multiple_choices_frame.grid(row=0, column=0, padx=(15, 15), pady=(0, 15), sticky="ns")

        self.employee_checkbox_frame = ScrollableEmployeesFrame(master=self.multiple_choices_frame, width=100,
                                                                item_list=[employee.__str__() for employee in
                                                                           self.employee_list],
                                                                label_text="Виберіть працівника(ів):")
        self.employee_checkbox_frame.grid(row=0, column=0, padx=(15, 0), pady=(5, 15), sticky="ns")

        self.service_type_checkbox_frame = ScrollableServiceFrame(master=self.multiple_choices_frame, width=230,
                                                                  command=self.services_checkbox_frame_event,
                                                                  item_list=[service.__str__() for service in
                                                                             self.service_list],
                                                                  label_text="Виберіть тип послуги:")
        self.service_type_checkbox_frame.grid(row=0, column=1, padx=(15, 15), pady=(5, 15), sticky="ns")

        self.orders_treeview.bind("<Double-1>", lambda event: self.double_click_event(event))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        # print("destroyed")
        self.file_manager.write_employees(self.employee_list)
        self.file_manager.write_services(self.service_list)
        self.destroy()

    def double_click_event(self, event):
        # identefy region clicked
        region = self.orders_treeview.identify_region(event.x, event.y)
        if region == "separator":
            return
        elif region == "cell":
            row = self.orders_treeview.identify_row(event.y)
            # print(self.orders_treeview.index(row))
            self.edit_order_action(int(self.orders_treeview.index(row)))
        elif region == "heading":
            return

    def edit_order_action(self, index):

        order = self.order_list[index]

        for checkbox in self.employee_checkbox_frame.checkbox_list:
            checkbox.deselect()
            for employee in order.employees:
                if employee.__str__() == checkbox.cget("text"):
                    checkbox.select()

        for checkbox in self.service_type_checkbox_frame.checkbox_list:
            checkbox.deselect()
            for service in order.service_types:
                if service == (checkbox.cget("text")).split("   ")[0].rstrip():
                    checkbox.select()

        self.start_hours_entry.delete(0, tkinter.END)
        self.start_hours_entry.insert(0, order.start_time.strftime("%H"))

        self.start_minutes_entry.delete(0, tkinter.END)
        self.start_minutes_entry.insert(0, order.start_time.strftime("%M"))

        self.end_hours_entry.delete(0, tkinter.END)
        self.end_hours_entry.insert(0, order.end_time.strftime("%H"))

        self.end_minutes_entry.delete(0, tkinter.END)
        self.end_minutes_entry.insert(0, order.end_time.strftime("%M"))

        self.price_entry.delete(0, tkinter.END)
        self.price_entry.insert(0, order.price)

        delete_button = ctk.CTkButton(self.add_order_frame, text="Видалити", width=100, height=24, fg_color="#ff3300",
                                      command=lambda: self.delete_order(index, delete_button))
        delete_button.grid(row=4, column=0, padx=(15, 5), pady=(0, 5), sticky="ns")
        self.add_button.configure(text="Змінити", command=lambda: self.edit_order(index, delete_button),
                                  fg_color="#007399")

    def delete_order(self, index, button):
        button.destroy()
        self.add_button.configure(text="Додати", command=self.add_button_action, fg_color="#007399")
        self.order_list.pop(index)
        self.clear_treeview()
        self.fill_orders_treeview()
        self.clear_add_order_frame()

    def edit_order(self, index, button):

        # print("changes saved")
        result = self.validate_order()

        if result != 0:
            # print(order.price)
            order_ = self.create_order()

            for employee in order_.employees:
                for order in self.order_list:

                    if order is self.order_list[index]:
                        continue

                    if employee in order.employees:

                        if self.check_if_busy(order, order_.start_time, order_.end_time):
                            tkinter.messagebox.showerror("Помилка",
                                                         f"Працівник {employee.name} виконує: {order.service_types}!\n"
                                                         f"Протягом {order.start_time.strftime('%H:%M')}-"
                                                         f"{order.end_time.strftime('%H:%M')}")
                            return 0

            self.order_list.pop(index)
            self.order_list.insert(index, order_)
            # print(order.price)

        self.clear_treeview()
        self.fill_orders_treeview()
        self.clear_add_order_frame()

        self.add_button.configure(text="Додати", command=self.add_button_action, fg_color="#007399")
        button.destroy()

    def clear_add_order_frame(self):
        for checkbox in self.employee_checkbox_frame.checkbox_list:
            checkbox.deselect()

        for checkbox in self.service_type_checkbox_frame.checkbox_list:
            checkbox.deselect()

        self.start_hours_entry.delete(0, tkinter.END)
        self.start_minutes_entry.delete(0, tkinter.END)
        self.end_hours_entry.delete(0, tkinter.END)
        self.end_minutes_entry.delete(0, tkinter.END)
        self.price_entry.delete(0, tkinter.END)

    def fill_orders_treeview(self):
        for order in self.order_list:
            self.add_order_to_treeview(order)

    def services_checkbox_frame_event(self):
        # print(f"checkbox frame modified: {self.service_type_checkbox_frame.get_checked_items()}")
        sum_ = 0
        for index in self.service_type_checkbox_frame.get_checked_items():
            sum_ += self.service_list[index].price

        self.price_entry.delete(0, tkinter.END)
        self.price_entry.insert(0, sum_)

    def create_order(self):
        employees = []
        for employee in self.employee_list:
            if employee.__str__() in self.employee_checkbox_frame.get_checked_items():
                employees.append(employee)

        start_time = time(int(self.start_hours_entry.get()), int(self.start_minutes_entry.get()))
        end_time = time(int(self.end_hours_entry.get()), int(self.end_minutes_entry.get()))

        price = float(self.price_entry.get())

        service_types = []
        for index in self.service_type_checkbox_frame.get_checked_items():
            service_types.append(self.service_list[index].name.strip())

        order = data_structures.Order(employees, start_time, end_time, price, service_types)
        # print(order)

        return order

    def validate_order(self):
        try:
            time(int(self.start_hours_entry.get()), int(self.start_minutes_entry.get()))
            time(int(self.end_hours_entry.get()), int(self.end_minutes_entry.get()))
        except ValueError:
            tkinter.messagebox.showerror("Помилка", "Некоректний час! Перевірте введені дані")
            return 0

        try:
            float(self.price_entry.get())
        except ValueError:
            tkinter.messagebox.showerror("Помилка", "Некоректна ціна! Перевірте введені дані")
            return 0

        if self.start_hours_entry.get() > self.end_hours_entry.get():
            tkinter.messagebox.showerror("Помилка", "Некоректний час! Перевірте введені дані")
            return 0

        if self.start_hours_entry.get() == self.end_hours_entry.get() and self.start_minutes_entry.get() > self.end_minutes_entry.get():
            tkinter.messagebox.showerror("Помилка", "Некоректний час! Перевірте введені дані")
            return 0

        if not self.service_type_checkbox_frame.get_checked_items():
            tkinter.messagebox.showerror("Помилка", "Виберіть тип послуги!")
            return 0

        if self.price_entry.get() == "" or self.price_entry.get() == "0":
            tkinter.messagebox.showerror("Помилка", "Введіть ціну!")
            return 0

        if float(self.price_entry.get()) < 0:
            tkinter.messagebox.showerror("Помилка", "Некоректна ціна!")
            return 0

        if not self.employee_checkbox_frame.get_checked_items():
            tkinter.messagebox.showerror("Помилка", "Виберіть працівника!")
            return 0

    def check_if_employee_is_available(self, employees, start_time, end_time):

        for employee in employees:
            for order in self.order_list:
                if employee in order.employees:
                    # if start_time < order.end_time and end_time > order.start_time:
                    #     return 0
                    if self.check_if_busy(order, start_time, end_time):
                        tkinter.messagebox.showerror("Помилка",
                                                     f"Працівник {employee.name} виконує: {order.service_types}!\n"
                                                     f"Протягом {order.start_time.strftime('%H:%M')}-{order.end_time.strftime('%H:%M')}")
                        return 0

        return 1

    def check_if_busy(self, order, start_time, end_time):
        order_start, order_end = order.start_time, order.end_time

        if start_time < order_end and end_time > order_start:
            return 1

        if start_time < order_end < end_time or start_time < order_start < end_time < order_end:
            return 1

        return 0

    def add_button_action(self):

        result = self.validate_order()

        if result == 0:
            return

        order = self.create_order()

        if not self.check_if_employee_is_available(order.employees, order.start_time, order.end_time):
            # tkinter.messagebox.showerror("Помилка", "Працівник зайнятий!")
            return

        self.order_list.append(order)
        self.add_order_to_treeview(order)
        self.clear_add_order_frame()

    def add_order_to_treeview(self, order):

        start_time = order.start_time.strftime("%H:%M")
        end_time = order.end_time.strftime("%H:%M")

        self.orders_treeview.insert("", "end", values=[f"{start_time}-{end_time}", order.price,
                                                       ", ".join([employee.__str__() for employee in order.employees]),
                                                       ", ".join(order.service_types)])

    def segmented_button_callback(self, value):
        # print("segmented button clicked:", value)
        if value == "Послуги":
            self.open_service_config_window()
        elif value == "Працівники":
            self.open_employees_config_window()
        elif value == "Розрахувати":
            self.open_profit_window()

    def open_service_config_window(self):
        if self.service_config_window is None or not self.service_config_window.winfo_exists():
            self.service_config_window = ServiceConfigWindow(master=self)
            self.menu_segmented_button.set("fuck ctk")
        else:
            self.service_config_window.focus()  # if window exists focus it
            # self.menu_segmented_button.configure(state="disabled")

    def open_employees_config_window(self):
        if self.employees_config_window is None or not self.employees_config_window.winfo_exists():
            self.employees_config_window = EmployeeConfigWindow(master=self)
            self.menu_segmented_button.set("fuck")
        else:
            self.employees_config_window.focus()

    def open_profit_window(self):
        result = self.check_unfinished_orders()
        if not result:
            return

        if self.profit_window is None or not self.profit_window.winfo_exists():
            self.profit_window = ProfitWindow(master=self)
            self.menu_segmented_button.set("non-existatnt option")
        else:
            self.profit_window.focus()

    def check_unfinished_orders(self):
        current_time = datetime.datetime.now().time()
        # print(current_time)

        for order in self.order_list:
            # print(order.end_time)
            if order.end_time > current_time:
                # print("unfinished orders")
                result = tkinter.messagebox.askquestion("Є незавершені замовлення!",
                                                        "Завершити незакінчені замовлення?")
                # Check the user's choice and call the corresponding function

                if result == "yes":
                    self.end_unfinished_orders()
                    return 1
                else:
                    self.menu_segmented_button.set("non-existatnt option")
                    return 0

        return 1

    def end_unfinished_orders(self):
        # set current time as end time for unfinished orders
        current_time = datetime.datetime.now().time()
        for order in self.order_list:
            if order.end_time > current_time:
                order.end_time = current_time

        self.clear_treeview()
        self.fill_orders_treeview()

    def clear_treeview(self):
        for i in self.orders_treeview.get_children():
            self.orders_treeview.delete(i)


class ProfitWindow(ctk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.geometry("400x300")
        self.title("Розрахунок зарплат")

        # making this window top level
        self.transient(self.master)
        self.grab_set()
        self.focus()
        self.master = master

        self.employee_list = master.employee_list
        self.order_list = master.order_list

        self.profit = self.get_profit()
        self.calculate_employees_salaries()

        self.general_info_frame = ctk.CTkFrame(self)
        self.general_info_frame.grid(row=0, column=0, pady=(10, 10), padx=(15, 15))

        self.profit_lable = ctk.CTkLabel(self.general_info_frame, text=f"Загальний прибуток:  {self.profit} грн")
        self.profit_lable.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=(15, 15))

        self.employer_profit_label = ctk.CTkLabel(self.general_info_frame,
                                                  text=f"Прибуток власника: {self.profit / 2} грн")
        self.employer_profit_label.grid(row=1, column=0, pady=(10, 10), padx=(15, 15))

        self.employee_profit_label = ctk.CTkLabel(self.general_info_frame,
                                                  text=f"Прибуток працівників: {self.profit / 2} грн")
        self.employee_profit_label.grid(row=1, column=1, pady=(10, 10), padx=(15, 15))

        self.employee_frame = EmployeesSalaryFrame(self)
        self.employee_frame.grid(row=1, column=0, pady=(10, 10), padx=(15, 15))

        self.checkout_button = ctk.CTkButton(self, text="Розрахувати", width=100, height=24,
                                             command=self.checkout_button_action, fg_color="#ff0000")

        self.checkout_button.grid(row=2, column=0, pady=(0, 10), padx=(15, 15))

        self.bind("<Destroy>", self.nulify_employees_salaries())

    def checkout_button_action(self):
        self.master.order_list.clear()
        # print(len(self.order_list))
        self.master.clear_treeview()
        self.nulify_employees_salaries()
        self.destroy()

    def nulify_employees_salaries(self):
        for employee in self.employee_list:
            employee.salary = 0

    def get_profit(self):
        profit = 0
        for order in self.order_list:
            profit += order.price
        return profit

    def calculate_employees_salaries(self):

        for order in self.order_list:
            for employee in order.employees:
                employee.salary += round((order.price / 2) / len(order.employees), 2)

            # self.order_list.remove(order)


class EmployeesSalaryFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.master = master
        self.radiobutton_variable = ctk.StringVar()
        self.label_list = []
        self.entry_list = []

        self.employee_list = master.employee_list
        for employee in self.employee_list:
            self.add_item(employee)

    def add_item(self, item):
        label = ctk.CTkLabel(self, text=item.name, padx=5, anchor="w")
        salary = ctk.CTkEntry(self, width=100, justify=tkinter.CENTER)
        salary.insert(0, item.salary)
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        salary.grid(row=len(self.entry_list), column=1, pady=(0, 10), padx=5)

        self.label_list.append(label)
        self.entry_list.append(salary)


if __name__ == "__main__":

    app = App()
    app.mainloop()
