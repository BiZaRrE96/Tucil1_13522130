from tkinter import *
import tkinter.scrolledtext as st

m_window = Tk()
m_window.title('BRUH')
m_window['bg'] = "#0e110d"

row_offset = 0
active_boxes = 0

input_container = Frame(m_window)
input_container['bg'] = "#0e110d"
input_container['highlightbackground'] = 'red'
input_container.configure(highlightthickness=1)
input_container.grid(row=2,column=0)

#scrolltext object for output
debug_output = st.ScrolledText(m_window)
debug_output.grid(row=10,column=0)
def debug_print(text:str):
    debug_output.insert(INSERT,(text+"\n"))

entry_matrix = [[0 for i in range(20)] for i in range(20)]

def focus_entry(row,col):
    global active_boxes
    if (row >= active_boxes or col >= active_boxes or row < 0 or col < 0):
        return False
    entry_matrix[row][col].focus()
    return True

def focus_next(row,col):
    global active_boxes
    print(row,(col+1)%active_boxes)
    if (row < active_boxes and col < active_boxes):
        return focus_entry(row+(col+1)//active_boxes,(col+1)%active_boxes)
    else:
        return True
    
def focus_prev(row,col):
    global active_boxes
    if (row >= 0 and col >= 0):
        return focus_entry(row+(col-1)//active_boxes,(col-1)%active_boxes)
    else:
        return True
    
#entry validation thingamajig
def process_entry(type,code,text,row=99999, col=99999):
    global active_boxes
    row = int(row)
    col = int(col)
    code = int(code)
    type = int(type)
    string = "%s %d %d (CODE %d)" %(text,row,col,code)
    debug_print(string)
    text = str(text).strip(" ")
    if str(text).isalnum() or text == "":
        if type == 0:
            return True
        elif code == 0 and len(text) == 1:
            pass
        elif code == 1 and len(text) == 1:
            focus_next(row,col)
        elif code == 0 and len(text) == 2:
            focus_next(row,col)
        elif code == 0 and len(text) > 1:
            print(3)
            entry_matrix[row][col].insert(0,text[:2])
            entry_matrix[row+(col+1)//active_boxes][(col+1)%active_boxes].insert(0,text[2:])
        elif code == 1 and len(text) > 1:
            print(4)
            entry_matrix[row][col].delete(0,END)
            entry_matrix[row][col].insert(0,text[:2])
            entry_matrix[row+(col+1)//active_boxes][(col+1)%active_boxes].insert(0,text[2:])
        return True
    else:
        return False

def backspace_test(event):
    global active_boxes
    global entry_matrix
    if (event.widget.get() == ""):
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']
        print(row,col)
        if (row > 0 and col > 0):
            entry_matrix[row+(col-1)//active_boxes][(col-1)%active_boxes].delete(1,END)
        focus_prev(row,col)

validator = m_window.register(process_entry)

def populate_box(size: int):
    global row_offset
    global active_boxes
    global entry_matrix
    print("A",size,active_boxes)
    if (size > active_boxes):
        for i in range(size):
            for j in range(size):
                if (i < active_boxes and j < active_boxes):
                    continue
                if (entry_matrix[i][j]==0):
                    entry_matrix[i][j] = Entry(input_container, bg='red', width= 4)
                    entry_matrix[i][j].config(validate="key",validatecommand=(validator,'%d','%i','%S',i,j))
                    entry_matrix[i][j].bind("<BackSpace>", backspace_test)
                entry_matrix[i][j].grid(row=i, column=j, pady=10, padx=10)
    elif (size < active_boxes): #ngecilin
        for i in range(active_boxes):
            for j in range(active_boxes):
                if (i<size and j<size):
                    continue
                print(i,j)
                entry_matrix[i][j].grid_remove()
    active_boxes = size
    m_window.update()
    return True

def increase_size():
    global active_boxes
    populate_box(active_boxes+1)


def decrease_size():
    global active_boxes
    populate_box(active_boxes-1)


def test():
    global debug_output
    entry_matrix[0][0].delete(0,END)
    debug_print("test")


button_container = Frame(m_window)
button_container['bg'] = 'green'
button_container.grid(row=0,column=0)
Button(button_container,text="<",command=decrease_size).grid(row=0,column=0)
Button(button_container,text=">",command=increase_size).grid(row=0,column=1)

Button(m_window,command=test,text="BALLS").grid(row=3,column=0)
increase_size()
#target['bg'] = 'red'

#SOLUTION CONTAINER
key_container = Frame(m_window)
key_container.configure(background='blue')
key_container.grid(row=3,column=1,rowspan=3)

active_keys = 0
key_list = [[0,0] for i in range(20)]

def populate_keys():
    global active_keys
    for i in range(active_keys+1):
        if key_list[i] == [0,0]:
            key_list[i][0] = 

def backspace_key(event):
    global active_keys
    global entry_matrix
    if (event.widget.get() == ""):
        row = event.widget.grid_info()['row']
        col = event.widget.grid_info()['column']
        print(row,col)
        if (row > 0 and col > 0):
            entry_matrix[row+(col-1)//active_boxes][(col-1)%active_boxes].delete(1,END)
        focus_prev(row,col)

m_window.mainloop()

