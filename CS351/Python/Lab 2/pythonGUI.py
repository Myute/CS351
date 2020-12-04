#Gui example
#https://pythonspot.com/tag/tkinter/
#https://www.pythoncentral.io/introduction-to-pythons-tkinter/
#https://www.python-course.eu/python_tkinter.php
#https://wiki.python.org/moin/Intro%20to%20programming%20with%20Python%20and%20Tkinter
#oop in python:
#https://python-textbok.readthedocs.io/en/1.0/Introduction_to_GUI_Programming.html


from tkinter import *

class MyFirstGUI:

    def __init__(self, master):
        self.numOutputs = 1
        self.database = []
        self.outString = ""
        self.master = master
        self.master.bind("<Return>", self.submitname)
        master.title("My Cat Registration System")

        self.label = Label(master, text="Cat Name: ").grid(row=0,column=0,sticky=E)
        self.identrylabel = Label(master, text = "Cat ID: ").grid(row=0,column=2,sticky=E)
        self.outnamelabel = Label(master, text = "Registered Name: ").grid(row = 1, column = 0, sticky = E)
        self.outIDlabel = Label(master, text="Registered ID: ").grid(row =1, column = 2, sticky = E)

        self.catnameentry = Entry(master)
        self.catnameentry.grid(row=0, column=1, sticky =E) # this call returns NULL when it is done

        self.catidentry = Entry(master)
        self.catidentry.grid(row=0,column=3, sticky = E)

        self.submitbutton = Button (master, text="Submit Cat", command=self.submitname).grid(row=0,column=4, sticky=E)
        self.printbutton = Button (master, text = "Print Database", command = self.printdatabase).grid(row=1,column=4,sticky=E)

    def submitname (self, Event = None):
        if self.catidentry.get() == "" or self.catnameentry.get() == "":
            print("Error: Either \"Cat Name\" or \"Cat ID\" field is empty")
            return

        print ("a cat name submitted: " + self.catnameentry.get())
        self.database.append((self.catnameentry.get(),self.catidentry.get()))

        self.registeredName = Label(self.master, text = self.catnameentry.get()).grid(row=self.numOutputs,column=1,sticky=E)        
        self.registeredid = Label(self.master, text = self.catidentry.get()).grid(row=self.numOutputs,column=3,sticky=E)   
        self.numOutputs += 1
        
        self.catnameentry.delete(0,END)
        self.catidentry.delete(0,END)
        
        return
    
    def printdatabase(self):
        print("**********************\nMy Cat Registration System\n**********************" 
                + "\nCat Name, Cat ID")
        for x in self.database:
            print(x[0] + ", " + x[1])
        return


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()

