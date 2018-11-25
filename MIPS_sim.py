#Justino Almazan
#Alberto Espinoza
print("ECE 366 Project 4 MIPS simulator")
#file_reader reads each line of a file in an array as elements
#input: file -- read MIPS instruction
#outputs: filing
import numpy #originally I included numpy because I wanted to do 2d matrixes
             #for part d instead of using an array of 8 values
             #It didn't go as planned after debugging, but I kept numpy anyway to
             # so it would create 8 bit arrays for me
import math
def miss():
    print("MISS! Replacing cache...")
    return
def hit():
    print("HIT! Loaded from cache...")
    return
#this is where the cache function will be performed
def cacheMeOusside(Addr, cache, tags, tagsd, LRU):#pop culture reference
    #part 3 a
    #log(16) = 4 bits   <---I'm going by the example Rao gave us in class for DM
    #[b3 b2 b1 b0]  in word offset
    #block index log(2) = 1 bit
    #16 - 1 - 4 = 11
    #11 bit tag field...
    #Addr=bin(Addr)      #convert int of the lw offset back to binary
    print("Running DM cache of 2 blocks, 4 words")
    print("Offset for CACHE: ", Addr, tags)
    taga=int(Addr[0:11], 2)     #these values are for part a
    print("TAG :", taga)
    blocka=int(Addr[11], 2)
    print("Block: ", blocka)
    OFFSETa=int(Addr[12:16], 2)
    print("4 bit offset: ", OFFSETa)
    olda=cache[0]
    olda1=cache[1]
    if blocka == 0:    #untested from this point on in the cache function
        if taga != tags[0]:
            cache[0]+=1   #increasing miss counter when the tags don't match from
            tags[0] = taga  #replacing the tag for future reference
        elif taga == tags[0]:
            cache[1]+=1     #increase hit counter
            tags[0]=taga
    elif blocka == 1:   #this will check in second block (block 1)
        if taga != tags[1]:   #tags are not equal to eachother
            cache[0]+=1    #increase miss counter
            tags[1] = taga      #replace tag for block 1
        elif taga == tags[1]:   #part a has a hit for block 1
            cache[1]+=1          #hit counter increase
            tags[1]=taga         #In the time spent debugging, I thought
                                 #"What if I replace tag again anyway? That might work"
                                 #Surprisingly it did work, and I don't want to find
                                 #out why.
    if olda != cache[0]:
        miss()
    elif olda1 != cache[1]:
        hit()
    #part 3 b
    #log(8) = 3
    #[b2 b1 b0] in word offset
    #block index log(4)=2
    #16-3-2=11
    #11 bit tag field same as part a \...(0.o)..../
    print("Running DM cache of 4 blocks, 2 words")
    blockb=int(Addr[11:13], 2)   #should read 4 block range
    print("Block: ", blockb)
    OFFSETb=int(Addr[13:16], 2)  #I don't think the offset is important for this
    print("3 bit offset: ", OFFSETb) #but just for completion i'll do it anyway
    oldb=cache[2]
    oldb1=cache[3]
    if blockb==0:
        if taga != tags[2]: #I'm going to reuse variable 'taga' since the tag field
            cache[2]+=1     # is also 11 bit, the same as part a
            tags[2]=taga
        elif taga==tags[2]:
            cache[3]+=1
            tags[2]=taga
    elif blockb==1:
        if taga !=tags[3]:
            cache[2]+=1
            tags[3]=taga
        elif taga==tags[3]:
            cache[3]+=1
            tags[3]=taga
    elif blockb==2:
        if taga !=tags[4]:
            cache[2]+=1
            tags[4]=taga
        elif taga==tags[4]:
            cache[3]+=1
            tags[4]=taga
    elif blockb==3:
        if taga !=tags[5]:
            cache[2]+=1
            tags[5]=taga
        elif taga==tags[5]:
            cache[3]+=1
            tags[5]=taga
    if oldb != cache[2]:
        miss()
    elif oldb1 != cache[3]:
        hit()
    #part 3 d
    #block = 1 bit
    #set index = log(4) = 2 bit
    #tag index = 16 - 2 - 1 = 13
    print("Running 2-way set associative cache")
    tagd = int(Addr[0:13], 2)    #aquiring tag
    print("Tag: ", tagd)
    si=int(Addr[13:16], 2)       #aquiring set index
    print("Set Index: ", si)
    bo=int(Addr[15], 2)          #aquiring offset in block
    print("Offset in Block: ", bo)
    old=cache[6]
    old1=cache[7]
    if si ==0 or si ==4:
        if tagd != tagsd[0] and tagd != tagsd[1]:
            cache[6] += 1           #increasing miss counter
            if LRU[0] < LRU[1]: #we're checking now which block was least used
                tagsd[0] = tagd      #store the tag in cache if this was block was least used
                LRU[0] += 1          #incremement this block so we know it is used once more
            elif LRU[0] > LRU[1]:  #the same thing happens here except under opposite conditions
                tagsd[1] = tagd
                LRU[1] += 1
            else:
                tagsd[0] = tagd
                LRU[0] += 1      #this should be activated for the initial
                                  #cache access of this block
                                  #or for when both blocks are being used the same amount
        elif tagd == tagsd[0]:
            cache[7] += 1
            tagsd[0] = tagd
            LRU[0] += 1
        elif tagd == tagsd[1]:
            cache[7] += 1
            tagsd[1] = tagd
            LRU[1] += 1
    elif si == 1 or si == 5:
        if tagd != tagsd[2] and tagd != tagsd[3]:
            cache[6] += 1           #increasing miss counter
            if LRU[2] < LRU[3]: #we're checking now which block was least used
                tagsd[2] = tagd      #store the tag in cache if this was block was least used
                LRU[2] += 1          #incremement this block so we know it is used once more
            elif LRU[2] > LRU[3]:  #the same thing happens here except under opposite conditions
                tagsd[3] = tagd
                LRU[3] += 1
            else:
                tagsd[2] = tagd
                LRU[2] += 1      #this should be activated for the initial
                                  #cache access of this block
                                  #or for when both blocks are being used the same amount
        elif tagd == tagsd[2]:
            cache[7] += 1
            tagsd[2] = tagd
            LRU[2] += 1
        elif tagd == tagsd[3]:
            cache[7] += 1
            tagsd[3] = tagd
            LRU[3] += 1
    elif si == 2 or si == 6:
        if tagd != tagsd[4] and tagd != tagsd[5]:
            cache[6] += 1           #increasing miss counter
            if LRU[4] < LRU[5]: #we're checking now which block was least used
                tagsd[4] = tagd      #store the tag in cache if this was block was least used
                LRU[4] += 1          #incremement this block so we know it is used once more
            elif LRU[4] > LRU[5]:  #the same thing happens here except under opposite conditions
                tagsd[5] = tagd
                LRU[5] += 1
            else:
                tagsd[4] = tagd
                LRU[4] += 1      #this should be activated for the initial
                                  #cache access of this block
                                  #or for when both blocks are being used the same amount
        elif tagd == tagsd[4]:
            cache[7] += 1
            tagsd[4] = tagd
            LRU[4] += 1
        elif tagd == tagsd[5]:
            cache[7] += 1
            tagsd[5] = tagd
            LRU[5] += 1
    elif si == 3 or si ==7:
        if tagd != tagsd[6] and tagd != tagsd[7]:
            cache[6] += 1           #increasing miss counter
            if LRU[6] < LRU[7]: #we're checking now which block was least used
                tagsd[6] = tagd      #store the tag in cache if this was block was least used
                LRU[6] += 1          #incremement this block so we know it is used once more
            elif LRU[6] > LRU[7]:  #the same thing happens here except under opposite conditions
                tagsd[7] = tagd
                LRU[7] += 1
            else:
                tagsd[6] = tagd
                LRU[6] += 1      #this should be activated for the initial
                                  #cache access of this block
                                  #or for when both blocks are being used the same amount
        elif tagd == tagsd[6]:
            cache[7] += 1
            tagsd[6] = tagd
            LRU[6] += 1
        elif tagd == tagsd[7]:
            cache[7] += 1
            tagsd[7] = tagd
            LRU[7] += 1
    if old != cache[6]:
        miss()
    elif old1 !=cache[7]:
        hit()
    print("2 way set cache: \n", tagsd)
    print("LRU: \n", LRU)
    return [cache, tags, tagsd, LRU]        #return cache and tag values
    
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

def execute_operation(op, reg_arr, pc, cycle, x, percentage,hazard, dic, cache, tags, tagsd, LRU):
    if op[0:6]=="000000" and op[26:32]=="100000":
        print("ADD")
        rs=int(op[6:11], 2)
        print("RS register: $", rs, int(reg_arr[rs]))
        rt=int(op[11:16], 2)
        print("RT register: $", rt, int(reg_arr[rt])) 
        rd=int(op[16:21], 2)
        print("RD register: $", rd)
        hazard[0] = rd          #storing register value rd
        hazard[1] = dic         #storing dic value to compare to BEQ/BNE dic value
                                #must differ by 1 dic to signify hazard, immediate use
        reg_arr[rd]=int(reg_arr[rs]) + int(reg_arr[rt])
        print("The result stored in Register RD is: ", reg_arr[rd])
        pc+=4
        cycle[0]+=1             #single cycle
        cycle[1]+=4             #multi cycle
        cycle[2]+=1             #pipeline
        cycle[4]+=1             #4 steps
        percentage[0]+=1     #ALU based instruction
        x+=1
        print("X:", x)
        
    elif op[0:16]=="0001000000000000":   #for ending the program beq $0, $0, whatever
        x+=10000
        cycle[0]+=1    #single cycle
        cycle[1]+=3    #multi cycle
        cycle[2]+=1    #pipeline
        cycle[3]+=1    #3 step
        percentage[3]+=1
        
    elif op[0:6]=="001000":
        print("ADDI")
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        imm = int(op[16:32], 2)
        hazard[0] = rt          #storing register value rt
        hazard[1] = dic         #storing dic value   
        if( imm & 0x8000) !=0:  #checks if last bit is 1
            imm = imm - 0x10000 #if so, converts to negative int
        print("RS: $", rs)
        print("RT: $", rt)
        print("imm: ", imm)
        reg_arr[rt]=int(reg_arr[rs]) + imm
        print("Result stored in RT is :", reg_arr[rt])
        pc+=4
        percentage[0]+=1     #ALU based instruction 
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        x+=1
        print("X: ", x)
        
    elif op[0:6]=="000000" and op[26:32]=="100010":
        print("SUB")
        rs=int(op[6:11], 2)
        print("RS: ", rs)
        rt=int(op[11:16], 2)
        print("RT: ", rt)
        rd=int(op[16:21], 2)
        print("RD: ", rd)
        hazard[0] = rd          #storing register value rt
        hazard[1] = dic         #storing dic value
        reg_arr[rd]=int(reg_arr[rs]) - int(reg_arr[rt])
        print("Result: ", reg_arr[rd])
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        percentage[0]+=1     #ALU based instruction
        x+=1
        
    elif op[0:6]=="000000" and op[26:32]=="100110":
        print("XOR")
        rs=int(op[6:11], 2)
        print("RS: ", rs, reg_arr[rs], bin(reg_arr[rs]))
        rt=int(op[11:16], 2)
        print("RT: ", rt, reg_arr[rt], bin(reg_arr[rt]))
        rd=int(op[16:21], 2)
        print("RD: ", rd)
        hazard[0] = rd          #storing register value rt
        hazard[1] = dic         #storing dic value
        reg_arr[rd]=int(reg_arr[rs]) ^ int(reg_arr[rt])
        print("Result: ", reg_arr[rd], bin(reg_arr[rd]))
        pc+=4
        cycle[0]+=1
        cycle[1]+=4
        cycle[2]+=1
        cycle[4]+=1
        percentage[0]+=1     #ALU based instruction 
        x+=1
        
    elif op[0:6]=="000100":
        print("BEQ")
        rs=int(op[6:11], 2)
        print("RS: ", rs)
        rt=int(op[11:16], 2)
        print("RT: ", rt)
        cycle[0]+=1   #single cycle
        cycle[1]+=3   #multi cycle
        cycle[3]+=1   #3 steps
        percentage[1]+=1     #Branch based instruction
        print("---------------------Previous $", hazard[0])
        print("---------------------BEQ      $", rs)
        if hazard[0] == rs:
            if dic == hazard[1] + 1:
                hazard[2]+=1
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
            print("Branch Complete..Stalling..")
        else:
            pc+=4
            cycle[2]+=1
            x+=1
    elif op[0:6]=="000101":
        print("BNE")
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        offset=int(op[16:32], 2)
        cycle[0]+=1
        cycle[1]+=3
        cycle[3]+=1
        percentage[1]+=1     #Branch based instruction
        print("---------------------Previous $", hazard[0])
        print("---------------------BEQ      $", rs)
        if hazard[0] == rs:
            if dic == hazard[1] + 1:   #check if same register is being accessed ONE
                                        #instr after
                hazard[2]+=1
    
        if op[16]=="1":
            offset = -(65535 -int(op[16:32],2)+1)  #incase the offset is negative
            print("offset when MSB is 1: ", offset)
        else:
            offset=int(op[16:32], 2)
        if reg_arr[rs]!=reg_arr[rt]: #if register values are not equal we will branch
            pc+=4
            pc=pc+(int(offset)*4)    #altering pc based on what i found on the internet
            cycle[2]+=2              #increasing pipeline count
            x=x+1+offset
            print("Branching..Stalling..")
        else:
            pc+=4
            cycle[2]+=1
            x+=1
            print("No Branch Necessary.")
    elif op[0:6]=="000000" and op[26:32]=="101010":
        print("SLT")
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
        percentage[0]+=1     #ALU based instruction 
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
        rs=int(op[6:11], 2)
        rt=int(op[11:16], 2)
        offsetforcache=op[16:32]
        offset=int(op[16:32], 2)
        kk=reg_arr[rs]+offset-8192 #you put -8912, but should be -8192 lol
        print("Offset: ", kk)
        print("memory: ", memREE[kk])
        print("Register and its value: register", rs, reg_arr[rs]) #A.E instead of rt, should be rs
        reg_arr[rt]=memREE[kk]    
        cycle[0]+=1
        cycle[1]+=5
        cycle[2]+=2
        cycle[5]+=1
        percentage[2]+=1     #Memory based instruction 
        x+=1
        pc+=4
        kk=reg_arr[rs]+offset  #These lines down I troubleshot for hours until some
        kk=bin(kk)             #thing worked
        kk=kk.zfill(16)        #this was a sanity check
        print("KK:", kk)       #I print this in case i need to debug
                               # "kk" is just a value i stored the offset+register in
                               #plus i didn't know what to call this value
        cacheMeOusside(kk, cache, tags, tagsd, LRU) #jump to function that performs the cache assignments (part 3)
    elif op[0:6]=="101011":
        print("SW")
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
        percentage[2]+=1     #Memory based instruction
        x+=1
    return [op, reg_arr, pc, cycle, x, cache, tags, tagsd, LRU]
#sim: simulates the MIPS hex code
#inputs: file name of txt that carries the instructions
def sim(MIPS_HEX):
    LRU=numpy.zeros((8))  #this will be matrix for LRU
    tags=[0, 0, 0, 0, 0, 0]  #these tags are [a0, a1, b0, b1, b2, b3]
    tagsd=numpy.zeros((8))  #this will be a matrix or tags of part d
    cache=[0, 0, 0, 0, 0, 0, 0, 0]  #[part a miss, part a hit, part b miss...part c hit]
    x=0   #this is to configure pc back to 1 increments instead of 4 so I can make it easier to read my input files
    pc = 0 #initialize pc and register array
    reg_arr = [0, 0, 0, 0, 0, 0, 0, 0] #registers [$0, $1, $2, $3, $4, $5, $6, $7]
    cycle=[0, 0, 0, 0, 0, 0] #this array will work like so [single cycle, multi cycle, pipeline, 3cycle, 4cycle, 5cycle]
    #create file variables from file name strings
    percentage=[0, 0, 0, 0] #A.E. array for instct percentages [ALU, BRANCH, MEMORY, other] since JUMP
                            #will always be zero since our program does not cover that instr
    hazard=[0,0,0]      #A.E. [$RD, PC, HazardCount]
    hazard[2] = 0
    instr_mem_input = open(MIPS_HEX, "r")#read file for programming instructions
    instr_mem = file_to_array(instr_mem_input)
    dic=0   #dynamic instruction will be counted
    i=1      #used to printout hazards when ever they occur
    while x < len(instr_mem):
        op = instr_mem[x]
        print("PC: ", pc, hex(pc))
        data_set = execute_operation(op, reg_arr, pc, cycle, x, percentage, hazard,dic, cache, tags, tagsd, LRU)
        reg_arr = data_set[1]
        pc=data_set[2]
        cycle=data_set[3]
        x=data_set[4]
        print("OP: ", op)
        print("Register Array:", reg_arr)#prints for each instruction so we can see what is being stored in each register
        print("Cycle:", cycle)
        dic+=1 #increment DIC by 1 everytime we perform an instruction
        print("D.I.C: ", dic)
        print("\n")
        
        if(i == hazard[2]):
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!! Total Hazards: ", hazard[2])
            i+=1
        if x>1000:
            break

    print("Dynmic Instruction Count: ", dic, "\nPC: ", pc)
    print("Single Cycle Count:       ", cycle[0])
    print("Multi Cycle Count:        ", cycle[1])
    print("Count 3 Step Cycles:      ", cycle[3])
    print("Count 4 Step Cycles:      ", cycle[4])
    print("Count 5 Step Cycles:      ", cycle[5])
    cycle[2]+=4
   
    print("Pipeline Cycle count:     ", hazard[2]+cycle[2])
    print("Below is a listing of the final values for each register: \n")
    print("$1 = ", reg_arr[1], "\n$2 = ",reg_arr[2], "\n$3 = ",reg_arr[3])
    print("$4 = ", reg_arr[4], "\n$5 = ", reg_arr[5], "\n$6 = ", reg_arr[6])
    print("$7 = ", reg_arr[7])
    print("Memory display: ...")
    cashmoney = cache[0] + cache[1]    #totaling the hit/miss from part a
    print("Total times accessed cache DM 4 words, 2 blocks: ", cashmoney)
    print("Total hits: ", cache[1])
    print("Total misses: ", cache[0])
    biggiesmalls = 100*(cache[1]/(cache[0]+cache[1]))
    print("Cache Hit Ratio: ", biggiesmalls, "%")
    print("Total times accessed cache DM 2 words, 4 blocks: ", cashmoney)
    print("Total hits: ", cache[3])
    print("Total misses: ", cache[2])
    biggiesmalls =100*(cache[3]/(cache[2]+cache[3]))
    print("Cache Hit Ratio: ", biggiesmalls, "%")
    cashmoney= cache[6] + cache[7]
    print("Total times accessed cache from set associative 2-way: ", cashmoney)
    print("Total hits: ", cache[7])
    print("Total misses: ", cache[6])
    biggiesmalls = 100*(cache[7]/(cache[6]+cache[7]))
    print("Cache Hit Ratio: ", biggiesmalls)
    i=0
    for i in range(0, 4096, 4):
        if int(memREE[i]) != 0:
            print("Memory ",i,":" '%8s' % memREE[i])
    print("--------------------------------")
    print("Instrution percentages")
    print("ALU:", '%10s' % round(100 *(percentage[0] / dic)), "%")
    print("Jump:" '%10s' % "0%")
    print("Branch:", '%7s' % round(100 *(percentage[1] / dic)), "%")
    print("Memory:", '%7s' % round(100 *(percentage[2] / dic)), "%")
    print("Other:" '%9s' % round(100 *(percentage[3] / dic)), "%")

memREE = [0]*4096 #initialize to list of 4096 none's
#sim("i_mem.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_a.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_b.txt")
#print("\n\n\n\n\n\n\n\n")
sim("sample_c.txt")
#print("\n\n\n\n\n\n\n\n")
#sim("sample_d.txt")
