from ex11 import Database, User

from tkinter import Tk, Entry, END

class Table:
    
    def __init__(self,root, users):
        
        # create header
        if len(users) > 0:
            i = 0
            k = 0
            for key,value in users[i].items():
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                # start row at 0
                self.e.grid(row=i, column=k)
                self.e.insert(END, key)
                k = k+1

        # create body
        for i in range(len(users)):
            k = 0
            for _,value in users[i].items():
                
                self.e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                # start row at 1
                self.e.grid(row=i+1, column=k)
                self.e.insert(END, value)
                k = k+1

if __name__ == '__main__':

    # take the data
    db = Database()
    user = User(db)
    users = user.get_users()
    
    # create root window
    root = Tk()
    t = Table(root, users)
    root.mainloop()