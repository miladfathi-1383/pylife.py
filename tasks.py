import json
from datetime import datetime
from people import people
import logger

tasks = []

class Task():
    def __init__(self , title , description , priority, category , deadline , status ,person , created_time=None) -> None:
        self.title = title
        self.description = description
        self.priority = priority
        self.category = category
        self.deadline = deadline
        self._status = status
        self.person = person
        if created_time == None:
            self.created_time = datetime.now().strftime("%Y-%m-%d | %H:%M")
        else:
            self.created_time = created_time
    @property
    def status(self):
         return self._status
    @status.setter
    def status(self , value):
        valid_status = ['pending' , 'in progress' , 'completed' , 'cancelled']
        for value in valid_status:
            self._status = value
        else:
            print('your status is not correct')       

    def change_status(self , status):
            self.status = status
    def __str__(self) -> str:
        return(
        f'person:{self.person.name}\ntitle: {self.title} \ndescription:{self.description}\npriority:{self.priority}'
        f'\ncategory: {self.category} \ndeadline: {self.deadline} \nstatus: {self.status} '
        f'\ncreated time: {self.created_time}')
    def __repr__(self) -> str:
        return f'Task(title={self.title!r}, status={self.status!r})'
    def __eq__(self, other) :
        if not isinstance(other , Task):
            return False
        return(self.title == other.title and self.deadline == other.deadline and self.created_time == other.created_time)
    def __lt__(self , other):
        if not isinstance(other , Task):
            return NotImplemented
        self_deadline = datetime.strptime(self.deadline, "%Y-%m-%d | %H:%M")
        other_deadline = datetime.strptime(other.deadline, "%Y-%m-%d | %H:%M")
        return self_deadline < other_deadline
        
        






def load_tasks():
    global tasks
    try:
        with open('tasks.json', 'r') as file :
            data = json.load(file)
    except FileNotFoundError:        
        tasks = []
        return
    except json.JSONDecodeError:
        tasks = []
        print('json problem')

        return 
    tasks = []       
    for task in data:
        person_name = task['person']
        selekted_person = None
        for person in people:
            if person.name == person_name:
                selekted_person = person
                break
        task_object = Task(task['title'] , task['description'] , task['priority']
        ,task['category'] , task['deadline'] , task['status'] ,  selekted_person,task['created_time'])
        tasks.append(task_object)


load_tasks()






def save_tasks():
    data = []
    for task in tasks:
        data.append({'title': task.title
        ,'description': task.description
        , 'priority': task.priority
        , 'category': task.category
        , 'deadline': task.deadline
        , 'status': task.status
        , 'created_time': task.created_time
        , 'person': task.person.name} )
    with open('tasks.json', 'w') as file :
        json.dump(data , file , indent=4)


def show_tasks_menu():
    print('-'* 40)
    print(' '* 14 , 'tasks')
    print('-'* 40)
    print('1.add tasks\n2.show tasks\n3.search tasks\n4.delete tasks\n5.change tasks\n6.change status\n7.filter tasks\n8.exit')


def add_tasks():
    print('people:\n')
    for num ,person in enumerate(people, start=1):
        print(num,'.',)
        print(person.name)
    while True:
        try:
            person_number= int(input('your name:'))
            if person_number >len (people) or person_number <=  0 :
                print('you should write correct an answer!')
                continue
            else:
                selected_person = people[person_number -1]
                break
        except:
            print('please enter correct number')
    title = input('title:')
    description = input('description:')
    priority = input('periority:')
    category = input('category:')
    deadline = get_deadline()
    deadline = deadline.strftime("%Y-%m-%d | %H:%M")
    status = "pending"
    task = Task(title , description , priority , category , deadline ,status, selected_person)
    tasks.append(task)
    logger.log_info(f'task added :{task.title}')
    save_tasks()


def show_tasks():
    sorted_task = sorted(tasks)
    if len (tasks) == 0:
        print('you dont have any tasks!')
    else:
        for num ,task in enumerate(sorted_task , start =1):
            print('*'*40)
            print(num,'.',task)

            print('*'*40)
            

def search_person_task():
    print('people:\n')
    for num ,person in enumerate(people, start=1):
        print(num,'.',person.name)
    while True:
        person_number= int(input('your name:'))
        if person_number >len (people) or person_number <=  0 :
            print('you should write correct an answer!')
            continue
        else:
            selected_person = people[person_number -1]
            break
    found = False
    for task in tasks:
        if task.person == selected_person:
            print('*'*40)
            print(num,'.',task)
            print('*'*40)   
            found = True
    if found == False:
        print('we dont find any task for this person!')


def search_task():
    search = input('what you want for search:')
    found =False
    for num ,task in enumerate(tasks, start=1):
        if search in task.title :
            print('*'*40)
            print(num,'.',task)
            print('*'*40)   
            found = True
    if found == False:
        print('*'*40)
        print(search,' is not in the tasks')
        print('*'*40)


def delete_task():
    delete= input('write title that you want to delete:')
    found = False
    for task in tasks:
        if delete == task.title:
            tasks.remove(task)
            logger.log_info(f'task deleted :{task.title}')
            print('this task deleted completly!')
            print('*'*40)
            save_tasks()
            found = True
    if found == False:
        print('*'*40)
        print('we don t find task like this!')


def update_task():
    update = input('the title you ant to edit:')
    found = False
    for task in tasks:
        if task.title== update:
            found = True
            print('1.title\n2.description\n3.priority\n4.category\n5.deadline\n6,change person\n7.change all\n8.exit')
            choice = input('your choice:')
            while True:
                if choice == '1':
                    print('*'*40)
                    new_tatle= input('new title:')
                    task.title = new_tatle
                    print('your title change ', task.title)
                    print('*'*40)
                    logger.log_info(f'task change :{task.title}')
                    save_tasks()
                    break
                elif choice == '2':
                    print('*'*40)
                    new_description= input('new descriptin:')
                    task.description = new_description
                    print('your description change ', task.description)
                    print('*'*40)
                    logger.log_info(f'task change :{task.title}')
                    save_tasks()
                    break
                elif choice == '3':
                    print('*'*40)
                    new_priority= input('new priority:')
                    task.priority = new_priority
                    print('your priority change ', task.priority)
                    print('*'*40)
                    logger.log_info(f'task change :{task.title}')
                    save_tasks()
                    break
                elif choice == '4':
                    print('*'*40)
                    new_category= input('new category:')
                    task.category = new_category
                    print('your category change ', task.category)
                    print('*'*40)
                    logger.log_info(f'task change :{task.title}')
                    save_tasks()
                    break
                elif choice == '5':
                    print('*'*40)
                    new_deadline= input('new deadline:')
                    task.deadline = new_deadline
                    print('your dead line change to', task.deadline)
                    print('*'*40)
                    logger.log_info(f'task change deadline:{task.title}')
                    save_tasks()
                    break
                elif choice == '6':
                    print('people:\n')
                    for num ,person in enumerate(people, start=1):
                        print(num ,'.', person.name)
                    while True:
                        new_person_number= int(input('your new person name:'))
                        if new_person_number >len (people) or new_person_number <=  0 :
                            print('write correct len!')
                            continue
                        else :
                            new_selected_person = people[new_person_number -1]
                            break
                    task.person = new_selected_person
                    print('*'*40)
                    logger.log_info(f'task change person :{task.title}')
                    save_tasks()
                    break

                elif choice == '7':
                    print('*'*40)
                    new_tatle= input('new title:')
                    new_description= input('new descriptin:')
                    new_priority= input('new priority:')
                    new_category= input('new category:')
                    new_deadline= input('new deadline:')
                    task.title = new_tatle
                    task.description = new_description
                    task.priority = new_priority
                    task.category = new_category
                    task.deadline = new_deadline
                    print('your title change to', task.title, '\nyour description change to', task.description)
                    print('your priority change to', task.priority,'\nyour category change to', task.category )
                    print('your title change to', task.deadline)
                    print('*'*40)
                    logger.log_info(f'task change all :{task.title}')
                    save_tasks()
                    break                    
                elif choice == '8':
                    break
                else :
                    print('*'*40)
                    print('write correct choice!')
                    break
            break
    if found == False:
        print('*'*40)
        print('we dont find this title in task!')


def change_status():
    search_status = input('enter the title:')
    found = False
    for task in tasks:
        if task.title== search_status:
            found = True
            print('*'*40)
            print('1.pending\n2.in progress\n3.completed\n4.cancelled\n5.exit')
            choice= input('your choice to install in status:')
            while True:
                if choice == '1':
                    task.change_status('pending')
                    print('your status change to pending', task.status)
                    logger.log_info(f'task status change :{task.title}')
                    save_tasks()
                    break
                elif choice == '2':
                    task.change_status('in progress')
                    print('your status change to in progress' ,task.status)
                    logger.log_info(f'task status change :{task.title}')
                    save_tasks()
                    break
                elif choice == '3':
                    task.change_status('completed')
                    print('your status change to completed ' ,task.status)
                    logger.log_info(f'task status change :{task.title}')
                    save_tasks()
                    break

                elif choice == '4':
                    task.change_status('cancelled')
                    print('your status change to ' ,task.status)
                    logger.log_info(f'task status change to cancelled :{task.title}')
                    save_tasks()
                    break
                elif choice == '5':
                    break
                else:
                    print('write correct choice:')
                    break
            break
    if found == False:
        print('we dont have this title in tasks!')


def find_tasks(tasks, field, value):
    found = False

    for num, task in enumerate(tasks, start=1):
        if getattr(task, field) == value:
            print('*' * 40)
            print(num,'.',task)
            found = True

    if not found:
        print('we dont find tasks!')


def fiter_tasks():
    print('*'*40)
    print('1.filter by status\n2.fiter by priority\n3.filter by category\n4,filter by dead line\n5.exit')
    choice = input('your choice:')
    print('*'*40)
    while True:
        if choice == '1':
            print('*'*40)
            print('1.filter by pending\n2.filter by in progress\n3.completed\n4.cancelled\n5.exit')
            choice2 = input('your choice for filter:')
            print('*'*40)
            if choice2 == '1':
                find_tasks(tasks , 'status' , 'pending')
            elif choice2 == '2':
                find_tasks(tasks , 'status' , 'in progress')
            elif choice2 == '3':
                find_tasks(tasks , 'status' , 'completed')
            elif choice2 == '4':
                find_tasks(tasks , 'status' , 'cancelled')
            elif choice2 == '5':
                break
            else :
                print('choose correct number!')
            
        elif choice == '2':
            print('*'*40)
            print('1.low\n2.medium\n3.high\n4.urgent')
            choice2 = input('your chice:')
            print('*'*40)
            if choice2 == '1':
                find_tasks(tasks , 'priority' , 'low')
            elif choice2 == '2':
                find_tasks(tasks , 'priority' , 'medium')
            elif choice2 == '3':
                find_tasks(tasks , 'priority' , 'high')
            elif choice2 == '4':
                find_tasks(tasks , 'priority' , 'urgent')            
            else :
                print('choose correct number!')
        elif choice == '3':
            print('*'*40)
            catetegory = input('your category:')
            print('*'*40)
            find_tasks(tasks , 'category' , catetegory)
        elif choice == '4':
            year =int(input('year:')) 
            month=int(input('month:')) 
            day=int(input('day:')) 
            filter_time = datetime(year , month , day )
            found = False
            for num ,task in enumerate(tasks, start=1):
                task_deadine = datetime.strptime(task.deadline, "%Y-%m-%d | %H:%M")
                if filter_time.date() == task_deadine.date():
                    print('*'*40)
                    print(num,'.',task)
                    print('*'*40)     
                    found = True
            if found == False:
                print('you dont have task on thid deadline!')
            break
        elif choice == '5':
            break




def get_deadline():
    while True:

        
        try:
            year =int(input('year:')) 
            month=int(input('month:')) 
            day=int(input('day:')) 
            hour =int(input('hour:'))            
            my_date_time = datetime(year , month , day , hour)
            return my_date_time
        except:
            print('please write correct date!')
            continue


