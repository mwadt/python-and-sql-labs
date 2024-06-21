import os
from prettytable import PrettyTable

class Database:
    def print_prompt (self):
        print('''
Please select what you would like to do:
    1. View all employees
    2. View all companies
    3. Add new employee
    4. Add new company
    5. Update employee
    6. Update company
    7. Delete employee
    8. Delete company
    9. Quit
''')

    def update_entry (self, table_name, id, property, value):
        self.cursor.execute(("UPDATE " + table_name + " SET " + property + " = %s WHERE id = %s"), [value, id])
        self.connection.commit()
    
    def delete_entry (self, table_name, id):
        self.cursor.execute(("DELETE FROM " + table_name + " WHERE id = %s"), [id])
        self.connection.commit()
    
    def view_employees (self, updating):
        if updating:
            print('=========')
            print('Employees')
            print('=========\n')
        else:
            print('==============')
            print('View Employees')
            print('==============\n')

        self.cursor.execute('''
            SELECT
                employees.id, first_name,
                last_name, age, email,
                name AS employer
            FROM
                employees
            LEFT JOIN
                companies
            ON
                employees.company_id = companies.id
            ORDER BY
                employees.id ASC''')
        data = self.cursor.fetchall()
        valid_ids = []

        if updating:
            output_table = PrettyTable(['ID', 'First', 'Last', 'Age', 'Email', 'Employer'])
            for entry in data:
                valid_ids.append(entry[0])
                output_table.add_row([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5]])
        else:
            output_table = PrettyTable(['First', 'Last', 'Age', 'Email', 'Employer'])
            for entry in data:
                output_table.add_row([entry[1], entry[2], entry[3], entry[4], entry[5]])
        
        print(output_table, '\n')

        if not updating:
            input('[Enter] to go back to menu. ')

            os.system('clear')
            self.print_prompt()
        else:
            return valid_ids
    
    def view_companies (self, updating):
        if updating:
            print('=========')
            print('Companies')
            print('=========\n')
        else:
            print('==============')
            print('View Companies')
            print('==============\n')

        self.cursor.execute('SELECT * FROM companies')
        data = self.cursor.fetchall()
        valid_ids = []


        if updating:
            output_table = PrettyTable(['ID', 'Name', 'State'])
            for entry in data:
                valid_ids.append(entry[0])
                output_table.add_row([entry[0], entry[1], entry[2]])
        else:
            output_table = PrettyTable(['Name', 'State'])
            for entry in data:
                output_table.add_row([entry[1], entry[2]])

        print(output_table, '\n')
        
        if not updating:
            input('[Enter] to go back to menu. ')

            os.system('clear')
            self.print_prompt()
        else:
            return valid_ids
    
    def add_employee (self, first, last, age, email, company_id):
        properties = 'first_name, last_name, age, email'
        values = '%s, %s, %s, %s'
        values_list = [first, last, age, email]

        if company_id != 0:
            properties += ', company_id'
            values += ', %s'
            values_list.append(company_id)

        self.cursor.execute(('INSERT INTO employees ' +
                '( ' + properties + ' ) ' +
            'VALUES (' + values + ')')
                , values_list)
        self.connection.commit()
        
        os.system('clear')
        print('New employee added...')
        self.print_prompt()
    
    def add_employee_prompt (self):
        os.system('clear')
        print('================')
        print('Add New Employee')
        print('================\n')
        
        valid_first, valid_last, valid_age, valid_email, valid_add_company = [False, False, False, False, False]
        company_id = 0

        while valid_first == False:
            first_name = input('First name: ')
            if len(first_name) <= 20:
                valid_first = True
            else:
                print('Invalid input. Try again.\n')
        
        while valid_last == False:
            last_name = input('Last name: ')
            if len(last_name) <= 20:
                valid_last = True
            else:
                print('Invalid input. Try again.\n')
        
        while valid_age == False:
            age = input('Age: ')
            try:
                age = int(age)
                valid_age = True
            except ValueError:
                print('Invalid input. Try again.\n')

        while valid_email == False:
            email = input('Email: ')
            if len(email) <= 32:
                valid_email = True
            else:
                print('Invalid input. Try again.\n')
        
        while not valid_add_company:
            add_company_input = input('Add an employer (y/n)? ')
            if add_company_input.lower() == 'y':
                valid_add_company = True
                
                print()
                valid_ids = self.view_companies(True)
                valid_company_id, company_id = [False, 0]

                while not valid_company_id:
                    company_id = input('Please enter the company ID: ')
                    if int(company_id) in valid_ids:
                        company_id = int(company_id)
                        valid_company_id = True
                    else:
                        print('Invalid input. Please try again.\n')
            elif add_company_input.lower() == 'n':
                valid_add_company = True
            else:
                print('Invalid input. Please try again.\n')
        
        self.add_employee(first_name, last_name, age, email, company_id)
    
    def add_company (self, name, state):
        self.cursor.execute('''INSERT INTO companies 
                ( name, state )
            VALUES
                (%s, %s)
            ''', [name, state])
        self.connection.commit()
        
        os.system('clear')
        print('New company added...')
        self.print_prompt()
    
    def add_company_prompt (self):
        os.system('clear')
        print('===============')
        print('Add New Company')
        print('===============\n')
        
        valid_name, valid_state = [False, False]

        while valid_name == False:
            name = input('Company name: ')
            if len(name) <= 20:
                valid_name = True
            else:
                print('Invalid input. Try again.\n')
        
        while valid_state == False:
            state = input("Company state (2 character abbreviation, ex. 'NY'): ")
            if len(state) == 2:
                valid_state = True
            else:
                print('Invalid input. Try again.\n')
        
        self.add_company(name, state)
    
    def update_employee (self):
        print()
        valid_ids = self.view_employees(True)
        employee_id = ''

        valid_id_selected = False
        while not valid_id_selected:
            employee_id = input('Please enter the ID of the employee you would like to update: ')
            
            if int(employee_id) in valid_ids:
                employee_id = int(employee_id)
                valid_id_selected = True
            else:
                print('Invalid input. Please try again.\n')
        
        print('\n===============')
        print('Update Employee')
        print('===============')

        user_updating = True
        while user_updating:
            print('''
What would you like to update?
    1. First name
    2. Last name
    3. Age
    4. Email
    5. Company worked for
    6. Done Updating
            ''')
            
            update_selection = input('> ')
            match update_selection:
                case '1':
                    valid_name, name = [False, '']
                    while not valid_name:
                        name = input('\nNew first name: ')
                        if len(name) <= 20:
                            valid_name = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('employees', employee_id, 'first_name', name)
                case '2':
                    valid_name, name = [False, '']
                    while not valid_name:
                        name = input('\nNew last name: ')
                        if len(name) <= 20:
                            valid_name = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('employees', employee_id, 'last_name', name)
                case '3':
                    valid_age, age = [False, '']
                    while not valid_age:
                        age = input('\nNew age: ')
                        try:
                            age = int(age)
                            valid_age = True
                        except ValueError:
                            print('Invalid input. Try again.\n')
                    
                    self.update_entry('employees', employee_id, 'age', age)
                case '4':
                    valid_email, email = [False, '']
                    while not valid_email:
                        email = input('\nNew email: ')
                        if len(email) <= 32:
                            valid_email = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('employees', employee_id, 'email', email)
                case '5':
                    valid_ids = self.view_companies(True)
                    
                    valid_company_id, company_id = [False, 0]
                    while not valid_company_id:
                        company_id = input('New company ID: ')
                        if int(company_id) in valid_ids:
                            company_id = int(company_id)
                            valid_company_id = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('employees', employee_id, 'company_id', company_id)
                case '6':
                    user_updating = False
                case _:
                    print('Invalid input. Please try again.\n')
        
        os.system('clear')
        print('Employee updated...')
        self.print_prompt()
    
    def update_company (self):
        print()
        valid_ids = self.view_companies(True)
        company_id = ''

        valid_id_selected = False
        while not valid_id_selected:
            company_id = input('Please enter the ID of the company you would like to update: ')
            
            if int(company_id) in valid_ids:
                company_id = int(company_id)
                valid_id_selected = True
            else:
                print('Invalid input. Please try again.\n')
        
        print('\n==============')
        print('Update Company')
        print('==============')

        user_updating = True
        while user_updating:
            print('''
What would you like to update?
    1. Company name
    2. Company state
    3. Done Updating
            ''')
            
            update_selection = input('> ')
            match update_selection:
                case '1':
                    valid_name, name = [False, '']
                    while not valid_name:
                        name = input('\nNew company name: ')
                        if len(name) <= 20:
                            valid_name = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('companies', company_id, 'name', name)
                case '2':
                    valid_state, state = [False, '']
                    while not valid_state:
                        name = input("\nNew company state (2 character abbreviation, ex. 'NY'): ")
                        if len(name) == 2:
                            valid_name = True
                        else:
                            print('Invalid input. Please try again.\n')
                    
                    self.update_entry('companies', company_id, 'state', state)
                case '3':
                    user_updating = False
                case _:
                    print('Invalid input. Please try again.\n')
        
        os.system('clear')
        print('Company updated...')
        self.print_prompt()
    
    def delete_employee (self):
        valid_ids = self.view_employees(True)
        
        employee_id = ''
        valid_id_selected = False

        while not valid_id_selected:
            employee_id = input('Enter the ID of the employee you want to delete: ')
            if int(employee_id) in valid_ids:
                valid_id_selected = True
                employee_id = int(employee_id)
                self.delete_entry('employees', employee_id)
            else:
                print('Invalid input. Please try again.\n')
        
        os.system('clear')
        print('Employee deleted...')
        self.print_prompt()
    
    def delete_company (self):
        valid_ids = self.view_companies(True)
        
        company_id = ''
        valid_id_selected = False

        while not valid_id_selected:
            company_id = input('Enter the ID of the company you want to delete: ')
            if int(company_id) in valid_ids:
                valid_id_selected = True
                company_id = int(company_id)
                self.delete_entry('companies', company_id)
            else:
                print('Invalid input. Please try again.\n')
        
        os.system('clear')
        print('Company deleted...')
        self.print_prompt()
    
    def __init__ (self, connection, cursor):
        self.connection = connection
        self.cursor = cursor


# # SHOW ALL ENTRIES FOR TESTING
# # Show all employee entries
# cursor.execute('SELECT * FROM employees')
# print(cursor.fetchall())

# # Show all company entries
# cursor.execute('SELECT * FROM companies')
# print(cursor.fetchall())

# # Show all role entries
# cursor.execute('SELECT * FROM roles')
# print(cursor.fetchall())