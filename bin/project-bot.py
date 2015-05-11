import os, sys, argparse, json, sys

### Global Project defaults ###
project_dir = "../"
project_name = ''
project_path = ''
zeros=4
template_dir = ""

### Arg Parsing ###

parser = argparse.ArgumentParser()
parser.add_argument("name", help="Name of the project (and folder) to create")
args = parser.parse_args()
print args.name





# def main(argv):
#     in_project_name = ''
#     in_dir_name = ''

#     """ Help Text """
#     help = 'project-bot.py -p "Project Name"'

#     try:
#         opts, args = getopt.getopt(argv, "hp:d:", ["project=","directory="])
#     except getopt.GetoptError:
#         print help
#         sys.exit(2)
#     for opt, arg in opts:
#         if opt == '-h':
#             print help
#             sys.exit()
#         elif opt in ("-p", "--project"):
#             in_project_name = arg
#             print(in_project_name)
#         elif opt in ("-d", "--directory"):
#             in_dir_name = arg
#             print(in_dir_name)
#     if in_project_name != '':
#         global project_name 
#         project_name = in_project_name

# if __name__ == "__main__":
#     main(sys.argv[1])
    
   
def create_project():

    global project_name
    if project_name == '':
        project_name = raw_input("Project name, sir: ")

    project_dir = getDefaultProjectDir()
    print("Project Dir: " + str(os.listdir(project_dir)))
    
    existing_dirs = [x for x in os.listdir(project_dir) if not os.path.isfile(os.path.join(project_dir,x)) and x[0] != '.' and x != "bin"]
    existing_dirs = sorted(existing_dirs)
    print("Narrowed Dirs: "+ str(existing_dirs))
    
    if len(existing_dirs) == 0:
        num = 0
    else:
        last_proj = existing_dirs[len(existing_dirs)-1]
        num = int(last_proj.split("-")[0]) + 1
        
    # print(last_proj)
    
    new_path = project_dir + str(num).zfill(zeros) + "-" + project_name
    print("Making dir: " + new_path)
    project_path = new_path
    os.mkdir(new_path)
    
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def getDefaultProjectDir():
    dirs_tmp = getScriptPath().split("/")
    dirs = []
    for d in dirs_tmp:
        if d == "bin":
            break
        else:
            dirs.append(d)
    print("Default Project Dir: " + "/".join(dirs)+"/")
    return "/".join(dirs) + "/"
    
def genExampleFolder():
    # This is where the example folder will be generated
    
    ### Set global options and what not
    
    create_project()
    
def parseTemplate(template_path):
    try:
        gen_file = open(template_path + 'generic.json', 'r')
        gen = json.load(gen_file)
        gen_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise
        sys.exit()

    # generic.json File loaded and parsed correctly
    
    try:
        val_file = open(template_path + 'values.json', 'r')
        val = json.load(gen_file)
        val_file.close()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    # values.json File loaded and parsed correctly
    
    # can sort by folders on top?
    for s in gen['structure']:
        if s['type'] == "folder":
            os.mkdir(project_dir + s['path'])
        elif s['type'] == "file":
            if s['name'] == 'readme.md':
                generateReadme(template_path + s['template'])
    

def generateReadme(file_template_path):
    
    # Try to load src file
    try:
        src_file = open(file_template_path, 'r')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
        raise
    # Src file loaded properly (at least we hope)
    
    
    # Open destination file for writing!
    try:
        temp_file = open(project_path + 'readme.md', 'w')
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit()
    except:
        print "Unexpected error:", sys.exc_info()[0]
        sys.exit()
        raise
    # Opened successfully
    
    # Now just to go through line by line and substitute variables in src
    
    for line in src_file:
      
      l=""
      
      #perform operation and substitution on line into l
      
      temp_file.write(l)# + "\n") # TODO uncomment if no new lines in output
    
    temp_file.close()
    src_file.close()


""" Actual Execution """
# create_project()