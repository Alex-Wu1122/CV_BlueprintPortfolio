import sys
import os 
import re
dic={}
def get_fun(expr):
    fun_dic={}
    var=[]
    exp=[]
    re_exp=[]
    open=0
    f=0
    c=0
    #print(expr)
    for value in expr:
        if value in [" "]:
            continue
        elif "fun" in value:
            str_left=""
            for left in value[1:len(value)-1]:
                if open==1:
                    if left in [' ']:
                        var.append(str_left)
                        str_left=""
                        continue
                    elif left==')':
                        open+=1
                        var.append(str_left)
                    else:
                        #var.append(left)
                        str_left+=left
                    
                elif open==0:
                    if left in [' ']:
                        continue
                    elif left =='(':
                        open+=1
                    elif left == '+':
                        print('hi')

                elif open==2:

                    re_exp.append(left)
                    
        else:
            if value in ["#t",'#f']:
                fun_dic[var[c]]=value
                c+=1

            else:
                try:
                    int(value)
                    #fun_dic[var[c]]=int(value)
                    fun_dic[var[c]]=value
                    c+=1
                except:
                    print("fun_error")
                    return "error"
    #print(re_exp)
    re_exp = re.split(r"(\W)","".join(re_exp))
    #print(re_exp)
    if len(fun_dic)!=0:
        for idx,value in enumerate(re_exp):
            if value in fun_dic.keys():
                re_exp[idx]=fun_dic.get(value)
    strr="".join(re_exp)
    #print(strr)
    re_exp = re.split(r"(\W)",strr)
    for index,i in enumerate(re_exp):
        if i == '' :
            re_exp.pop(index)  
    #print(fun_dic)
#處理布林
    for index,i in enumerate(re_exp):
        if i == '#':
            if re_exp[index+1]=='t':
                re_exp.insert(index,"#t")
                re_exp.pop(index+1)
                re_exp.pop(index+1)
            elif re_exp[index+1]=='f':
                re_exp.insert(index,"#f")
                re_exp.pop(index+1)
                re_exp.pop(index+1)
    #print(re_exp)
    while "(" in re_exp:
            
            count = 0
            for idx,value in enumerate(re_exp):
                if value == ')':
                    count = idx
                    for i in range(count,-1,-1):
                        if re_exp[i]=='(' :
                            new_expr = re_exp[i+1:count]
                            #print(new_expr)
                            get_answer=compute(new_expr)
                            if (get_answer=="error"): return "error"
                            re_exp.insert(i,str(get_answer))
                            for j in range(count-i+1):
                                re_exp.pop(i+1)
                            break  
                    break
    while ' ' in re_exp:
        for index,i in enumerate(re_exp):
            if i == ' ':
                re_exp.pop(index)           
    #print(fun_dic)
    #print(re_exp)
    #print(var)
    return re_exp[0]
                    
                
            
def get_defination(expr):
    global dic
    flag = 0
    var=""
    exp=""
    hi=0
    hi2=0
    head=0
    for h in range(len(expr)):
        if expr[h]!=" ":
            head=h
            break
    for value in expr[head+1:]:
        if value in [" "]:
            continue
        else:
            if (flag==0):
                var=value
            else:
                exp=value
            flag+=1
    """
    for value in expr[1:]:
        if value in [" "]:
            if (hi==1):
                flag=1
                hi+=1
            elif (hi2==1):
                flag=2
            continue
        else:
            if (flag==0):

                var+=value
                print(var)
                hi=1
            elif (flag==1):
                exp+=value
                hi2=1
            else:
                flag+=1
                hi2+=1
"""

    if (flag==2):
        dic[var]=exp
    else:
        print("Need 2 arguments, but got ",flag,".")
    #print (dic)

def compute(expr):
    answer=0
    head=0
    for h in range(len(expr)):
        if expr[h]!=" ":
            head=h
            break

    if (expr[head]=="+"):
        flag=0
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    flag+=1
                    answer+=int(value)
                except:
                    if value in ['#t','#f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag>=2):
            return answer
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
        
    elif (expr[head]=="*"):
        answer=1
        flag=0
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    flag+=1
                    answer*=int(value)
                except:
                    if value in ['#t','#f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag>=2):
            return answer
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='-'):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:    
                    if (flag==0):
                        answer=int(value)
                    else:
                        answer-=int(value)
                    flag+=1
                except:
                    if value in ['#t','#f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==2):
            return answer
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='/'):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    if (flag==0):
                        answer=int(value)
                    else:
                        answer//=int(value)
                    flag+=1
                except:
                    if value in ['#t','#f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==2):
            return answer
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='mod'):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    if (flag==0):
                        answer=int(value)
                    else:
                        answer%=int(value)
                    flag+=1
                except:
                    if value in ['#t','f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==2):
            return answer
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='>'):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    if (flag==0):
                        answer=int(value)
                    else:
                        if (answer>int(value)) : r=True
                        else: r=False
                    flag+=1
                except:
                    if value in ['#t','f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==2):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='<'):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    if (flag==0):
                        answer=int(value)
                    else:
                        if (answer<int(value)) :r=True
                        else: r=False
                    flag+=1
                except:
                    if value in ['#t','f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==2):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='='):
        flag = 0;
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                try:
                    if (flag==0):
                        answer=int(value)
                    else:
                        if (answer==int(value)) :r=True
                        else: r=False
                    flag+=1
                except:
                    if value in ['#t','f']:
                        print("Type Error: Expect 'number' but got 'boolean'")
                    else: print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag>=2):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need 2 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='and'):
        flag =0
        r=True
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                if value=="#f":
                    r= False
                    flag+=1
                elif value=='#t':
                    flag+=1
                else:
                    try:
                        int(value)
                        print("Type Error: Expect 'boolean' but got 'number'")
                    except:
                        print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag>=2):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need more than 1 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='or'):
        flag = 0
        r=False
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                if value=="#t":
                    r=True
                    flag+=1
                elif value=="#f":
                    flag+=1
                else:
                    try:
                        int(value)
                        print("Type Error: Expect 'boolean' but got 'number'")
                    except:
                        print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag>=2):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need more than 1 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='not'):
        flag=0
        
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                if value=="#t":
                    flag+=1
                    r=False
                elif value=='#f':
                    flag+=1
                    r=True
                else :
                    try:
                        int(value)
                        print("Type Error: Expect 'boolean' but got 'number'")
                    except:
                        print("syntax error, unexpected ","'",value,"'")
                    return "error"
        if (flag==1):
            if r : return "#t" 
            else: return "#f"
        else:
            print("Need 1 arguments, but got ",flag,".")
            return "error"
    elif (expr[head]=='if'):
        get_test=0
        flag=0
        ga=0
        get_then=0
        get_els=0
        for value in expr[head+1:]:
            if value in [" "]:
                continue
            else:
                
                if value in ['#t','#f'] and get_test==0:
                    get_test=1
                    if value=='#t':r=True
                    else :r=False
                    flag+=1
                elif value not in ['#t','#f'] and get_test==0:
                    try:
                        int(value)
                        print("Type Error: Expect 'boolean' but got 'number'")
                    except:
                        print("syntax error, unexpected ","'",value,"'")
                    return "error"


                elif (get_test==1 and get_then==0):
                    get_then=1
                    if value in ['#t','#f']:
                        then=value
                    else:
                        try:
                            then=int(value)
                        except:
                            print("syntax error, unexpected ","'",value,"'")
                            return "error"
                    flag+=1
                elif (get_test==1 and get_then==1 and get_els==0):
                    get_els=1
                    if value in ['#t','#f']:
                        els=value
                    else:
                        try:
                            els=int(value)
                        except:
                            print("syntax error, unexpected ","'",value,"'")
                            return "error"
                    flag+=1
                elif (get_test==1 and get_then==1 and get_els==1):
                    flag+=1
                else:
                    ga=1
        if (flag==3):
            if r:return then
            else:return els
        elif (flag==0):
            if ga==0:
                print("Need 3 arguments, but got ",flag,".")
                return "error"
            else :
                print("Didn't get TEST-EXP")
                return "error"
        elif (flag>0 and flag <3):
            print("Need 3 arguments, but got ",flag,".")
            return "error"
        elif (flag>3):
            print("Need 3 arguments, but got ",flag,".")
            return "error"
    else:
        
        for value in expr[head]:
            if value in [" "]:
                continue
            elif value in ["#t","#f"]:
                return value
            else:
                try:

                    int(value)
                    return value
                except:
                    print("syntax error, unexpected ","'",value,"'")
                    return "error"
        

                    





def find_parse(input_list):
    global dic
    while "(" in input_list:
        if ")" not in input_list: 
            print("lack of right")
            return
        count = 0
        if len(dic)!=0:
            for idx,value in enumerate(input_list):
                if value in dic.keys():
                    input_list[idx]=dic.get(value)
            #print(input_list)
        for idx,value in enumerate(input_list):
            if value == ')':
                count = idx
                for i in range(count,-1,-1):
                    if input_list[i]=='(' :
                        expr = input_list[i+1:count]
                        #print(expr)
                        head=0
                        for h in range(len(expr)):
                            if expr[h]!=" ":
                                head=h
                                break
                        expr = expr[head:]
                        #print(expr)
                        #print(expr)
                        #print("".join(input_list[i+1:i+10]))
                        count_pri=0
                        
                        if ("print" in expr and "num" in expr):
                            for k in expr:
                                try:
                                    pri_num=int(k)
                                    count_pri+=1
                                except:
                                    if k in [" ","print","-","num"]:continue
                                    elif k in ['#f','#t']:
                                        print("Type Error: Expect 'number' but got 'boolean'")
                                        break

                                    else:     
                                        print("syntax error, unexpected ","'",k,"'")
                                        break
                            if (count_pri==1):print(pri_num)
                            elif (count_pri>1):
                                print("Need 1 arguments, but got ",count_pri,".")
                            for j in range(count-i+1):
                                input_list.pop(i)
                            break
                        elif ("print" in expr and "bool" in expr):
                            for k in expr:
                                if k in [" ","print","-","bool"]: continue
                                elif k in ["#t","#f"]:
                                    count_pri+=1
                                    pri_bool=k

                                else:
                                    try:
                                        int(k)
                                        print("Type Error: Expect 'boolean' but got 'number'")
                                        break
                                    except:
                                        print("syntax error, unexpected ","'",k,"'")
                                        break
                            if (count_pri==1):print(pri_bool)
                            elif (count_pri>1):
                                print("Need 1 arguments, but got ",count_pri,".")
                            for j in range(count-i+1):
                                input_list.pop(i)
                            break
                        elif ("fun" in expr[0]):
                            get_answer=get_fun(expr)
                            if (get_answer=="error"): return
                            input_list.insert(i,get_answer)
                            for j in range(count-i+1):
                                input_list.pop(i+1)
                            break
                        #"".join(input_list[i+1])=="define"
                        
                        elif ("define" in expr):
                            get_defination(expr)
                            for j in range(count-i+1):
                                input_list.pop(i)
                            break

                            
                        else:  
                            #print(count)
                            #print(expr)
                            get_answer=compute(expr)
                            if (get_answer=="error"): return
                        input_list.insert(i,str(get_answer))
                        for j in range(count-i+1):
                            input_list.pop(i+1)
                        break  
                break
    while ' ' in input_list:
        for index,i in enumerate(input_list):
            if i == ' ':
                input_list.pop(index)
    if (len(input_list)==1):
        print(input_list[0])
    return 
if (len(sys.argv)==1):
    words=input("請輸入:")
else:
    f = open(sys.argv[1])
    words = f.read()
#for line in f.readlines():
#    line=line.strip('\n')
#print(type(words))
re_words = re.split(r"(\W)",words)
words = words.replace('\n','')
words = words.replace('\t',' ')
re_words = re.split(r"(\W)",words)
for index,i in enumerate(re_words):
    if i == '' :
        re_words.pop(index)  


#處理布林
for index,i in enumerate(re_words):
    if i == '#':
        if re_words[index+1]=='t':
            re_words.insert(index,"#t")
            re_words.pop(index+1)
            re_words.pop(index+1)
        elif re_words[index+1]=='f':
            re_words.insert(index,"#f")
            re_words.pop(index+1)
            re_words.pop(index+1)
#(+-號直接與後面的字串結合)
for index,i in enumerate(re_words):
    if i in ['+','-'] and re_words[index+1]!=" ":
        try:
            int(re_words[index+1])
            re_words.insert(index,i+re_words[index+1])
            re_words.pop(index+1)
            re_words.pop(index+1)
        except:
            pass

while "fun" in re_words:
    count_left=0
    pos_fun=0
    pos_fun_left=0
    pos_fun_right=0
    for index,i in enumerate(re_words):
        if i=='fun':
            pos_fun=index
            #print(pos_fun)
            for pos in range(pos_fun,-1,-1):
                if re_words[pos]=='(':
                    pos_fun_left=pos
                    break
            break
    re_=re_words[pos_fun_left:]
    for index,i in enumerate(re_):
        if i =='(':
            count_left+=1
        elif i == ')':
            if count_left==1:
                pos_fun_right=pos_fun_left+index
                break
            else:
                count_left-=1
    #print(pos_fun_left)
    #print(pos_fun_right)
    str_fun="".join(re_words[pos_fun_left:pos_fun_right+1])
    re_words.insert(pos_fun_left,str_fun)
    for j in range(pos_fun_right-pos_fun_left+1):
        re_words.pop(pos_fun_left+1)
pos_def=[]
len_def=[]
str_def=[]
flag=0
for index,i in enumerate(re_words):
    if i=='define':
        flag=1
        count_left=0
        pos_left=0
        pos_right=0
        first=0
        str_=""

    elif flag==1:
        if i ==" ":
            if first==1:
                pos_right=index-1
                flag=0
                pos_def.append(pos_left)
                len_def.append(pos_right-pos_left+1)
                str_def.append(str_)
            continue
        else:
            if flag == 1 and first==0:
                pos_left=index
                first=1
                str_+=i
            elif flag==1 and first==1:
                str_+=i 
#print(re_words)
for k in range(len(pos_def)):     
    re_words.insert(pos_def[k],str_def[k])
    for j in range(len_def[k]):
        re_words.pop(pos_def[k]+1)
#print(re_words)
for index_f,f in enumerate(str_def):
    pos_def=[]
    len_def=[]
    str_ddd=[]
    flag=0
    #print(f)
    for index_i,i in enumerate(re_words):
        c=0
        pos_def_left=0
        pos_def_right=0
        len_str=0
        for index_j,j in enumerate(re_words[index_i:]):
            if j in f:
                #print("hi")
                #print(j)
                len_str+=len(j)
                c+=1  
                if c == 1:
                    pos_def_left=index_j+index_i
            if c>0:
                if j not in f and j in ["(",")"," "]:
                    pos_def_right=index_j+index_i
                    #print("me")
                    break
                elif j not in f and j!=" ":
                    c=0   
                    #print("you")
                    break
        if len_str==len(f) and c!=0:
            len_def.append(pos_def_right-pos_def_left)
            pos_def.append(pos_def_left)
            str_ddd.append(f)
    #print(len_def)
    #print(pos_def)
    #print(str_ddd)
    #print(len(len_def))
    #print(len(pos_def))
    #print(len(str_ddd))
    #print(re_words)

    for i in range(len(len_def)): 
        if (re_words[pos_def[i]]==str_ddd[i]):continue
        re_words.insert(pos_def[i],str_ddd[i])
        for j in range(len_def[i]):
            re_words.pop(pos_def[i]+1)
        #print("hi")
    #print(len(re_words))

#print(re_words)
find_parse(re_words)





"""



test=input("please input(加油):")
test=test.strip()
re_test = re.split(r"(\W)",test)
#print(re_test)

for index,i in enumerate(re_test):
    if i == '':
        re_test.pop(index)

#處理布林
for index,i in enumerate(re_test):
    if i == '#':
        if re_test[index+1]=='t':
            re_test.insert(index,"#t")
            re_test.pop(index+1)
            re_test.pop(index+1)
        elif re_test[index+1]=='f':
            re_test.insert(index,"#f")
            re_test.pop(index+1)
            re_test.pop(index+1)
#(+-號直接與後面的字串結合)
for index,i in enumerate(re_test):
    if i in ['+','-'] and re_test[index+1]!=" ":
        try:
            int(re_test[index+1])
            re_test.insert(index,i+re_test[index+1])
            re_test.pop(index+1)
            re_test.pop(index+1)
        except:
            pass
#print(re_test)
count_left=0
pos_fun=0
pos_fun_left=0
pos_fun_right=0
while "fun" in re_test:
    for index,i in enumerate(re_test):
        if i=='fun':
            pos_fun=index
            #print(pos_fun)
            for pos in range(pos_fun,-1,-1):
                if re_test[pos]=='(':
                    pos_fun_left=pos
                    break
            break
    re_=re_test[pos_fun_left:]
    for index,i in enumerate(re_):
        if i =='(':
            count_left+=1
        elif i == ')':
            if count_left==1:
                pos_fun_right=pos_fun_left+index
                break
            else:
                count_left-=1
    #print(pos_fun_left)
    #print(pos_fun_right)
    str_fun="".join(re_test[pos_fun_left:pos_fun_right+1])
    re_test.insert(pos_fun_left,str_fun)
    for j in range(pos_fun_right-pos_fun_left+1):
        re_test.pop(pos_fun_left+1)
        
    break
    
print(re_test)
find_parse(re_test)

print(dic)
"""