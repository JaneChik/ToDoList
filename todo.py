import re
import os

def start(path_to_file):
    global all_lists
    all_lists = {}
    global name
    name = str
    global file
    file = path_to_file
    if os.path.exists(file):
        with open(file, 'r') as database:
            if os.path.getsize(file) > 0:
                for line in database:
                    key, value = line.strip().split('*and*')
                    value_2 = []
                    if value == '[]':
                        value_2 = []
                    else:
                        for item in value.split('\t'):
                            value_2.append(item)
                    all_lists[key] = value_2
    else:
        with open(file, 'w') as database:
            pass


def save_and_close():
    with open(file, 'w') as file_data:
        for elem in all_lists:
            line_2 = ''
            if all_lists[elem] == []:
                line_2 += '[]'
            else:
                for item in all_lists[elem]:
                    line_2 += item + '\t'
            line = str(elem)+'*and*'+line_2+'\n'
            file_data.write(line)


def new_list(*names: str):
    for item in names:
        all_lists[item] = []


def delete_list(name):
    del all_lists[name]


def work_with(name_of_list):
    global name
    name = name_of_list


def all_my_lists():
    print('My lists:')
    j = 1
    for i in all_lists:
        print(str(j) + '. ' + i)
        j+=1


def all_my_lists_t():
    j = 1
    for i in all_lists:
        print(str(j) + '. ' + i)
        n = 1
        for t in all_lists[i]:
            print('\t' + str(n) + ') ' + t)
            n += 1
        j += 1


def new_task(*tasks: str):
    for item in tasks:
        if ', ' in item:
            dead = re.search('\,\s\d+$', item)
            dead_line = int(dead.group(0)[2:])
            task = re.search('.+\,', item).group(0)[:-1]
            if dead_line is not None:
                task += ' (days left: ' + str(dead_line) + ')'
            all_lists[name].append(task)
        else:
            all_lists[name].append(item)


def timeline(n_task=None):
    if n_task is not None and 'days left: ' not in all_lists[name][n_task - 1]:
        print(f'No deadlines for {all_lists[name][n_task - 1]}')
    elif n_task is not None and 'DONE' not in all_lists[name][n_task - 1]:
        print(all_lists[name][n_task - 1])
        print('TODAY ', end='')
        string = all_lists[name][n_task - 1]
        right_number = re.search('\d+\)', string)
        right_number = int(right_number.group(0)[:-1])
        scale = ['|#'+str(i+1)+'#|' for i in range(right_number)]
        for i in scale:
            print(i, end='-')
        print('--!!!DEADLINE!!!')
    else:
        for n in range(len(all_lists[name])):
            if 'days left: ' in all_lists[name][n] and 'DONE' not in all_lists[name][n]:
                print(all_lists[name][n])
                print('TODAY ', end='')
                string = all_lists[name][n]
                right_number = re.search('\d+\)', string)
                right_number = int(right_number.group(0)[:-1])
                scale = ['|#' + str(i + 1) + '#|' for i in range(right_number)]
                for i in scale:
                    print(i, end='-')
                print('--!!!DEADLINE!!!')
                print()


def show_list():
    print(name + ':')
    for i in range(len(all_lists[name])):
        print(str(i+1) + '. ' + all_lists[name][i])
    tasks = []
    for i in range(len(all_lists[name])):
        if 'DONE' in all_lists[name][i]:
            tasks.append(str(i+1) + '. ' + all_lists[name][i])
    print('Progress:', str(len(tasks)) + '/' + str(len(all_lists[name])), '->',
          format(len(tasks) * 100 / len(all_lists[name]), '.2f'), '% done')
    percent = ['-' for i in range(50)]
    for k in range(int(len(tasks) * 100 / len(all_lists[name])/2)):
        percent[k] = '#'
    print('0', end=' |')
    for i in percent:
        print(i, end='')
    print('> 100%')
    marker = [' ' for i in range(50)]
    marker[12], marker[23], marker[34] = '25%', '50%', '75%'
    print(' ', end='')
    for h in marker:
        print(h, end='')
    print()


def delete_task(number: int):
    all_lists[name].remove(all_lists[name][number-1])


def task_done(number: int):
    all_lists[name][number-1] += ' |DONE|'


def tasks_to_do():
    tasks = []
    print('Tasks to do from "' + name + '":')
    for i in range(len(all_lists[name])):
        if 'DONE' not in all_lists[name][i]:
            tasks.append(str(i+1) + '. ' + all_lists[name][i])
    if len(tasks) == 0:
        answer = input(f'All tasks from "{name}" are done. Would you like to delete this list? yes/no ')
        if answer == 'yes':
            delete_list(name)
    else:
        for item in tasks:
            print(item)
        print('Need to be done:', str(len(tasks)) + '/' + str(len(all_lists[name])), '->',
              format(len(tasks)*100/len(all_lists[name]),'.2f'), '% not finished')


def info(command = None):
    inform = {'start': 'before working with lists, specify path to txt-file as database (existing or create new)',
              'new_list(name of the list)': 'create new todo-list',
              'delete_list(name of list)': 'delete specified todo-list',
              'all_my_lists': 'print all your existing lists',
              'all_my_lists_t': 'print all your lists with all tasks',
              'work_with(list)': 'specifies the list you want to work with now',
              'new_task(your new task)': 'add new task to the list',
              'delete_task(task number)': 'delete this task',
              'show_list': 'print all your tasks from this list',
              'task_done(task number)': 'mark task as DONE, if all done ask if you want to delete this list',
              'tasks_to_do': 'print all tasks that are undone yet',
              'timeline': 'see how much time you have before deadline for each undone task',
              'save_and_close': 'save your progress in txt file, no arguments needed'}
    if command is not None:
        print(command + ': ' + inform[command])
    else:
        for com in inform:
            print(com + ': ' + inform[com])




