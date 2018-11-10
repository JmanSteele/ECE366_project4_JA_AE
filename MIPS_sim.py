print("ECE 366 Project 4 MIPS simulator")
#file_reader reads each line of a file in an array as elements
#input: file -- read MIPS instruction
#outputs: filing
def file_reader(file):
    return_array = []
    #read in each line into array elements and ignore newlines
    for line in file:
        line = line.partition('#')[0]
        line=line.rstrip()
        if line[0:2] == "0x":
            return_array.append(line)

    return return_array

if op[2:8]=="000000":
    #add instruction
    rs=int(op[8:14], 2)
    rt=int(op[14:20], 2)
    rd=int(rs) +int(rt)
