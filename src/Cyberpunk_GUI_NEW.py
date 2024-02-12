from tkinter import *
import tkinter.scrolledtext as st
import tkinter.filedialog as fd
import time

root = Tk()
root.title = "TEST"
root['bg'] = "#0e110d"

box_container = Frame(root)
box_container.grid(row=1,column=0)
box_container['bg'] = "#0e110d"
#buffer_size
#matrix_width matrix_height
#matrix
#number_of_sequences
#sequence_1
#sequence_1_reward
#sequence_2
#sequence_2_reward
#...
#sequence_n
#sequence_n_reward

##SETUP
matrix = []
box_matrix = []
colsize = 0 #X
rowsize = 0 #Y
seqsize = 0 #reward size
sequence = []
bsize = 0
runtime = 0

boxcol = 0
boxrow = 0

def set_bsize(size):
    global bsize
    bsize = size
    pass

def set_msize(width,height):
    global matrix
    global box_matrix
    global colsize
    global rowsize
    if len(matrix) == 0:
        matrix = [["" for j in range(height)] for i in range(width)]
        box_matrix = [[0 for j in range(height)] for i in range(width)]
    else:
        for i in range(width):
            if i < len(matrix):
                for j in range(len(rowsize,height,1)):
                    matrix[i].append("")
                    box_matrix[i].append(0)
            else:
                matrix.append(["" for j in range(height)])
                box_matrix.append([0 for j in range(height)])
    colsize = width
    rowsize = height
    pass

def set_seqsize(count):
    global sequence
    global seqsize
    for i in range(len(sequence),count,1):
        sequence.append([0,[]])
    seqsize = count

##PROCESS

def check_in_list(source: list[str], find: list[str]) -> bool:
    for i in range(len(source)-len(find)+1):
        j = 0
        while (j < len(find)):
            if (source[j+i] == find[j]):
                j += 1
            else:
                break
            if (j == len(find)):
                return True
    return False

def convert_to_key(move_history: list[tuple[int,int]]) -> list[str]:
    global matrix
    global bsize
    key = [matrix[move_history[i][0]][move_history[i][1]] for i in range(bsize)]
    return key
    
def check_reward(key: list[str]) -> int:
    reward = 0
    #print("=============")
    #print("REWARD CHECK!")
    #dislay_path(key)
    #print(" ",end="")
    key = convert_to_key(key)
    #print(key)
    for i in range(seqsize):
        #print("CHECK ",end="")
        #print(seq[i])
        if check_in_list(key,sequence[i][0]):
            reward = reward + sequence[i][1]
    #print(reward)
    return reward
            

result_list = []

def insert_result(move: list[tuple[int,int]], point: int):
    global result_list
    if (len(result_list) == 0):
        result_list.append([point,move])
    else:
        i = 0
        while (result_list[i][0] > point and i < len(result_list)):
            #print("i",i)
            i += 1
            if i == len(result_list):
                break
        if not ([point,move] in result_list):
            result_list.insert(i,[point,move])

def dislay_path(move_history: list[tuple[int,int]]):
    global matrix
    for i in range(len(move_history)):
        x = move_history[i][0]
        y = move_history[i][1]
        print(matrix[x][y],end="")
        if (i < len(move_history)):
            print(" ",end="")
        else:
            print("")

def bruteforce(pos: tuple[int,int], depth: int, horizontal: bool, move_history: list[tuple[int,int]] = []):
    global bsize
    if (depth == bsize-1):
        move_history += [pos]
        reward = check_reward(move_history)
        if (reward > 0):
        #    dislay_path(move_history)
        #    print("PATH GET!",reward)
            insert_result(move_history,reward)
    else:
        if (horizontal):
            for i in range(rowsize):
                if (not [i,pos[1]] in move_history and [i,pos[1]] != pos):
                    bruteforce([i,pos[1]],depth+1,False,move_history + [pos])
        else:
            for i in range(colsize):
                if (not ([pos[0],i] in move_history) and ([pos[0],i] != pos)):
                    bruteforce([pos[0],i],depth+1,True,move_history + [pos])



def start_bruteforce():
    global runtime
    global colsize
    global result_list
    start = time.time()
    for i in range(colsize):
        bruteforce([i,0],0,False,[])
    for result in result_list:
        debug_print(result_to_str(result))
    end = time.time()
    runtime = end - start
    print(runtime)
        

##GUI
stcontainer = Frame(root)
stcontainer.grid(row=0,column=1)
stcontainer.grid_rowconfigure(0,weight=1)
stcontainer.grid_columnconfigure(0,weight=1)

debug_output = st.ScrolledText(stcontainer,width=50)
debug_output.grid(row=0,column=0,sticky=E)
def debug_print(text:str):
    debug_output.insert(INSERT,(text+"\n"))
    
def result_to_str(result: tuple[int,tuple[int,int]]) -> str:
    key = convert_to_key(result[1])
    text = "%d POINTS -" % result[0]
    for thing in key:
        text = text + " " + thing
    return text

    
def populate_box(col: int, row: int):
    global row_offset
    global box_matrix
    global boxcol
    global boxrow
    global matrix
    clear_effects()
    if (col > boxcol or row > boxrow):
        for i in range(row):
            for j in range(col):
                print(j,i)
                if (j < boxcol and i < boxrow):
                    continue
                elif (box_matrix[j][i]==0):
                    box_matrix[j][i] = Label(box_container, bg='black', fg='#90ff6b', width= 4)
                    box_matrix[j][i].configure(text=matrix[j][i])
                box_matrix[j][i].grid(row=i, column=j, pady=10, padx=10)
    elif (col < boxcol or row < boxrow): #ngecilin
        for i in range(row):
            for j in range(col):
                if (j < boxcol and i < boxrow):
                    continue
                box_matrix[j][i].grid_remove()
    boxcol = col
    boxrow = row
    root.update()
    return True

def open_file(filename = ""):
    global rowsize
    global colsize
    global matrix
    global seqsize
    global sequence
    
    if filename == "":
        target = fd.askopenfilename(filetypes=[("Text file","*.txt")])
    else:
        target = filename
    with open(target) as file:
        set_bsize(int(file.readline().strip()))
        msize = file.readline().strip().split(" ")
        set_msize(int(msize[0]),int(msize[1]))

        for i in range(rowsize):
            row = file.readline().strip().split(" ")
            for j in range(colsize):
                matrix[j][i] = row[j]
                
        set_seqsize(int(file.readline().strip()))
        for i in range(seqsize):
            sequence[i][0] = file.readline().strip().split(" ")
            sequence[i][1] = int(file.readline().strip())
        file.close()
        
    populate_box(colsize,rowsize)



def highlight(label : Label, type : str = "none"):
    if label == 0:
        return False
    if type == "none":
        back = 'black'
        front = '#90ff6b'
        pass
    elif type == "glow":
        front = 'black'
        back = '#90ff6b'
        pass
    label.configure(fg=front,bg=back)
    return True

def showbest():
    global result_list
    global box_matrix
    print(result_list[0])
    for path in result_list[0][1]:
        highlight(box_matrix[int(path[0])][int(path[1])],"glow")
    
def clear_effects():
    global box_matrix
    for rows in box_matrix:
        for cols in rows:
            highlight(cols)

buttoncontainer = Frame(root)
buttoncontainer.grid(row=0,column=0)
load = Button(buttoncontainer,text="Upload .txt file",command=open_file)
load.grid(row=0,column=0)
brute = Button(buttoncontainer,text="BRUTEFORCE",command=start_bruteforce)
brute.grid(row=0,column=1)
show = Button(buttoncontainer,text="SHOW",command=showbest)
show.grid(row=0,column=2)

root.mainloop()