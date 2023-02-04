# Konstantinos Themeliotis 

# This is a compiler for programming language minimal++
# This current file contains:
#   -   The Lexical Analyzer
#   -   The Syntax analyzer,
#   -   The Intermediate code generator
#   -   The Symbol table 
#   -   The Semantic analysis 
#   -   The Final Code generator
# 
# 
# The purpose is to compile a Minimal++ file and produce an equivelant assembly MIPS file
# To execute compiler in Linux enviroment --> cd to files directory and type: python3 mnmal.py <filename>.min  eg: python3 mnmal.py testi2.min
# To execute compiler in Windows enviroment --> cd to files directory and type : mnmal.py <filename>.min eg mnmal.py testi2.min
# After compilation 3 new files are created: intermediate.int wich contains the intermediate code 
# cFIle.c which contanins the C code and the <filename>.asm which contains the assembly code
 



import sys
import string
import pdb

#-----------------------Initializing variables----------------------------------

#Defining the Automats States
state_0 = 0
state_1 = 1
state_2 = 2
state_3 = 3
state_4 = 4 
state_5 = 5
state_6 = 6
state_7 = 7
state_8 = 8
state_9 = 9
error_state = -1
final_state = -2
eof_state = -3

#Minimall++ alphabet 
blank = 0     #white character  
letter = 1    #a-z or A-Z
digit = 2     #0-9
plus = 3      #+
minus = 4     #-
multi = 5     #*
divide = 6    #/
equals = 7    #=
smaller = 8   #<
bigger = 9    #>
colon = 10    #:
comma = 11    #,
semicolon = 12 #;
left_parenthesis = 13  #(
right_parenthesis = 14 #)
left_semicolon = 15    #[
right_semicolon = 16   #]
eof = 17
new_line = 18     #/n
left_bracklet = 19     #{
right_bracklet = 20    #}

#Commited Words 
commited_words = ['program', 'declare', 
                'if', 'else', 'then',
                'while' ,
                'forcase',  'when', 'default', 
                'not', 'and', 'or', 
                'function', 'procedure', 'call', 'return', 'in', 'inout', 
                'input', 'print' ]

#State Diagram: Rows represent the Automats states and columns represent Automats inputs
#The element represent the next state of the Automat
state_diagram = [
    [0, 1, 2, -2, -2, -2, 3, -2, 7, 8, 9, -2, -2, -2, -2, -2, -2, -3, 0, -2, -2],                  #state0
    [-2, 1, 1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],            #state1
    [-2, -2, 2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],           #state2
    [-2, -2, -2, -2, -2, 5, 4, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],            #state3
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 4, 4],                               #state4
    [5, 5, 5, 5, 5, 6, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],                               #state5
    [5, 5, 5, 5, 5, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],                               #state6
    [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2],          #state7
    [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2,-2 ,-2 ,-2 ,-2 ,-2 ,-2 , -2 , -2],         #state8
    [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2]]          #state9



# Input and output file opening - The file is given as a parameter in terminal

# No given input
if len(sys.argv) == 1 : 
    print("\nError: No file is given as input. Make sure you give only 1 file as a parameter")
    print("eg: mnmal.py testi.min")
    print("Process terminated")
    sys.exit(0)

# Too many argumets
elif len(sys.argv) > 2 :
    print("\nError: Too many file input arguments. Make sure you give only 1 file as a parameter!")
    print("eg: mnmal.py testi.min")
    print("Process terminated")
    sys.exit(0)
    
else :
    filename = sys.argv[1].split('.')
    if filename[1] == 'min' :
        input_file = open(str(sys.argv[1]),'r')
        output_final_file = open(filename[0] + '_FinalCode.asm', 'w')
    # Wrong file format
    else : 
        print("\nError: Wrong input file type. File must end with .min")
        print("eg: mnmal.py " + str(filename[0] + '.min'))
        print("Process terminated")
        sys.exit(0)



input_file = open(str(sys.argv[1]),'r')

#------------------------------------Lex-------------------------------------------
# Lexical analyzer (lex()) Global variables
tokens = ['','']    # Lexical units, tokens[0] contains the unit, tokens[1] the units token
lines_number = 1 
bytes_read = 0
char_read = '' 

def lex():
    
    global bytes_read
    global lines_number
    global tokens
    buffer = ''
    current_state = 0
    automat_input = 0
        
    while current_state != final_state and current_state != error_state :
        
        char_read = input_file.read(1)  #every char read by lex
        bytes_read += 1
        if char_read == '\n': #lines_counter 
            lines_number += 1
            bytes_read += 1
        if not char_read :
            automat_input = eof
        if char_read.isspace():
            automat_input = blank
        if char_read.isalpha():
            if current_state == state_2:
                continue
            else:
                buffer = buffer + char_read
            automat_input = letter
        if char_read.isdigit():
            automat_input = digit
            buffer = buffer  + char_read
        if char_read == '+':
            automat_input = plus
        if char_read == '-':
            automat_input = minus
        if char_read == '/':
            automat_input = divide
        if char_read == '*':
            automat_input = multi
        if char_read == '<':
            automat_input = smaller
        if char_read == '>':
            automat_input = bigger
        if char_read == '=':
            automat_input = equals
        if char_read == ':':
            automat_input = colon
        if char_read == ',':
            automat_input = comma
        if char_read == ';':
            automat_input = semicolon
        if char_read == '[':
            automat_input = left_semicolon
        if char_read == ']':
            automat_input = right_semicolon
        if char_read == '(':
            automat_input = left_parenthesis
        if char_read == ')':
            automat_input = right_parenthesis
        if char_read == '{':
            automat_input = left_bracklet
        if char_read == '}':
            automat_input = right_bracklet
        if char_read == '\n':
            automat_input = new_line
        
        # Changing state using state diagram
        previous_state = current_state
        current_state = state_diagram[current_state][automat_input] 
        
        # Discarding line comments
        if previous_state == state_4 : 
            if char_read == '\n' : 
                current_state = state_0
                previous_state = state_0
                tokens[0] = ''
                tokens[1] = ''
                buffer = ''

        # Discarding multiple line comments
        if previous_state == state_5:
            if char_read == '\n' :
                lines_number += 1
            if char_read == eof : 
                print("Error: Multiline comment started but did not close, line: " + str(lines_number))
                sys.exit(1)
        
        # Discarding multiple line comments       
        if previous_state == state_6:
            if char_read == '/':
                current_state = state_0
                previous_state = state_0
                tokens[0] = ''
                tokens[1] = ''
                buffer = ''
            
            if char_read == eof : 
                print("Error: Multiline comment started but did not close, line: " + str(lines_number))
        
        # If we hit final state or it's the eof then we check which state brought the automat to its final state
        if current_state == final_state or automat_input == eof :
            if previous_state == state_0:
                if automat_input == eof :
                    tokens[0] = 'eof'
                    tokens[1] = 'eoftk'
                    break
                if current_state != state_4 : 
                    tokens[0] = char_read
                    tokens[1] = char_read + 'tk'
             
            if previous_state == state_1:
                found_commited_word = False
                for i in range(len(commited_words)):
                    if buffer == commited_words[i]:
                        tokens[1] = commited_words[i] + 'tk'
                        found_commited_word = True
                if found_commited_word == False:
                    tokens[1] = 'idtk'
                
                tokens[0] = buffer
                if char_read.isspace() == False and char_read != '\n': #Should see again!
                    bytes_read -= 1
                    input_file.seek(bytes_read,0)
            
            if previous_state == state_2:
                tokens[0] = buffer
                tokens[1] = 'constant'
                
                if int(tokens[0]) > 32767 or int(tokens[0]) < -32767 : 
                    print("Error: Constant values must be between -32767 and 32767")
                    sys.exit(0)
                
                if char_read.isspace() == False and char_read != '\n':
                    bytes_read -= 1
                    input_file.seek(bytes_read,0)
            
            if previous_state == state_3:
                if char_read != '/' or char_read != '*':
                    tokens[0] = '/'
                    tokens[1] = '/tk'
                                
           
            if previous_state == state_7:
                if char_read == '=':
                    tokens[0] = '<='
                    tokens[1] = '<=tk'
                elif char_read == '>':
                    tokens[0] = '<>'
                    tokens[1] = '<>tk'
                else:
                    #regression
                    if char_read.isspace() == False and char_read != '\n':
                        bytes_read -= 1
                        input_file.seek(bytes_read,0)
                    tokens[0] = '<'
                    tokens[1] = '<tk'
            
            if previous_state == state_8:
                if char_read == '=':
                    tokens[0] = '>='
                    tokens[1] = '>=tk'
                else:
                    tokens[0] = '>'
                    tokens[1] = '>tk'
                    #regression
                    if char_read.isspace() == False and char_read != '\n':
                        bytes_read -= 1
                        input_file.seek(bytes_read,0)
          
            if previous_state == state_9:
                if char_read == '=':
                    tokens[0] = ':='
                    tokens[1] = ':=tk'
                else:
                    tokens[0] = ':'
                    tokens[1] = ':tk'
                    if char_read.isspace() == False and char_read != '\n':
                        bytes_read =- 1
                        input_file.seek(bytes_read,0)

            current_state = state_0
            buffer = ''
            return
    
    

#------------------Intermediate_Code-----------------------------

# Intermediate code Global variables
quads_list = []
temp_var_counter = 0

# Intemediate code Auxiliery functions

def nextQuad() :
    global quads_list
    return len(quads_list)


def genQuad(op,x,y,z) :
    global quads_list
    quads_list.append([op,x,y,z])


def newTemp() :
    global temp_var_counter
    temp_var_name = "T_" + str(temp_var_counter)
    temp_var_counter += 1
    create_new_entity(temp_var_name,"variable","") #Final Code   
    return temp_var_name


def emptyList() :
    return list()
 

def makeList(x) :
    return [x]


def merge(list_1,list_2) : 
    return list_1 + list_2


def backPatch(list,z) :
    for element in list :
        quads_list[element][3] = z

# Creating output files

# Creating int file  
def createInt_File() :
    global quads_list
    int_file = open(str(filename[0]) + '_IntFile.int', "w")
    for i in range(len(quads_list)) :
        int_file.write(str(i) + ": " + str(quads_list[i]) + "\n")
    
    int_file.close()
    return


# Creating equivalent C code
def createC_File():
    global quads_list
    c_file = open(str(filename[0]) + "_CFile.c", "w")
    c_file.write("#include <stdio.h>\n")
    c_file.write("#include <stdlib.h>\n")
    c_file.write("int main(void) {\n")
    output_Var(c_file)
    c_file.write("After")
	
    for i in range(len(quads_list)):
        c_file.write("\tL_" + str(i) + ": " + str(get(quads_list[i])) + "; // " + str(quads_list[i]) + "\n")

    c_file.write("}\n") #final brack - return 0 in C?
    c_file.close()
    return


def output_Var(c_file):
	varlist = []
	for item in quads_list:
		if item[0] == "begin_block" or item[0] == "end_block":
			continue
		for i in range(1, 4):
			if not str(item[i]).isdigit() and item[i] != "_" and not item[i] in varlist:
				varlist.append(item[i])
	for item in varlist:
		c_file.write("\tint " + str(item) + ";\n")
	c_file.write("\n")


def get(quad):
	if quad[0] in ["begin_block", "end_block", "halt",  "RET", "call", "par"]:
		return ""
	elif quad[0] == "jump":
		return "goto L_" + str(quad[3])
	elif quad[0] == ":=":
		return quad[3] + " = " + str(quad[1])
	elif quad[0] == "<>":
		return "if (" + str(quad[1]) + " != " + str(quad[2]) + ") goto L_" + str(quad[3])
	elif quad[0] == "=":
		return "if (" + str(quad[1]) + " == " + str(quad[2]) + ") goto L_" + str(quad[3])
	elif quad[0] == "inp":
		return 'scanf("%d\\n", ' + "&" + str(quad[1]) + ")"
	elif quad[0] == "out":
		return 'printf("%d\\n", ' + str(quad[3]) + ")"
	elif quad[0] in ["<", ">", "<=", ">="]:
		return "if (" + str(quad[1]) + " " + str(quad[0]) + " " + str(quad[2]) + ") goto L_" + str(quad[3])
	elif quad[0] in "+-*/":
		return str(quad[3]) + " = " + str(quad[1]) + " " +str(quad[0]) + " " + str(quad[2])




#-------------------Symbol_Table---------------
# A list which consists of scope items and every scope item has an Entity list
scope_list = list()

# Objects-Classes that make up the symbol table

class Entity:
    # Default constructor
    def __init__(self, Name, Type, offset, par_mode) :
        self.Type = Type
        self.Name = Name
        
        if Type == "variable" :
            self.offset = offset
        
        elif Type == "function" :
            self.function = par_mode  #REF or RET par passing mode
            self.start_quad = 0       #first quad
            self.argument_list = list()
            self.framelength = 0      #graphs length
        
        elif Type == "parameter" :
            self.par_mode = par_mode
            self.offset = offset
        
        else : 
            print("False Entity Class contructor")


class Scope : 
    # Class Default constructor
    def __init__(self):
        self.offset = 12
        self.entity_list = list()
    
    
    # Add a new Entity to currents Scope Entity list
    def add_Entity(self,entity) :
        self.entity_list.append(entity)
        self.offset += 4
    

    # Add a new argument to the last Entity item in current Scope
    def add_Argument(self, par_mode) :
        self.entity_list[-1].argument_list.append(par_mode)


# Auxiliery function for symbol table

def add_new_Scope() :
    global scope_list
    scope_list.append(Scope())


def delete_Scope() :
    global scope_list
    scope_list.pop()


def create_new_entity (name, Type, par_mode) :
    global scope_list

    if Type == "variable" :
        offset = scope_list[-1].offset
        scope_list[-1].add_Entity(Entity(name, Type, "", offset))
    
    elif Type == "function" : 
        scope_list[-1].add_Entity(Entity(name, Type, par_mode, 0))
    
    elif Type == "parameter" :
        offset = scope_list[-1].offset
        scope_list[-1].add_Entity(Entity(name, Type, par_mode, offset))
    
    else :
        print("Invalid Type parameter")


def add_new_argument(par_mode) :
    global scope_list
    scope_list[-2].add_Argument(par_mode)


def search_Entity(name) :
    global scope_list
    for i in range(len(scope_list)-1, -1, -1) : 
        for j in range (0, len(scope_list[i].entity_list)) : 
           
            if name == scope_list[i].entity_list[j].Name : 
                return(scope_list[i].entity_list[j], i )
    
    return None, None 



def get_main_offset() : 
    global scope_list
    return scope_list[0].offset



def get_Current_Scope() : 
    global scope_list
    return len(scope_list) - 1


def is_current_scope(name) :
    global scope_list
    for i in range(0,len(scope_list[- 1].entity_list)) :
        if name == scope_list[- 1].entity_list[i].Name : 
            return True #exists in current scope
    
    return False


def set_start_quad(quad) : 
    global scope_list
    if len(scope_list) == 1 :
        return
    else :
        scope = scope_list[-1]
        entity = scope.entity_list[-1]
        entity.start_quad = quad


def set_FrameLength() : 
    global scope_list
    last_scope = scope_list[-1]
    current_scope = scope_list[-1]
    entity = last_scope.entity_list[-1]
    entity.framelength = current_scope.offset


#-------Semantic analysis-------------

# Checks for already declared var
def is_declared (var) :
    if is_current_scope(var) == True :
        print("ID" + var + "already exists in current scope")
        sys.exit(1)


# Checks for undeclared var
def is_undeclared(var) :
    found = search_Entity(var)
    if found == None : 
        print("Id" + var + "has already been declared")
        sys.exit(1)


#-------------------------Final_Code-------------------------------

# Basic Auxiliery Functions used to create the final code in assembly Mips

# Transfers a non-local variables address, to register $t0 
def gnvlcode(v) : 
    
    v_entity, nesting_level = search_Entity(v)
    
    output_final_file.write("lw $t0, -4($sp)\n")
    
    for i in range(get_Current_Scope() - nesting_level) :
        output_final_file.write("lw $t0, -4($t0)\n")
    
    output_final_file.write("add $t0, $t0, -" + str(v_entity.offset) + "\n")


# Transfers data to register r
def loadvr(v, r) : 
    v_entity, nesting_level = search_Entity(v)
    
    if v_entity == None :   #Constant
        output_final_file.write("li $t" + r + ", " + str(v) + "\n")
    else :
        dif_scope = get_Current_Scope() - nesting_level
        
        # Global variable-Belongs to main
        if nesting_level == 0 : 
            output_final_file.write("lw $t" + r + ", -" + str(v_entity.offset) + "($s0)\n")
        else :
            
            # Nesting level = current 
            if dif_scope == 0 :
                
                # Variable or parameter by RET
                if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "CV") :
                    output_final_file.write("lw $t" + r + ", -" + str(v_entity.offset) + "($sp)\n")
                
                # Parameter by REF 
                elif v_entity.Type == "parameter" and v_entity.par_mode == "REF":
                    output_final_file.write("lw $t0" + ", -" + str(v_entity.offset) + "($sp)\n")
                    output_final_file.write("lw $t" + r + ", ($t0)\n")
                # Error
                else :
                    output_final_file.write("Something went wrong at loadvr(v, r) function\n") 
                    print("Something went wrong at loadvr(v, r ) function")
                    sys.exit(0)
            else :
                # Nesting level < current
                if dif_scope != 0 :
                    
                    # Variable or Parameter by RET
                    if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "CV") :
                        gnvlcode(v)
                        output_final_file.write("lw $t" + r + ", ($t0)\n")
                    
                    # Variable or Parameter by REF 
                    elif v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "REF") :
                        gnvlcode(v)
                        output_final_file.write("lw $t0, ($t0)\n")
                        output_final_file.write("lw $t" + r + ", ($t0)\n")
       
                    else :
                        output_final_file.write("Something went wrong at loadvr(v, r) function\n") 
                        print("2.Something went wrong at loadvr(v, r ) function\n")
                        sys.exit(0)


# Transfers data from register r to memory (variable v) 
def storerv(r, v) : 
    v_entity, nesting_level = search_Entity(v)

    
    # Global variable-Belongs to main
    if nesting_level == 0 : 
        output_final_file.write("sw $t" + r + ", -" + str(v_entity.offset) + "($s0)\n")
    else :
        
        dif_scope = get_Current_Scope() - nesting_level
        
        # Nesting level = current
        if dif_scope == 0  : 
            
            # Variable or Parameter by RET
            if (v_entity.Type == "parameter" and v_entity.par_mode == "CV") or (v_entity.Type == "variable") :
                output_final_file.write("sw $t" + r + ", -" + str(v_entity.offset) + "($sp)\n")
            
            # Parameter by REF
            elif  v_entity.Type == "parameter" and v_entity.par_mode == "REF" :
                output_final_file.write("lw $t0" + ", -" + str(v_entity.offset) + "($sp)\n")
                output_final_file.write("sw $t" + r + ", ($t0)\n")
            # Some kind of error
            else : 
            
                output_final_file.write("Something went wrong at store(r, v) function\n") 
                print("1.Something went wrong at store(r, v) function ")
                sys.exit(0)
        else : 
            # Nesting level < current            
            if dif_scope > 0 :
                
                # Variable or Parameter by RET
                if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "CV") : 
                    gnvlcode(v)
                    output_final_file.write("sw $t" + r + ", ($t0)\n")
                
                # Variable or Parameter by REF
                elif v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "REF") :
                    gnvlcode(v)
                    output_final_file.write("lw $t0, ($t0)\n")
                    output_final_file.write("sw $t" + r + ", ($t0)\n")
               
                else : # Some kind of error
                    output_final_file.write("Something went wrong at store(r, v) function\n") 
                    print("2.Something went wrong at store(r, v) function ")
                    sys.exit(0)





begin_flag = True
quad_count = 0

# Producing final code by using intermediate code quads
def produce_final_code() :
    global begin_flag
    global quad_count
    global scope_list
    par_number = 0 

    if begin_flag == True : 
        output_final_file.write("j Lmain\n") #First label
        begin_flag = False
    
    for i in range(quad_count, len(quads_list)) : 
        
        quad = quads_list[i]
        output_final_file.write("L" + str(i) + ":\n")   
        
        # jump , "_", "_", label 
        if quad[0] == "jump" :
            output_final_file.write("j L" + str(quad[3]) + "\n")
        
        # relop x, y, z
        elif quad[0] == "<" or quad[0] == ">" or quad[0] == "<=" or quad[0] == ">=" or quad[0] == "=" or quad[0] == "<>" :
            loadvr(quad[1], "1")
            loadvr(quad[2], "2")
            output_final_file.write(get_branch(quad[0]) + " $t1, $t2, L\n")
        
        # :=, x, "_", z
        elif quad[0] == ":=" :
            loadvr(quad[1], "1")
            storerv("1", quad[3])
        
        # op, x, y, z
        elif quad[0] == "+" or quad[0] == "-" or quad[0] == "*" or quad[0] == "/" :
            loadvr(quad[1], "1")
            loadvr(quad[2], "2")
            output_final_file.write(get_op(quad[0]) + " $t1, $t1, $t2\n")
            storerv("1", quad[3])
        
        # out, "_", "_", x
        elif quad[0] == "out" : 
            output_final_file.write("li $v0, 1\n")
            loadvr(quad[0], "0")
            output_final_file.write("add $a0, $t1, 0\n")
            output_final_file.write("syscall\n")
        
        # inp, "_", "_", x
        elif quad[0] == "inp" :
            output_final_file.write("li $v0, 1\n")
            output_final_file.write("syscall\n")
            output_final_file.write("move $t0, $v0\n")
            storerv("0", quad[1])
        
        # retv "_", "_", x
        elif quad[0] == "retv" : 
            loadvr(quad[1], "1")
            output_final_file.write("lw $t0, -8($sp)\n")
            output_final_file.write("sw $t1, ($t0)\n")
        
        # Function parameters
        elif quad[0] == "par" :
            v_entity, nesting_level = search_Entity(quad[1])
            dif_scope = get_Current_Scope() - nesting_level
            offset = v_entity.offset
            
            # Before first parameter
            if par_number == 0 :
                v_entity, nesting_level = search_Entity(quad[1])
                framelength = v_entity.offset
                output_final_file.write("add $fp, $sp, " + str(framelength) + "\n")
            
            # par, x, CV, _
            if quad[2] == "CV" : 
                loadvr(quad[1], "0")
                output_final_file.write("sw $t0, -" + str(12+4*par_number) + "($fp)\n")
            
            # par, x, REF, _
            elif quad[2] == "REF" : 
                # Cases for REF                           
                if dif_scope == 0 : 
                    if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "CV") :
                        output_final_file.write("add $t0, $sp, -" + str(offset) + "\n")
                        output_final_file.write("sw $t0, -" + str(12+4*par_number) + "($fp)\n")
                    else : 
                        if v_entity.Type == "parameter" and v_entity.par_mode == "REF" :
                            output_final_file.write("lw $t0, -" + str(offset) + "($sp)\n")
                            output_final_file.write("sw $t0, -" + str(12+4*par_number) + "($fp)\n")
                elif dif_scope > 0 :
                    if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "CV" ) : 
                        gnvlcode(quad[1])
                        output_final_file.write("sw $t0, -" + str(12+4*par_number) + "($fp)\n")
                    else : 
                        if v_entity.Type == "variable" or (v_entity.Type == "parameter" and v_entity.par_mode == "REF") : 
                            gnvlcode(quad[1])
                            output_final_file.write("lw $t0, ($t0)\n")
                            output_final_file.write("sw $t0, -" + str(12+4*par_number) + "($fp)\n")
                else : 
                    print("Error during final code producing")
            
            # par, x, RET, _
            elif quad[2] == "RET" : 
                output_final_file.write("add $t0, $sp, -" + str(offset) + "\n")
                output_final_file.write("sw $t0, -8($fp)\n")
                par_number += 1
        
        # call, f, _, _
        elif quad[0] == "call" :
            f_entity, f_nesting_level = search_Entity(quad[1])

            
            if f_nesting_level == len(scope_list) : #Same nesting level
                output_final_file.write("lw $t0, -4($sp)\n")
                output_final_file.write("sw $t0, -4($fp)\n")
            else :  # different nesting level
                output_final_file.write("sw $sp, -4($fp)\n")
            
            
            output_final_file.write("add $sp, $sp, " + str(f_entity.framelength) + "\n")
            output_final_file.write("jal L" + str(f_entity.start_quad) +"\n")
            output_final_file.write("add $sp, $sp, -" + str(f_entity.framelength) + "\n")
            par_number = 0

        # begin block   
        elif quad[0] == "begin_block" : 
            if quad[1] == "__main" : 
                output_final_file.write("add $sp, $sp\n")
                output_final_file.write("move $s0, $sp\n")
            else : 
                output_final_file.write("sw $ra, ($sp)\n")
        # end block
        elif quad[0] == "end_block" : 
            if quad[1] != "__main" : 
                output_final_file.write("lw $ra, ($sp)\n")
                output_final_file.write("jr $ra\n")
        
        quad_count = nextQuad()


# Some more auxiliery function

def get_branch(relop) : 
    if relop == "=" : 
        return "beq"
    elif relop == ">" : 
        return "bgt"
    elif relop == "<" : 
        return "blt"
    elif relop == ">=" : 
        return "bge"
    elif relop ==  "<=" : 
        return "ble"
    else :
        return "bne"  



def get_op(operator) : 
    if operator == "+" : 
        return "add"
    elif operator == "-" : 
        return "sub"
    elif operator == "*" : 
        return "mul" 
    else : 
        return "div"


 
        


#--------------------Syntax--------------------

has_return = False
subprograms_list = list()
is_procedure = False


def program() :
    if tokens[1] == 'programtk' :
        lex()
        if tokens[1] == 'idtk' :
            program_ID = tokens[0]
            lex()
            if tokens[1] == '{tk' :
                add_new_Scope() # Beggining of main programm scope
                lex()
                block(program_ID)
                set_FrameLength()
                if tokens[1] == '}tk' :
                    genQuad("halt", "_", "_", "_")  
                    genQuad("end_block", program_ID, "_", "_")
                    produce_final_code() 
                    delete_Scope()  # deletes final scope
                    lex()
                    if tokens[1] == 'eoftk' :
                        # Compilation Completed
                        print("")
                    else :
                        # If we reach here no output file will be created
                        print("Some kind o error")
                        sys.exit(1)
                else :
                    print(tokens[0],tokens[1])
                    print("Syntax error: } is missing to close program bracklet ")
                    sys.exit(1)
            else:
                print("Syntax error: expected { to open keyword 'program' brackelt ")
                sys.exit(1)
        else :
            print("Syntax error: program ID is missing")
            sys.exit(1)
    else :
        
        print("Syntax error: 'program' statement is missing ")
        sys.exit(1)

def block(block_ID) :
    declarations()
    subprograms()
    if block_ID != None :
        set_start_quad(nextQuad())
        genQuad("begin_block", block_ID, "_", "_")
    
    statements()


def declarations() :
    while tokens[1] == 'declaretk' :
        lex()
        varlist()
        if tokens[1] == ';tk' :
            lex()
        else:
            print("Syntax error: Expected ; after declaration, line: " + str(lines_number))
            sys.exit(1)


def varlist() :
    if tokens[1] == 'idtk' :
        is_declared(tokens[0])   # checks for already declared 
        create_new_entity(tokens[0], "variable", "")    #new var
        lex()
        while tokens[1] == ',tk' :
            lex()
            if tokens[1] == 'idtk' :
                is_declared(tokens[0])
                create_new_entity(tokens[0], "variable", "")     #new var
                lex()
            else :
                print("SyntaxError: Expected id , line: " + str(lines_number))
                sys.exit(1)

def subprograms() :
    while tokens[1] == 'functiontk' or tokens[1] == 'proceduretk' :
        subprogram()


def subprogram():
    global is_procedure
    global has_return
    has_return = False
    
    if tokens[1] == 'functiontk' :
        is_procedure = False
        lex()
        if tokens[1] == 'idtk' :
            sub_ID = tokens[0]
            is_declared(tokens[0]) # Checks for already declared function
            create_new_entity(tokens[0], "function", "")
            add_new_Scope()
        else :
            print("Syntax Error: Function ID expected , line: " + str(lines_number))
            sys.exit(1)
    elif tokens[1] == 'proceduretk' :
        is_procedure = True 
        lex()
        if tokens[1] == 'idtk' :
            sub_ID = tokens[0] 
            is_declared(tokens[0])
            create_new_entity(tokens[0], "function", "")
            add_new_Scope()
        else : 
            print("Syntax Error: Procedure ID expected , line: " + str(lines_number))

    lex()
    subprograms_list.append(sub_ID)
    funcbody(sub_ID)




def funcbody(Function_ID) :
    global is_procedure
    global has_return
    formalpars()
    if tokens[1] == '{tk' :
        create_new_entity(Function_ID,"function","")
        add_new_Scope()
        lex()
        block(Function_ID)
        if tokens[1] == '}tk' :
            set_FrameLength()
            
            genQuad("end_block",Function_ID, "_", "_")
            produce_final_code()
            delete_Scope()
            lex()
            
            if is_procedure == True : 
                if has_return == True : # No returns allowed in procedure 
                    print("Found 'return' statement inside procedure")
                    sys.exit(1)
            else : #function
                if has_return == False : 
                    print('Missing return statement from function')
                    sys.exit(1) 
        
        else :
            print("SyntaxError: Expected }, line: " + str(lines_number))
            sys.exit(1)
    else :
        print("SyntaxError: Expected { , line: " + str(lines_number))
        sys.exit(1)


def formalpars() :
    if tokens[1] == '(tk' :
        lex()
        formalparlist()
        if tokens[1] == ')tk' :
            lex()
        else :
            print("Expected ) , line: " + str(lines_number)) 
            sys.exit(1)
    else :
        print("SyntaxError: Expected ( , line: " + str(lines_number))
        sys.exit(1) 


def formalparlist() :
    formalparitem()
    while tokens[1] == ',tk' :
        lex()
        formalparitem()

def formalparitem() :
    if tokens[1] == 'intk' :
        add_new_argument("RET")
        create_new_entity(tokens[0], "parameter", "RET")
        lex()
        if tokens[1] == 'idtk' :
            lex()
        else :
            print("Syntax error: Expected ID , line: " + str(lines_number))
            sys.exit(1)
    elif tokens[1] == 'inouttk' :
        add_new_argument("REF")
        create_new_entity(tokens[1], "parameter", "REF")
        lex()
        if tokens[1] == 'idtk' :
            lex()
        else :
            print("Syntax error: Expected ID " + str(lines_number))
            sys.exit(1)
    else :
        print("SyntaxError:In or inout keyword expected , line: " + str(lines_number) )
        sys.exit(1)
    

def statements() :
    if tokens[1] == '{tk' :
        lex()
        statement()
        while tokens[1] == ';tk' :
            lex()
            statement()
        
        if tokens[1] == '}tk':
            lex()
        else :
            print(tokens[0], tokens[1])
            print("SyntaxError : Expected } , line: " + str(lines_number))
            sys.exit(1)
    else :
        statement()
        

def statement() :
    global has_return
    if tokens[1] == 'idtk' :
        is_undeclared(tokens[0])
        assignment_stat()
    elif tokens[1] == 'iftk' :
        lex()
        if_stat()
    elif tokens[1] == 'whiletk' :
        lex()
        while_stat()
    elif tokens[1] == 'forcasetk' :
        lex()
        forcase_stat()
    elif tokens[1] == 'calltk' :
        lex()
        call_stat()
    elif tokens[1] == 'returntk' :
        has_return = True
        lex()
        return_stat()
    elif tokens[1] == 'inputtk' :
        lex()
        input_stat()
    elif tokens[1] == 'printtk' :
        lex()
        print_stat()
    else :
        print("")


def assignment_stat():
    temp_ID = tokens[0]
    lex()
    if tokens[1] == ':=tk':
        lex()
        genQuad(":=", expression(), "_", temp_ID)
    else :
        print("SyntaxError : Expected ':=' , line:" + str(lines_number))
        sys.exit(1)


def if_stat() :
    if tokens[1] == '(tk' :
        lex()
        (b_True, b_False) = condition()
        if tokens[1] == ')tk' :
            lex()
            if tokens[1] == 'thentk' :
                lex()
                backPatch(b_True, nextQuad())
                statements()
                if_List = makeList(nextQuad())
                genQuad("jump","_","_","_")
                backPatch(b_False, nextQuad())
                elsepart()
                backPatch(if_List, nextQuad())
            else :
                print("SyntaxError: Keyword 'then' expected, line: " + str(lines_number))
                sys.exit(1)
        else :
            print("Syntax error : Expected )?, line: " + str(lines_number))
            sys.exit(1)
    else :
        print("SyntaxError:Expected '(' , line: " + str(lines_number))
        sys.exit(1)

def elsepart() :
    if tokens[1] == 'elsetk' :
        lex()
        statements()
    else:
        print("ok")
        #statements()

def while_stat() :
    if tokens[1] == '(tk' :
        lex()
        q = nextQuad()
        (b_True, b_false) = condition()
        if tokens[1] == ')tk':
            lex()
            backPatch(b_True, nextQuad())
            statements()
            genQuad("jump","_","_",q)
            backPatch(b_false,nextQuad())
        else :
            print("SyntaxError : Expected ) , line: " + str(lines_number))
            sys.exit(1)
    else :
        print("SyntaxError: Expexted ( , line: " + str(lines_number))
        sys.exit(1)


def forcase_stat():
    
    exit_list = emptyList()
    forcase_quad = nextQuad()
    
    while tokens[1] == 'whentk' :
        lex()
        if tokens[1] == '(tk' :
            lex()
            (b_true, b_false) = condition()
            backPatch(b_true, nextQuad())
            if tokens[1] == ')tk' :
                lex()
                if tokens[1] == ':tk' :
                    lex()
                    statements()
                    quad = nextQuad()
                    list = makeList(quad)
                    genQuad("jump","_","_",quad)
                    exit_list = merge(exit_list,list)
                    backPatch(b_false, nextQuad())
                else :
                    print("SyntaxError : Expected : , line: " + str(lines_number))
                    sys.exit(1)
            else :
                print("SyntaxError : Expected ')' ,line: " + str(lines_number))
                sys.exit(1)
        else :
            print("ForCaseSyntaxError : Expected '(' , line: " + str(lines_number))
    if tokens[1] == 'defaulttk' :
        lex()
        if tokens[1] == ':tk' :
            lex()
            statements()
        else :
            print("SyntaxError : Expected ':' , line: " + str(lines_number))
    else :
        print("SyntaxError : Expected keyword 'default' , line: " + str(lines_number))


def return_stat() :
    exp = expression()
    genQuad("retv",exp,"_","_")


def call_stat() :
    if tokens[1] == 'idtk' :
        temp_ID = tokens[0]
        f_entity, nesting_level = search_Entity(tokens[0])
        temp_ID = tokens[0]
        lex()
        actualpars(f_entity)
        genQuad("call",temp_ID,"_","_")
    else :
        print("SyntaxError : Expected ID , line:" + str(lines_number))
        sys.exit(1)


def print_stat() :
    if tokens[1] == '(tk' :
        lex()
        expr = expression()
        genQuad("out","_","_",expr)
        if tokens[1] == ')tk' :
            lex()
        else :
            print("SyntaxError : Expected ')' , line: " + str(lines_number) )
            sys.exit(1)
    else :
        print("PrintStatSyntaxError : Expected '(' , line: " + str(lines_number))
        sys.exit(1)


def input_stat():
    if tokens[1] == '(tk' :
        lex()
        if tokens[1] == 'idtk' :
            genQuad("inp",tokens[0],"_","_")
            lex()
            if tokens[1] == ')tk' :
                lex()
            else :
                print("SyntaxError : Expected ')' , line: " + str(lines_number) )
        else :
            print("SyntaxError : Expected ID , line: " + str(lines_number) )
            sys.exit(1)
    else:
        print("InputStatSyntaxError: Expected '(' , line:" + str(lines_number))
        sys.exit(1)


def actualpars(f_entity) :
    if tokens[1] == '(tk' :
        lex()
        actualparlist(f_entity)
        if tokens[1] == ')tk' :
            lex()
        else :
            print("SyntaxError : Expected ')' , line:" + str(lines_number) )
            sys.exit(1)
    else:
        print(tokens[0],tokens[1])
        print("ActualParsSyntaxError : Expected '(' , line: " + str(lines_number))
        sys.exit(1)


def actualparlist(f_entity) :
    if tokens[1] == 'intk' or tokens[1] == 'inouttk':
        argument = 0
        actualparitem(f_entity, argument)
        while tokens[1] == ',tk' :
            argument += 1
            lex()
            actualparitem(f_entity, argument)


def actualparitem(f_entity, argument) :
    if tokens[1] == 'intk' :
        lex()
        genQuad("par",expression(),"CV","_") 
    
    elif tokens[1] == 'inouttk' :
       
        #if f_entity.argument_list[argument].par_mode == "REF" : 
            #print("Parameter mode declaration do not match")
       
        lex()
        if tokens[1] == 'idtk' :
            is_undeclared(tokens[0])
            genQuad("par", tokens[0], "REF", "_")
            lex()
        else :
            print("SyntaxError : ID Expected , line: " + str(lines_number))
            sys.exit(1)
    else :
        print("SyntaxError : 'in' or 'inoout' parameter mode expected , line: " + str(lines_number))
        sys.exit(1)


def condition() :
    (q1_true,q1_false) = boolterm()
    b_true = q1_true
    b_false = q1_false
    while tokens[1] == 'ortk' :
        lex()
        backPatch(b_false, nextQuad())
        (q2_true, q2_false) = boolterm()
        b_true = merge(b_true, q2_true)
        b_false = q2_false
    
    return(b_true, b_false)


def boolterm():
    
    (r1_true, r1_false) = boolfactor()
    q_true = r1_true
    q_false = r1_false
    while tokens[1] == 'andtk' :
        lex()
        backPatch(q_true, nextQuad())
        (r2_true, r2_false) = boolfactor()
        q_false = merge(q_false, r2_false)
        q_true = r2_true
    
    return (q_true, q_false)


def boolfactor():
    if tokens[1] == 'nottk' :
        lex()
        if tokens[1] == '[tk' :
            lex()
            (q1_true,q2_false) = condition()
            if tokens[1] == ']tk' :
                lex()
                return (q1_true, q2_false)
            else :
                print("SyntaxError : Expected ']' , line: " + str(lines_number))
                sys.exit(1)
        else:
            print("SyntaxError : Expected '[' , line: " + str(lines_number))
            sys.exit(1)
    elif tokens[1] == '[tk' :
        lex()
        (q1_true,q1_false) = condition()
        if tokens[1] == ']tk' :
            lex()
            return (q1_true, q1_false)
        else :
            print("SyntaxError : Expected ']' , line: " + str(lines_number))
            sys.exit(1)
    else: 
        expression_1 = expression()
        relop = relational_oper()
        expression_2 = expression()
        r_true = makeList(nextQuad())
        genQuad(relop, expression_1, expression_2, "_")
        r_false = makeList(nextQuad())
        genQuad("jump", "_", "_", "_")
        return (r_true,r_false)


def expression() :
    optional_sign()
    term1 = term()
    while tokens[1] == '+tk' or tokens[1] == '-tk' :
        temp_oper = tokens[0]
        add_oper()
        term2 = term()
        temp = newTemp()
        genQuad(temp_oper,term1,term2,temp)
        term1 = temp
    return term1


def term() :
    factor1 = factor()
    while tokens[1] == '*tk' or tokens[1] == '/tk' :
        temp_oper = tokens[1]
        temp = newTemp()
        mul_oper()
        factor2 = factor()
        genQuad(temp_oper,factor1,factor2,temp)
        factor1 = temp
    return factor1


def factor() :
    temp_exp = tokens[0]
    if tokens[1] == 'constant' :
        lex()
        
    elif tokens[1] == '(tk' :
        lex()
        temp_exp = expression()
        if tokens[1] == ')tk' :
            lex()
        else :
            print("SyntaxError : Expected ')' , line: " + str(lines_number))
            sys.exit(1)
    elif tokens[1] == 'idtk' :
        is_undeclared(tokens[0])
        token_ID = tokens[0]
        lex()
        idtail(token_ID) #Check again
    else :
        print("Tokens: ", tokens[0]," - ",tokens[1])
        print("SyntaxError : constant or variable/function missing , line " + str(lines_number))
        sys.exit(1)
    return temp_exp


def idtail(ID) :
    if tokens[1] == '(tk' :
        entity, nl = search_Entity(ID)
        actualpars(entity)
        temp = newTemp()
        genQuad("par",temp,"RET","_")
        genQuad("call", ID, "_", "_")
        genQuad(":=",temp,"_",ID)
        
        #return act


def relational_oper() :
    
    if tokens[1] == '=tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    elif tokens[1] == '<=tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    elif tokens[1] == '>=tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    elif tokens[1] == '>tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    elif tokens[1] == '<tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    elif tokens[1] == '<>tk' :
        temp_relop = tokens[0]
        lex()
        return temp_relop
    else :
        print("SyntaxError : Relational Operator Expected , line :" + str(lines_number))
        sys.exit(1)


def add_oper() :
    lex()


def mul_oper() :
    lex()


def optional_sign() :
    if tokens[1] == '+tk' or tokens[1] == "-tk" :
        #lex()
        add_oper()
        


# Main function
def main() :
            
    # Reading the first char
    lex()
        
    # Beggining of syntax analysis
    program()
    print("Syntax Analysis Completed!\n")
        
    # Creating int file
    createInt_File()
    print("Intermediate File Created!  --> " + str(filename[0]) + "_IntFile.int\n" )
        
    # Creating C File 
    createC_File()
    print("C file Created!  --> " + str(filename[0]) + "_CFile.c\n")

    print("Assembly File Created! --> " + str(filename[0]) + '_FinalCode.asm\n')
    print("Compilation Completed!")


# Calling main to start compilation
main()

#File Closing
output_final_file.close()

input_file.close()








    




