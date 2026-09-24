import json
from functools import wraps
import logger
people = []


class Person:
    def __init__(self , name , age , phone) -> None:
        self.name = name
        self.age = age
        self.phone = phone
    def show_info(self):
        print('name:' , self.name , '\nage:' , self.age , '\nphone:', self.phone)


def load_people():
    global people
    try:
        with open('people.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        people = []
        return
    except json.JSONDecodeError:
        people = []
        print('json problem')
        return
    people = []        
    for person in data:
        person_object = Person(person['name'] , person['age'] , person['phone'])
        people.append(person_object)

load_people()

def show_people_menu():
    print('-'* 40)
    print(' '* 16 , 'People')
    print('-'* 40)
    print('1.add people\n2.show people\n3.search person\n4.delete person\n5.change information\n6.exit')




def get_name():
    while True:
        name = input('name:')
        if  name.strip() == '':
            print('it shoulld contain somthing!')
            continue
        elif len(name)<2 :
            print('name should contain at least 2 len')
            continue
        elif not name.replace(' ' , '').isalpha():
            print('name dont need number!')
            continue
        break
    return name


def get_age():
    while True:
        try:
            age = int (input('age:'))
            if age <= 0 :
                print('age must be bigger than zero!')
                continue
            break
        except ValueError:
            print('write correct age')
    return age


def get_phone(current_person = None):
    while True:
        phone = input('phone:')
        if len(phone)< 11 or len(phone)>11:
            print('number should have 11 digit!')
            continue
        elif not phone.startswith('09'):
            print('phone should start with 09')
            continue
        elif not phone.isdigit():
            print('number shouid contain digit not alphabet')
            continue
        phone_exit = False
        for person in people:
            if person.phone == phone and person is not current_person:
                phone_exit = True
                print('this phone number is in the accounts!')
                break
        if phone_exit :
            continue
        break
    return phone




def get_inforation():
    name = get_name()
    age= get_age()
    phone =get_phone()
    person = Person(name , age , phone)
    people.append(person)
    logger.log_info(f'Person added :{person.name}')
    save_people()

def show_information():
    if len(people)== 0:
        print('-'* 40)
        print('you have no person in app!')
    else:
        for num ,person in enumerate(people, start=1):
            print('*'*40)
            print(num ,'.')
            person.show_info()
            print('*'*40)
            

def delete_person():
    print('*'*40)
    delete_person = input('enter your person you want delete:')
    found = False
    for person in people:
        if delete_person == person.name or delete_person == person.phone:
            print('*'*40)
            print(person.name,' deleted succesfully!')
            people.remove(person)
            logger.log_info(f'Person deleted :{person.name}')
            found = True
            save_people()
            break
    if found == False :
        print(f'we dont find {delete_person} in accounts')


def update_person():
    print('*'*40)
    search = input('enter your person you want to update informatin:')
    found = False
    for person in people:
        if search == person.name or search== person.phone:
            found = True
            while True:
                print('*'*40)
                print('what you want to change?\n1.name\n2.age\n3.phone\n4.all change information\n5.exit')
                choice = input('your choice:')
                print('*'*40)
                if choice == '1':
                    person.name = get_name()
                    print('your name change to ',person.name )
                    print('*'*40)
                    logger.log_info(f'Person change name:{person.name}')
                    save_people()
                    break
                elif choice == '2':
                    person.age = get_age()
                    print('your age change to ',person.age )
                    print('*'*40)
                    logger.log_info(f'Person change age :{person.name}')
                    save_people()
                    break
                elif choice == '3':
                    person.phone = get_phone(person)
                    print('your phone change to ',person.phone )
                    save_people()
                    logger.log_info(f'Person change phone :{person.name}')
                    print('*'*40)
                    break
                elif choice== '4':
                    person.name = get_name()
                    person.age = get_age()
                    person.phone = get_phone(person)
                    print('*'*40)
                    print('your name change to ',person.name )
                    print('your age change to ',person.age )
                    print('your phone change to ',person.phone )
                    print('*'*40)
                    logger.log_info(f'Person change all :{person.name}')
                    save_people()
                    break
                elif choice == '5':
                    break
                else :
                    print('write correct choice!')
            break
    if not found :
        print(f'we dont find {search} in accounts')


def search_person():
    search_term =  input('enter your person you look for:')
    for person in people:
        if search_term in person.name:
            yield person


def show_search_people():
    found = False
    for person in search_person():
        print('*'*40)
        print('name:', person.name,'\nage:',person.age,'\nphone:',person.phone)
        print('*'*40)
        found = True
    if not found :
        print('we dont find in accounts')



def save_people():
    data = []
    for person in people:
        data.append({'name' :person.name,
        'age': person.age,
        'phone': person.phone})
    with open('people.json', 'w') as file:
        json.dump(data , file , indent= 4)










