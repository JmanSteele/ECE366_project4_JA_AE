#Justino Almazan
#Alberto Espinoza
print("ECE 366 Project 4 MIPS simulator")
#file_reader reads each line of a file in an array as elements
#input: file -- read MIPS instruction
#outputs: filing
def file_to_array(file):
    return_array = []
    #read in each line into array elements and ignore newlines
    for line in file:
        line=line.partition('#')[0]
        line=line.rstrip()
        if line[0:2] == "0x":
            return_array.append(line)

    return return_array
def execute_operation(op, reg_arr, pc, branch):
    if op[2:8]=="000000" and op[29:34]=="100000":
        #add instruction
        print("ADD")
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        reg_arr[rd]=int(reg_arr[rs]) + int(reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
    elif op[2:8]=="001000":
        #addi instruction
        print("ADDI")
        rs=int(op[8:14], 2)
        imm = int(op[20:34], 2)
        reg_arr[rt]=int(reg_arr[rs]) + imm
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
    elif op[2:8]=="000000":
        print("SUB")
        #sub instruction
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        reg_arr[rd]=int(reg_arr[rs]) - int(reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
    elif op[2:8]=="000000" and op[29:34]=="100110":
        print("XOR")
        #xor instruction
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        rd=int(op[20:24], 2)
        reg_arr[rd]=int(reg_arr[rs]) ^ int(reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
    elif op[2:8]=="000100":
        print("BEQ")
        #Branch instruction
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        offset=(op[20:34], 2)
        cycle[0]+=1
        cycle[1]+=3
        cycle[3]+=1
        if reg_arr[rs]==reg_arr[rt]:
            pc+=offset*4
            cycle[2]+=2
        else:
            pc+=4
            cycle[2]+=1
    elif op[2:8]=="000101":
        print("BNE")
        #branch if not equal to instruction
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        cycle[0]+=1
        cycle[1]+=3
        cycle[3]+=1
        if reg_arr[rs]!=reg_arr[rt]:
            pc+=offset*4
            cycle[2]+=2
        else:
            pc+=4
            cycle[2]+=1
    elif op[2:8]=="000000" and op[20:34]=="101010":
        print("SLT")
        #set less than
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        rd=int(op[20:24], 2)
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        if reg_arr[rs]<reg_arr[rt]:
            reg_arr[rd]=1
        else:
            reg_arr[rd]=0
            pc+=4
    elif op[2:8]=="100011":
        print("LW")
        #load word
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        offset=int(op[20:34], 2)
        reg_arr[rs]+=offset    #move register across memory by offset to access value
        reg_arr[rt]=reg_arr[rs]#set register rt equal to whatever value rs obtains from memorys
        pc+=4
        cycle[0]+=1
        cycle[1]+=5
        cycle[2]+=2
        cycle[5]+=1
    elif op[2:8]=="101011":
        print("SW")
        #store word
        rs=int(op[8:14], 2)
        rt=int(op[14:20], 2)
        offset=int(op[20:34], 2)
        reg_arr[rs]+=offset
        reg_arr[rs]=reg_arr[rt]
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
#sim: simulates the MIPS hex code
#inputs: file name of txt that carries the instructions
def sim (MIPS_HEX):
    #initialize pc and register array
    pc = 0
    branch = 0
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0] #registers [$0, $1, $2, $3, $4, $5, $6, $7]
    cycle=[0, 0, 0, 0, 0, 0] #this array will work like so [single cycle, multi cycle, pipeline, 3cycle, 4cycle, 5cycle]
    #create file variables from file name strings
    instr_mem_input = open(MIPS_HEX, "r")#read file for programming instructions
    instr_mem = file_to_array(instr_mem_input)
    dic=0   #dynamic instruction will be counted
    while pc < len(instr_mem):
        op = instr_mem[pc]
        print("PC: ", pc)
        data_set = execute_operation(op, reg_arr, pc, branch, cycle)
        reg_arr = data_set[0]
        pc=data_set[1]
        branch=data_set[2]
        cycle=data_set[3]
        print("register array:", reg_arr)#prints for each instruction so we can see what is being stored in each register
        dic+=1 #increment DIC by 1 everytime we perform an instruction

    print("Dynmic Instruction Count: ", dic)
    print("Single Cycle Count:       ", cycle[0])
    print("Multi Cycle Count:        ", cycle[1])
    print("Count 3 Step Cycles:      ", cycle[3])
    print("Count 4 Step Cycles:      ", cycle[4])
    print("Count 5 Step Cycles:      ", cycle[5])
    print("Pipeline Cycle count:     " cycle[2]+=4)
