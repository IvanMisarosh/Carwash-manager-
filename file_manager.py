# -*- coding: utf-8 -*-
import data_structures


class FileManager:
    def __init__(self, services_filename, employees_filename):
        self.services_filename = services_filename
        self.employees_filename = employees_filename

    def read_services(self):
        data_list = []
        with open(self.services_filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(',')
                data_list.append(data_structures.ServiceType(line[0], float(line[1])))

        return data_list

    def read_employees(self):
        data_list = []
        with open(self.employees_filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.split(',')
                data_list.append(data_structures.Employee(line[0]))

        return data_list

    def write_services(self, services):
        with open(self.services_filename, 'w', encoding='utf-8') as f:
            for service in services:
                f.write(f'{service.name},{service.price}\n')

    def write_employees(self, employees):
        with open(self.employees_filename, 'w', encoding='utf-8') as f:
            for employee in employees:
                f.write(f'{employee.name},\n')


# file_manager = FileManager('services.txt', 'employees.txt')
# services = file_manager.read_services()
# employees = file_manager.read_employees()
#
# for service in services:
#     print(service.name, service.price)
#
# for employee in employees:
#     print(employee)
#
# file_manager.write_services(services)
# file_manager.write_employees(employees)