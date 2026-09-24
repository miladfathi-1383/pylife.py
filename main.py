import people
import tasks






def show_main_menu():
    print('-' * 40)
    print(' '* 14, 'Main Memu')
    print('-'* 40)
    print('1.people\n2.tasks\n3.exit')


if __name__ == '__main__':
    while True:
        show_main_menu()
        choice= input('your choice:')
        if choice == '1':
            while True:
                people.show_people_menu()
                choice= input('your choice:')
                if choice == '1':
                    people.get_inforation()
                elif choice == '2':
                    people.show_information()
                elif choice == '3':
                    people.show_search_people()
                elif choice == '4':
                    people.delete_person()
                elif choice == '5':
                    people.update_person()
                elif choice == '6':
                    break
                else:
                    print('please choose correct choice!')
        elif choice== '2':
                while True:
                    tasks.show_tasks_menu()
                    choice= input('your choice:')
                    if choice == '1':
                        tasks.add_tasks()
                    elif choice == '2':
                        print('1.show all tasks\n2.show by person\n3.exit')
                        choice = input('your choice:')
                        if choice == '1':
                            tasks.show_tasks()
                        elif choice == '2':
                            tasks.search_person_task()
                        elif choice == '3':
                            break
                        else:
                            print('please choose correct choice!')
                    elif choice == '3':
                        tasks.search_task()
                    elif choice == '4':
                        tasks.delete_task()
                    elif choice == '5':
                        tasks.update_task()
                    elif choice == '6':
                        tasks.change_status()
                    elif choice == '7':
                        tasks.fiter_tasks()
                    elif choice == '8':
                        break
                    else:
                        print('please choose correct choice!')
            
        elif choice == '3':
            break
            
        else :
            print('please choose correct choice!')


