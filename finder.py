# program created by mohit
# email-id  mohitraj.cs@gmail.com
import os
import re
import sys
from threading import Thread
from datetime import datetime
import subprocess
import pickle
import argparse
from difflib import SequenceMatcher
from functools import reduce
from colorama import init,Fore, Back, Style
init(autoreset=True)
_a = (Fore.CYAN + '-----------------------------------------------------------------')
_d = (Fore.RED + '-->D')

dict1 = {}
i = 1
Anonymous=False

def folder_open(path):
    #import pdb;pdb.set_trace()
    print ("path ", path)
    path = path.rsplit("/", 1)[0]
    path_list = path.split("\\")
    # print path_list
    os.chdir(path_list[0][0:2])
    if path_list[0][2:]:
        os.chdir(path_list[0][2:])
    if len(path_list) > 1:
        for i in range(1, len(path_list) - 1):
            os.chdir(path_list[i])
        os.chdir(path_list[-1].split(":")[0])
    subprocess.Popen(r'explorer /select,"." ')

def file_read(file_name):
    pickle_file = open(file_name,"rb")
    values = pickle.load(pickle_file) 
    pickle_file.close()
    return values

def file_write(file_name,data):
    pickle_file = open(file_name,"wb")
    pickle.dump(data,pickle_file)
    pickle_file.close()

	
    

def save_search(path1):
    file_path= os.path.expanduser('~')
    os.chdir(file_path)
    size = 10
    file_name = "save.raj"
	
    f_ok = os.access(file_name, os.F_OK)
    if f_ok:
        data= file_read(file_name)
        if path1 not in data:
            if len(data)>size:
                data.pop()
            data.insert(0,path1)
            file_write(file_name,data)
            		
    else :
        list1 = [path1]
        file_write(file_name,list1)
    print ("search recorded\n")		
		
        
	
def file_run(path1):
    path= path1[2:]

    file_list = path.split("//")
    file_list1 = file_list[0].split("/")[0]

    file_to_open =file_list[0].split("/")[1]
    print ("file to open", file_to_open)
    file_list = file_list1.split("\\")
    os.chdir(path1[0:2]+'//')
    if file_list[0]:
        for each in file_list:
           os.chdir(each)
        #print "yes"
    file_to_open= file_to_open.strip()
    file_name = '"'+file_to_open +'"'

    os.startfile(file_name)
    print ("Anonymous ",Anonymous)
    if Anonymous== False:
        save_search(path1)

def show_search():
    file_path= os.path.expanduser('~')
    os.chdir(file_path)
    file_name = "save.raj"
    f_ok = os.access(file_name, os.F_OK)
    if f_ok:
        choice_list = file_read(file_name)
        print ("\n*******************************************")
        for index, item in enumerate(choice_list):
            print (index+1, " ", item)
            print ("---------------------------------------"*2)
        print ("\n*******************************************")
        num = input("Enter the number of the file you want to run or press n :\t")
        try:
            num = int(num)
            file_run(choice_list[num - 1])
        except:
            pass
   
	
    


class ratio_mohit(SequenceMatcher):
    def __init__(self, isjunk=None, a='', b='', autojunk=True):
        SequenceMatcher.__init__(self, isjunk=None, a='', b='', autojunk=True)
        self.isjunk = isjunk
        self.a = self.b = None
        self.autojunk = autojunk
        # self.a=a
        # self.b=b
        self.set_seqs(a, b)

    def ratio2(self):
        matches = reduce(lambda sum, triple: sum + triple[-1],
                         self.get_matching_blocks(), 0)

        return float(matches) / len(self.a)


        # ob1 = ratio_mohit(None, 'kotak', 'katak.txt')


# print ob1.ratio2()


def suggestion(file_dict, file_to_be_searched, level=0.8, index2=10):
    list2 = []
    len1 = len(file_to_be_searched)
    for key in file_dict:
        b = key.split("|")[0]
        a = file_to_be_searched
        try:
            s = ratio_mohit(None, a, b)
            # s = SequenceMatcher(None, a, b)
            # res=s.find_longest_match(0, len(a), 0, len(b))
            # len1 = tuple(res)[2]
            # len2 = len(b)
            # ratio1= float(len1)/len2
            # print a[tuple(res)[0]: tuple(res)[0]+len1]
            ratio_result = s.ratio2()

            if ratio_result >= level:
                str1 = file_dict[key] + "/" + b
                list2.append(str1)
                list2.sort(key=lambda s: len(s))
                # print str1
                # print "_"*30
        except Exception as e:
            print (e)
    index1 = 0
    for index, each in enumerate(list2):
        print (_a)
        if index1 > index2:

            ch = input("want to see more suggestion, Press  Y ")
            # print "Want to open the folder ?  "
            if ch.lower() == 'y':
                index1 = 0
            else:
                break
        if each.endswith(">"):
            print (index + 1, " ", each, _d)
        else:
            print (index + 1, " ", each)
        index1 = index1 + 1
    print  ("Want to open the folder ? ")
    try:
        num = int(input("Enter the number "))
        folder_open(list2[num - 1])
    except:
        pass


def get_drives():
    response = os.popen("wmic logicaldisk get caption")
    list1 = []
    total_file = []
    t1 = datetime.now()
    for line in response.readlines():
        line = line.strip("\n")
        line = line.strip("\r")
        line = line.strip(" ")
        if (line == "Caption" or line == ""):
            continue
        list1.append(line)
    return list1


def search1(drive):
    global i
    for root, dir, files in os.walk(drive, topdown=True):
        dir = [each+">" for each in dir]
        files.extend(dir)
        for file in files:
            file = file.lower()
            if file in dict1:

                file = file + "|" + str(i)
                dict1[file] = root
                i = i + 1
            else:
                dict1[file] = root


def create():
    t1 = datetime.now()
    list2 = []  # empty list is created
    list1 = get_drives()
    print ("Creating Index...")
    for each in list1:
        process1 = Thread(target=search1, args=(each,))
        process1.start()
        list2.append(process1)

    for t in list2:
        t.join()  # Terminate the threads

    pickle_file = open("mohit.raj", "wb")
    pickle.dump(dict1, pickle_file)
    pickle_file.close()
    t2 = datetime.now()
    total = t2 - t1
    print ("Time taken to create ", total)


def file_open():
    pickle_file = open("mohit.raj", "rb")
    file_dict = pickle.load(pickle_file)
    pickle_file.close()
    return file_dict

def exclude(list2, elist):
    list1 = list2[:]
    for each in list2:
        for e in elist:
                
            e = e.lower()
            if each.lower().startswith(e):
                #print ("each",each, list1.index(each))
                list1.remove(each)
    return list1

def file_search(file_name, drive=None,elist=None, folder_flag=None, file_flag=None):
    t1 = datetime.now()
    try:
        file_dict = file_open()
    except IOError:
        create()
        file_dict = file_open()
    except Exception as e:
        print (e)
        sys.exit()
    file_to_be_searched = file_name.lower()
    file_to_be_searched = r'{}'.format(file_to_be_searched)
    list1 = []
    print (Fore.YELLOW +Style.BRIGHT + "All File(s) :")
    for key in file_dict:
        if re.search(file_to_be_searched, key):
            str1 = file_dict[key] + "/" + key.split("|")[0]

            #else :
            #   str1 = file_dict[key]  + key.split("|")[0]

            list1.append(str1)
    t2 = datetime.now()
    list1.sort()
    if elist:
         list1 = exclude(list1,elist)
    if drive:
        drive = drive[0]
        print ("drive",drive)
        list1 = [each for each in list1 if each.startswith(drive)]

    if list1:
        if folder_flag:
            list1 =filter(lambda x: x.endswith(">"), list1)
        if file_flag:
            list1 =filter(lambda x: not x.endswith(">"), list1)
        for index, item in enumerate(list1):
            # print re.sub("?\d+", "", each)
            if item.endswith(">"):
                print (index + 1, " " , item.split("|")[0].rstrip(">"),_d)
            else :
                print (index + 1, " " , item.split("|")[0])
            print (_a)
        total = t2 - t1
        print ("Time taken to search ", total)
        d_f = input( "Press d to open folder or press f to open file or press enter for both ")
        d_f = d_f.lower()

        num = input("Enter the number ")
        num = int(num)
        if d_f == 'd':

            # print list1[num-1]
            folder_open(list1[num - 1])
        elif d_f=='f':
            file_run(list1[num - 1])

        else:
            folder_open(list1[num - 1])
            file_run(list1[num - 1])


    print ("Total files are", len(list1))

    if not list1:
        print ("No File is found")
        ch = input("Do you want suggestions ? \n Press Y ")
        if ch.lower() == 'y':
            ob1 = ratio_mohit(None, 'kotak', 'katak.txt')
            suggestion(file_dict, file_to_be_searched)


def main():
    parser = argparse.ArgumentParser()
    # parser.add_argument("file_name",help="For creating index databases", type= str)
    parser.add_argument("file_name", nargs='?')
    parser.add_argument('-l', help="To show the most recent searches", action='store_true')
    parser.add_argument('-c', help="For creating index databases", action='store_true')
    parser.add_argument('-a', nargs=1, help="If you don't want to save the save the search")
    # parser.add_argument('-w',help="New value", action='store_true')
    parser.add_argument('-s', nargs=3,help='Takes three arguments first file_name second percentage in numeric and third how many suggestions like abc 80 10')
    parser.add_argument('-d', nargs=2, help='Filter by drive,finder -d <file-name> drive_name')
    parser.add_argument('-e', nargs='+', help='To display the files except for mentioned files with the option')
    parser.add_argument('-v', help="Version Number", action='store_true')
    parser.add_argument('-f', help="Searches only Folders", action='store_true')
    parser.add_argument('-of', help="Only files not folders", action='store_true')
    args = parser.parse_args()

    try:

        if args.c:
            create()
        elif args.v:
            print ("Current Version --> 6.0")
        elif args.l:
            show_search()

        elif args.s:
            # print args.s
            file_dict = file_open()
            suggestion(file_dict, args.s[0], float(args.s[1]) / 100)

        elif args.d:
            file_search(args.d[0], args.d[1], args.e, args.f, args.of)
        elif args.a:
            file = args.a[0]
            if file != None and file != "":
                if file.isspace():
                    print ("Please give file name")
                else:
                    global Anonymous
                    Anonymous= True	
                    file_search(file)
        else:
            if args.file_name != None and args.file_name != "":
                if args.file_name.isspace():
                    print ("Please give file name")
                else:
                    file_search(args.file_name,elist=args.e , folder_flag=args.f, file_flag=args.of)
                
            else :
                print ("Please give file name \n")
        print (Back.CYAN + Style.BRIGHT +"Email id mohitraj.cs@gmail.com")


    except Exception as e:
        print (e)
        print (Back.RED + Style.BRIGHT +"Please use proper format to search a file use following instructions")
        print (Back.RED + "finder file-name")
        print (Back.RED + "Use <finder -h >  For help")


main()
