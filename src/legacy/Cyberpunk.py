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
import time
sequence = []

def process_file():
    global sequence
    global seqsize
    global bsize
    global colsize
    global rowsize
    global matrix
    with open("input.txt") as f:
        #buffer size
        bsize = int(f.readline().strip())
        m_size = f.readline().strip().split(" ")
        #matrix size
        colsize = int(m_size[0])
        rowsize = int(m_size[1])
        #matrix
        matrix = [["" for j in range(rowsize)] for i in range(colsize)]
        for i in range(rowsize):
            row = f.readline().strip().split(" ")
            for j in range(colsize):
                matrix[j][i] = row[j]
        #no_of_sequences
        seqsize = int(f.readline().strip())
        #sequences
        if (seqsize > 0):
            for i in range(seqsize):
                seq = f.readline().strip().split(" ")
                seq_reward = int(f.readline().strip())
                sequence.append([seq,seq_reward])

        f.close()

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
            insert_result(convert_to_key(move_history),reward)
    else:
        #print(depth,bsize )
        if (depth < 3):
            print(move_history)
            #sleep(0.1)
        if (horizontal):
            for i in range(rowsize):
                if (not [i,pos[1]] in move_history and [i,pos[1]] != pos):
                    bruteforce([i,pos[1]],depth+1,False,move_history + [pos])
        else:
            for i in range(colsize):
                if (not ([pos[0],i] in move_history) and ([pos[0],i] != pos)):
                    bruteforce([pos[0],i],depth+1,True,move_history + [pos])
                
def result_ranking(result_list: list[tuple[int,tuple[int,int]]]):
    for result in result_list:
        print(result[0],end=" ")
        for node in result[1]:
            print(node,end=" ")
        print()

def start():
    global matrix
    process_file()
    start_bruteforce()
    result_ranking(result_list)
    
def start_bruteforce():
    global colsize
    for i in range():
        bruteforce([i,0],0,False,[])

def start_bruteforce():
    global colsize
    for i in range():
        bruteforce([i,0],0,False,[])
        