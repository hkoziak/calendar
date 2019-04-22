# from enum import Enum
import jsonpickle as jsp


class Client:
    '''
    This class represents a client with company name and id attributes.
    '''
    def __init__(self, name, serial_number):
        '''
        Initializes object as Client's class instance.
        '''
        self.name = name
        self.id = serial_number

    def __str__(self):
        '''
        String view for Client's instances.
        '''
        return "Company: {}, serial number - {}".format(self.name, self.id)


class Seller:
    '''
    This class represents a seller with name, surname and id attributes.
    '''
    def __init__(self, name, surname, serial_number):
        '''
        Initializes object as Seller's class instance.
        '''
        self.name = name
        self.surname = surname
        self.id = serial_number

    def __str__(self):
        '''
        String view for Seller's instances.
        '''
        return "Seller: Mr(Mrs) {} {}".format(self.name, self.surname)


class Task:
    '''
    Task class represents one particular task.
    Task attributes "client" and "seller" must be Client and Seller objects
    respectivily.
    '''
    def __init__(self, t_type, status, client, seller, date, description, \
                 serial_number):
        '''
        Initializes object as Task's class instance.
        '''
        self.t_type = t_type
        self.status = status
        self.client = client
        self.seller = seller
        self.date = date
        self.description = str(description)
        self.id = serial_number


class Tasks:
    '''
    "Tasks" class represents a number of tasks.
    The only one required attribute is list of Task's class objects.
    '''
    # Needed to save and work with all available information
    # The most convenient way to pass our data type with API is to store it in
    # "Tasks" object.
    def __init__(self, lst_of_tasks):
        '''
        Initializes object as Task's class instance.
        '''
        self.tasks = lst_of_tasks

    def save_to_file(self):
        '''
        Saves and encodes object in json format.
        '''
        f = open("tasks_{}.json".format(self), "w+")
        f.write(jsp.encode(self.lst_of_tasks))
        f.close()

    def render_as_html(self):
        pass

    def add(self, task):
        self.lst_of_tasks.append(task)

    def remove_task(self, task):
        self.lst_of_tasks.remove(task)

    def remove_by_id(self, id):
        index = 0
        for task in self.lst_of_tasks:
            if task.id == id:
                self.lst_of_tasks.pop(index)
                break
            index += 1

    def update(self, id, info):
        index = 0
        for task in self.lst_of_tasks:
            if task.id == id:
                self.lst_of_tasks[index].description = str(info)
                break
            index += 1

def read_from_file(filename):
    f = open(filename, "r")
    contents = f.read()
    tasks_object = jsp.decode(contents)
    f.close()
    return tasks_object

# class Task_type(Enum):
#     MEETING = "Meeting"
#     CALL = "Call"
#     OTHER = "Other"
#
#
# class Status(Enum):
#     DONE = "Done"
#     NOT_DONE = "Not Done"
#     POSTPONED = "Postponed"

client1 = Client("Marko NotPolo", 232)
client2 = Client("NotMarko NotPolo", 233)
seller1 = Seller("Marko", "Polo", 236)
task1 = Task("Call", "Done", client1, seller1, "16.04.2019", "", "")
print(seller1)
print(client1)
print(Status.DONE)
