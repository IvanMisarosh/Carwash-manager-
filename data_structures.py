from datetime import time
import datetime

# Допрацювати класи, щоб не можна було одного і того ж працівника записувати в один і той же час на різні послуги
class Employee:
    def __init__(self, name):
        self.name = name
        self.salary = 0.0

    def __str__(self):
        return str(self.name)


# # get a system time
# def get_time():
#     return datetime.datetime.now().time()
#
# # 17:57:07.195694
#
# print(get_time())

class ServiceType:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return str(self.name + "   " + str(self.price) + " грн")


class Order:
    def __init__(self, employees, start_time, end_time, price, service_types):
        self.employees = employees
        self.start_time = start_time
        self.end_time = end_time
        self.price = price
        self.service_types = service_types

    def __str__(self):
        return str(self.employees) + " " + str(self.start_time) + " " + str(self.end_time) + " " + str(self.price) + " " + str(self.service_types)


