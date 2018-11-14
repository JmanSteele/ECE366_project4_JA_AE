#Justino Almazan
#Alberto Espinoza
print("ECE 366 Project 4 MIPS simulator")
#file_reader reads each line of a file in an array as elements
#input: file -- read MIPS instruction
#outputs: filing
import time
import math
def file_to_array(file):
    return_array = []
    #read in each line into array elements and ignore newlines
    for line in file:
        if line =="\n" or line[0]=='#':
            continue
        line=line.partition('#')[0]
        line=line.rstrip()
        line=line.replace('0x', '')
        line=format(int(line,16),"032b")
        return_array.append(line)

    return return_array
def execute_operation(op, reg_arr, pc, cycle, x):
    if op[0:6]=="000000" and op[26:32]=="100000":
        #add instruction
        print("ADD")
        rs=int(op[6:11], 2)
        print("RS register: $", rs)
        rt=int(op[11:16], 2)
        print("RT register: $", rt) 
        rd=int(op[16:21], 2)
        print("RD register: $", rd)
        reg_arr[rd]=int(reg_arr[rs]) + int(reg_arr[rt])
        print("The result stored in Register RD is: ", reg_arr[rd])
        pc+=4
        cycle[0]+=1    #single cycle
        cycle[1]+=4    #multi cycle
        cycle[2]+=1    #pipeline
        cycle[4]+=1    #4 steps
        x+=1
        print("X:", x)
    elif op[0:32]=="00010000000000001111111111111111":
        x+=10000
        cycle[0]+=1    #single cycle
        cycle[1]+=3    #multi cycle
        cycle[2]+=2    #pipeline
        cycle[3]+=1    #3 step
    elif op[0:6]=="001000":
        #addi instruction
        print("ADDI")
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        imm = int(op[16:32], 2)
        print("RS: $", rs)
        print("RT: $", rt)
        print("imm: ", imm)
        reg_arr[rt]=int(reg_arr[rs]) + imm
        print("Result stored in RT is :", reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        x+=1
        print("X: ", x)
    elif op[0:6]=="000000" and op[26:32]=="100010":
        print("SUB")
        #sub instruction
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        rd=int(op[16:21], 2)
        reg_arr[rd]=int(reg_arr[rs]) - int(reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        x+=1
    elif op[0:6]=="000000" and op[26:32]=="100110":
        print("XOR")
        #xor instruction
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        rd=int(op[16:21], 2)
        reg_arr[rd]=int(reg_arr[rs]) ^ int(reg_arr[rt])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        x+=1
    elif op[0:6]=="000100":
        print("BEQ")
        #Branch instruction
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        cycle[0]+=1   #single cycle
        cycle[1]+=3   #multi cycle
        cycle[3]+=1   #3 steps
        if op[16]=="1":
            offset = -(65535 -int(op[16:32],2)+1)
            print("offset when MSB is 1: ", offset)
        else:
            offset=int(op[16:32], 2)
        print("OFFset: ", int(offset))
        if reg_arr[rs]==reg_arr[rt]:
            pc=pc+(int(offset)*4)
            cycle[2]+=2   #stall for branch so pipeline increases by 2
            x+=1
            x+=int(offset)
        else:
            pc+=4
            cycle[2]+=1
            x+=1
    elif op[0:6]=="000101":
        print("BNE")
        #branch if not equal to instruction
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        offset=int(op[16:32], 2)
        cycle[0]+=1
        cycle[1]+=3
        cycle[3]+=1
        if reg_arr[rs]!=reg_arr[rt]:
            pc+=offset*4
            cycle[2]+=2
            x=x+1+offset
        else:
            pc+=4
            cycle[2]+=1
            x+=1
    elif op[0:6]=="000000" and op[26:32]=="101010":
        print("SLT")
        #set less than
        rs=int(op[6:11], 2)
        print("RS: $", rs)
        rt=int(op[11:16], 2)
        print("RT: $", rt)
        rd=int(op[16:21], 2)
        print("RD: $", rd)
        cycle[0]+=1    #single cycle
        cycle[1]+=4    #multi cycle
        cycle[2]+=1    #pipeline
        cycle[4]+=1    #step 4
        pc+=4
        x+=1
        if reg_arr[rs]<reg_arr[rt]:
            reg_arr[rd]=1
            print("No Branch necessary")
        else:
            reg_arr[rd]=0
            print("Branch in progress...")
        print("RD: ", reg_arr[rd])
    elif op[0:6]=="100011":
        print("LW")
        #load word
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        offset=int(op[16:32], 2)
        reg_arr[rs]+=offset    #move register across memory by offset to access value
        reg_arr[rt]=reg_arr[rs]#set register rt equal to whatever value rs obtains from memorys
        pc+=4
        cycle[0]+=1
        cycle[1]+=5
        cycle[2]+=2
        cycle[5]+=1
        x+=1
    elif op[0:6]=="101011":
        print("SW")
        #store word
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        offset=int(op[16:32], 2)
        reg_arr[rs]+=offset
        reg_arr[rs]=reg_arr[rt]
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        x+=1
    return [op, reg_arr, pc, cycle, x]
#sim: simulates the MIPS hex code
#inputs: file name of txt that carries the instructions
def sim(MIPS_HEX):
    #initialize pc and register array
    x=0   #this is to configure pc back to 1 increments instead of 4 so I can make it easier to read my input files
    pc = 0
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0] #registers [$0, $1, $2, $3, $4, $5, $6, $7]
    cycle=[0, 0, 0, 0, 0, 0] #this array will work like so [single cycle, multi cycle, pipeline, 3cycle, 4cycle, 5cycle]
    #create file variables from file name strings
    instr_mem_input = open(MIPS_HEX, "r")#read file for programming instructions
    instr_mem = file_to_array(instr_mem_input)
    dic=0   #dynamic instruction will be counted
    while x < len(instr_mem):
        op = instr_mem[x]
        print("PC: ", pc)
        data_set = execute_operation(op, reg_arr, pc, cycle, x)
        reg_arr = data_set[1]
        pc=data_set[2]
        cycle=data_set[3]
        x=data_set[4]
        print("OP: ", op)
        print("Register Array:", reg_arr)#prints for each instruction so we can see what is being stored in each register
        print("Cycle:", cycle)
        dic+=1 #increment DIC by 1 everytime we perform an instruction
        print("DIC: ", dic)
        print("\n")
        if x>1000:
            break

    print("Dynmic Instruction Count: ", dic)
    print("Single Cycle Count:       ", cycle[0])
    print("Multi Cycle Count:        ", cycle[1])
    print("Count 3 Step Cycles:      ", cycle[3])
    print("Count 4 Step Cycles:      ", cycle[4])
    print("Count 5 Step Cycles:      ", cycle[5])
    cycle[2]+=4
    print("Pipeline Cycle count:     ", cycle[2])
    print("Below is a listing of the final values for each register: \n")
    print("$1 = ", reg_arr[1])
    print("$2 = ", reg_arr[2])
    print("$3 = ", reg_arr[3])
    print("$4 = ", reg_arr[4])
    print("$5 = ", reg_arr[5])
    print("$6 = ", reg_arr[6])
    print("$7 = ", reg_arr[7])


sim("i_mem.txt")
