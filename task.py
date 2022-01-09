#!/usr/bin/python3

 
import sys
import argparse
import os

complete_file_path = f"{os.getcwd()}/to/plans/completed.txt"
tasks_file_path = f"{os.getcwd()}/to/plans/task.txt"



class Report:

    def help(self):
        return """
Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics
        """
    
    def __sortFunction__(self,task):
        return int(task[1])

    def __init__(self):
        self.pendingTasks = []
        self.completedTasks = []
        if not os.path.exists(f"{os.getcwd()}/to/plans/"):
            os.makedirs(f"{os.getcwd()}/to/plans/")
        try:
            with open(tasks_file_path, "r") as reader:
                for line in reader.readlines():
                    taskLine = line.split()
                    if taskLine != []:
                        self.pendingTasks.append((taskLine[0], " ".join(taskLine[1:])))
        except FileNotFoundError:
            task_file = open(tasks_file_path, "x")
            task_file.close()
        try:
            with open(complete_file_path, "r") as reader:
                for line in reader.readlines():
                    self.completedTasks.append(line[0:len(line)-1])
        except FileNotFoundError:
            complete_file = open(complete_file_path, "x")
            complete_file.close()

    
    def printReport(self):
        return (len(self.completedTasks), len(self.pendingTasks))
    
    def addTask(self,task):
        #task[0] = priority
        #task[1] = title
        self.pendingTasks.append((task[0], task[1]))
        print(f"Added task: \"{task[1]}\" with priority {task[0]}")
        self.pendingTasks.sort(key= lambda task: task[0])
        with open(tasks_file_path, "w") as f:
            for task in self.pendingTasks:
                f.write(f"{task[0]} {task[1]}\n")
    
    def done(self,index):
        if (index - 1 >= 0 and index - 1 < len(self.pendingTasks)):
            completedTask = self.pendingTasks[index-1]
            self.completedTasks.append(completedTask)
            print(len(completedTask[1]))
            print(len(completedTask[1].lstrip()))
            with open(complete_file_path, "a") as f:
                lastTask  = self.completedTasks[-1]
                f.write(f"{lastTask[1]}\n")
            print("Marked item as done.")
            self.deleteTask(index,isDone=True)
        else:
            print(f"Error: no incomplete item with index #{index} exists.")

    def deleteTask(self,index,isDone = False):
        if (index - 1 >= 0 and index - 1 < len(self.pendingTasks)):
            deletedTask = self.pendingTasks.pop(index-1)
            with open(tasks_file_path, "r") as fp:
                lines = fp.readlines()
            with open(tasks_file_path, "w") as fp:
                for line in lines:
                    if line.strip("\n") != f"{deletedTask[0]} {deletedTask[1 ]}":
                        fp.write(line)
            if isDone == False:
                print(f"Deleted task #{index}")
        else:
            print(f"Error: task with index #{index} does not exist. Nothing deleted.")
            

    def listAllTasks(self):
        return self.pendingTasks
    
    def listAllCompletedTasks(self):
        return self.completedTasks

    def exit(self):
        with open(tasks_file_path, "r+") as task_file:
            task_file.truncate(0)
        with open(complete_file_path, "r+") as complete_file:
            complete_file.truncate(0)

    

report = Report() 

def checkAction(argsList):
    if argsList == []:
        print(report.help())
    elif args.action[0] == 'add':
        # args.action[2] = priority
        # args.action[3] = title
        if len(argsList) > 1:
            report.addTask((argsList[1], argsList[2]))
        else:
            print("Error: Missing tasks string. Nothing added!")
    elif args.action[0] == 'ls':
        allTasks = report.listAllTasks()
        if allTasks == []:
            print("There are no pending tasks!")
        for i in range(len(allTasks)):
            print(f"{i+1}. {allTasks[i][1]} [{allTasks[i][0]}]")

    elif args.action[0] == 'del':
        if len(argsList) == 2:
            report.deleteTask(int(argsList[1]))
        else:
            print("Error: Missing NUMBER for deleting tasks.")
    elif args.action[0] == 'done':
        if len(argsList) == 2:
            report.done(index=int(argsList[1]))
        else:
            print("Error: Missing NUMBER for marking tasks as done.")
    elif args.action[0] == 'report':

        pending_tasks = report.printReport()[1]
        completed_tasks = report.printReport()[0]
        
        print(f"Pending : {pending_tasks}")
        for i in range(pending_tasks): 
            print(f"{i+1}. {report.listAllTasks()[i][1]} [{report.listAllTasks()[i][0]}]")
        print("")
        print(f"Completed : {completed_tasks}")
        for i in range(completed_tasks): 
            print(f"{i+1}. {report.listAllCompletedTasks()[i]}")

    elif args.action[0] == 'help':
        print(report.help())
    elif args.action[0] == 'exit':
        report.exit()
    else:
        print(report.help())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', nargs="*")
    args = parser.parse_args()
    checkAction(args.action)



