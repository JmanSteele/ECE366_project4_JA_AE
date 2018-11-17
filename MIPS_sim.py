#Justino Almazan
#Alberto Espinoza
print("ECE 366 Project 4 MIPS simulator")
#file_reader reads each line of a file in an array as elements
#input: file -- read MIPS instruction
#outputs: filing
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
        print("RS register: $", rs, int(reg_arr[rs]))
        rt=int(op[11:16], 2)
        print("RT register: $", rt, int(reg_arr[rt])) 
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
    elif op[0:16]=="0001000000000000":   #for ending the program beq $0, $0, whatever
        x+=10000
        cycle[0]+=1    #single cycle
        cycle[1]+=3    #multi cycle
        cycle[2]+=1    #pipeline
        cycle[3]+=1    #3 step
    elif op[0:6]=="001000":
        #addi instruction
        print("ADDI")
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        imm = int(op[16:32], 2)
        if( imm & 0x8000) !=0:  #checks if last bit is 1
            imm = imm - 0x10000 #if so, converts to negative int
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
        print("RS: ", rs)
        rt=int(op[11:16], 2)
        print("RT: ", rt)
        rd=int(op[16:21], 2)
        print("RD: ", rd)
        reg_arr[rd]=int(reg_arr[rs]) - int(reg_arr[rt])
        print("Result: ", reg_arr[rd])
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
        print("RS: ", rs, reg_arr[rs], bin(reg_arr[rs]))
        rt=int(op[11:16], 2)
        print("RT: ", rt, reg_arr[rt], bin(reg_arr[rt]))
        rd=int(op[16:21], 2)
        print("RD: ", rd)
        reg_arr[rd]=int(reg_arr[rs]) ^ int(reg_arr[rt])
        print("Result: ", reg_arr[rd], bin(reg_arr[rd]))
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
        print("RS: ", rs)
        rt=int(op[11:16], 2)
        print("RT: ", rt)
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
            pc+=4
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
        if op[16]=="1":
            offset = -(65535 -int(op[16:32],2)+1)
            print("offset when MSB is 1: ", offset)
        else:
            offset=int(op[16:32], 2)
        if reg_arr[rs]!=reg_arr[rt]:
            pc+=4
            pc=pc+(int(offset)*4)
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
        cycle[2]+=2    #pipeline
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
        print("offset", offset)
        kk=reg_arr[rs]+offset-8192 #you put -8912, but should be -8192 lol
        print("memory: ", memREE[kk])
        print("Register and its value: register", rs, reg_arr[rs]) #A.E instead of rt, should be rs
        reg_arr[rt]=memREE[kk]    
        cycle[0]+=1
        cycle[1]+=5
        cycle[2]+=2
        cycle[5]+=1
        x+=1
        pc+=4
    elif op[0:6]=="101011":
        print("SW")
        #store word
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        print("Register and its value: register", rt, reg_arr[rt])
        offset=int(op[16:32], 2)
        print("Offset: ", offset)
        kk=offset+reg_arr[rs]-8192
        print("memory location: ", kk)
        memREE[offset+reg_arr[rs]-8192]=reg_arr[rt]
        print("What got stored in memory?", memREE[kk])
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
    #memREE[0] = 0 # A.E Starts with memory at location 0, be set at 0. 
                  #When we do our first LOAD instrc. it wants to load from memory 
                   # location 0, but theres a string "none" where it should be an int type
    while x < len(instr_mem):
        op = instr_mem[x]
        print("PC: ", pc, hex(pc))
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
    print("Memory: ...")
    i=0
    for i in range(0, 2000, 4):
        if int(memREE[i]) != 0:
            print("Memory ",i,":" ,memREE[i], hex(memREE[i]))
    #A.E Im comparing the results from MIPS executing final memory contants
    #I'll work on this later so you wont have alot of work on your hands


    #############################################3
    # Alberto,
    # sample A works correctly now,
    # if you notice I switched your memory locations
    # instead of incremementing by 1, I had them incremement
    # by 4, I think it works because remember in MIPS
    # we save words which take up 4 spaces and not 1.
    # Also can you add conditional hazard counter for when we
    # compute $rd prior to instructions beq or bne?
    # for example:
    # add $4, $3, $2    <---delay right here because of $rd (needs to be fixed)
    # beq $4, $0, somewhere    <---delay here if we DO branch (already taken care of)
    # apparently there is a hazard directly after that add instruction
    # when you compute the same $rd for beq
    # notice how they both have $4 as their $rd
    # this will happen to all computations of $rd prior to checking branch
    # let's start checking sample's b c and d
    # also i'm not sure if you want to add extra
    # counters cause in Rao's project description
    # it looks like she wants counters that'll produce percentages
    # of the instructions that are based on ALU, jump, branch, memory, other
    # my guess is our jumps will be zero because she did not have a j type
    # instruction be mandatory for this project, not sure what "other" means,
    # ALU is our add, addi, sub, xor, slt
    # branch will just be beq, bne, and that one instruction i left that'll
    # kill the program, also I believe the total will be our D.I.C.
    # so for each of these counters divide them by the total.  Display the percentage.
    # Lastly just compare our results from here with the results in MIPS
    # when you test samples b c and d.  After that we'll be done for the first week
    ###############################################

memREE = [0]*4096 #initialize to list of 4096 none's
#sim("i_mem.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_a.txt")
#print("\n\n\n\n\n\n\n\n")
sim("sample_b.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_c.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_d.txt")
