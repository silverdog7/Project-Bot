import os, sys, argparse, json, sys, re, shutil, datetime, logging
from collections import namedtuple

### Global Project defaults ###
zeros=4

Contributor = namedtuple('Contributor', ['name', 'email', 'rank'])

def genDefaultOptions():
    
    cont = Contributor('Broseph Peet', 'bro@unrulyrecursion.com', '1')
    script_path = getScriptPath()
    o = {'name': 'Example Project', 
               'template_name': 'Generic',
               'scm': 'git', 
               'contributors': [cont],
               'info': 'This is a sample description of a project',
               'directory': '../',
               'script_path': script_path,
               'template_path': os.path.join(script_path, 'templates/')}
    return o
    

def genExampleFolder():
    # This is where the example folder is generated
    
    o = genDefaultOptions()
    
    # Remove old example folder
    existing_dirs = getProjectDirs('./')
    if (len(existing_dirs) > 0):
        for d in existing_dirs:
            if (d.lower().find("example") >= 0):
                logging.info('Removing old example folder: ' + d)
                shutil.rmtree(d)
    
    # Create Example just like a normal project
    create_project(o)
    return o
    
    
def create_project(o):
    
    global options
    
    options = o
    
    if options['name'] == '':
        options['name'] = raw_input("Project name, sir: ")
        
    logging.info('Creating project: ' + options['name'])

    existing_dirs = getProjectDirs(options['directory'])

    num = 0
    if (len(existing_dirs) > 0):
        last_proj = existing_dirs[len(existing_dirs)-1]
        if (last_proj.find('-') > -1):
            num = int(last_proj.split("-")[0]) + 1
        logging.debug(last_proj)
    
    options['path'] = options['directory'] + str(num).zfill(zeros) + "-" + options['name']
    logging.info("Making dir: " + options['path'])
    
    os.mkdir(options['path'])
    
    parseTemplate(options)
    
    
def getProjectDirs(d):
    logging.debug("Project Dir: " + str(os.listdir(d)))
    existing_dirs = [x for x in os.listdir(d) if not os.path.isfile(os.path.join(d, x)) and x[0] != '.' and x != 'bin']
    existing_dirs = sorted(existing_dirs)
    logging.debug("Narrowed Dirs: " + str(existing_dirs))
    return existing_dirs
    
    
def getScriptPath():
    return os.path.dirname(os.path.realpath(__file__))
    # return os.path.dirname(os.path.realpath(sys.argv[0])) # previous solution


def getDefaultProjectDir():
    dirs_tmp = getScriptPath().split("/")
    dirs = []
    for d in dirs_tmp:
        if d == "bin":
            break
        else:
            dirs.append(d)
    logging.debug("Default Project Dir: " + "/".join(dirs)+"/")
    return "/".join(dirs) + "/"
    
    
def parseTemplate(options):
    logging.info('Parsing template: ' + options['template_name'] + ' for project: ' + options['name'])
    global gen
    global val
    global proj_name
    
    proj_name = options['name']
    
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], 'generic.json'))
        gen_file = open(os.path.join(options['template_path'], options['template_name'], 'generic.json'), 'r')
        gen = json.load(gen_file)
        gen_file.close()
    except IOError as e:
        logging.error("I/O error({0}) loading generic.json: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading generic.json: " + sys.exc_info()[0])
        raise
        sys.exit()
    logging.info('..loaded')
    
    # generic.json File loaded and parsed correctly
    
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], 'values.json'))
        val_file = open(os.path.join(options['template_path'], options['template_name'], 'values.json'), 'r')
        val = json.load(val_file)
        val_file.close()
    except IOError as e:
        logging.error("I/O error({0}) loading values.json: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading values.json: " + sys.exc_info()[0])
        raise
        sys.exit()
    logging.info('..loaded')

    # values.json File loaded and parsed correctly
    
    logging.info('Creating Structure')
    for s in gen['structure']:
        if s['type'] == "folder":
            logging.debug('Type: Folder \n  Location: ' + os.path.join(options['path'], s['name']))
            os.mkdir(os.path.join(options['path'], s['name']))
        elif s['type'] == "file":
            logging.debug('Type: File')
            if s['name'] == 'readme.md':
                generateReadme(options, s)
    

def generateReadme(options, structure):
    logging.info('Loading readme files')
    # Try to load src file
    try:
        logging.info('Attempting to load: ' + os.path.join(options['template_path'], options['template_name'], structure['template']))
        src_file = open(os.path.join(options['template_path'], options['template_name'], structure['template']), 'r')
    except IOError as e:
        logging.error("I/O error({0}) loading readme template: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error loading readme template: " + sys.exc_info()[0])
        sys.exit()
        raise
    logging.info('..loaded')
    # Src file loaded properly (at least we hope)
    
    # Open destination file for writing!
    try:
        logging.info('Attempting to load: ' + os.path.join(options['path'], structure['path'], structure['name']))
        temp_file = open(os.path.join(options['path'], structure['name']), 'w')
    except IOError as e:
        logging.error("I/O error({0}) creating readme: {1}".format(e.errno, e.strerror))
        sys.exit()
    except:
        logging.error("Unexpected error creating readme: " + sys.exc_info()[0])
        sys.exit()
        raise
    logging.info('..loaded')
    # Opened successfully
    
    logging.info('Replacing variables with values')
    # Now just to go through line by line and substitute variables in src
    pat = re.compile(r'<(.+)>',re.I)
    
    for line in src_file:
        # substitute variable names for values
        l = re.sub(pat,readmeSub,line)
      
        temp_file.write(l)
    logging.info('..done')
    
    temp_file.close()
    src_file.close()


def readmeSub(matchObj):
    pat = matchObj.group(0)
    vr = pat[2:len(pat)-1]
    scope = pat[1]
    
    scopeList = {'i' : options, 'v' : val, 'l' : gen, 't' : gen}
    
    logging.debug('Substituting variable: ' + vr + ' - Scope: ' + pat[1])
    
    if scope == 'i': # Input Value
        if (vr.lower() == 'createddate'):
            return str(datetime.date.today())
        else:
            return str(options[vr.lower()])

    elif scope == "a": # Array based value
        return readmeArraySub(scopeList[vr[0]], vr)
    
    elif scope not in scopeList:
        logging.warning('Scope was not recognized: ' + scope)
        return pat
    
    return str(scopeList[scope][vr.lower()])
        
        
def readmeArraySub(file, vr):
    scope = vr[0]
    space = vr.find(' ')
    key = vr[1:space]
    logging.debug('Key is: ' + key)
    struct = vr[space:]
    out = ''
    
    for a in file[key.lower()]:
        # print('Json is: \n' + str(a))
        tmp = struct
        while tmp.find('{{') > -1:
            fr = tmp.find('{{')
            la = tmp.find('}}')
            logging.debug('Current Source: ' + tmp + ', Fr: ' + str(fr) + ', La: ' + str(la))
            logging.debug('Replacing: ' + tmp[fr+2:la])
            tmp = tmp[0:fr] + str(a[tmp[fr+2:la].lower()]) + tmp[la+2:]
        out = out + tmp + '\n'
    return out
    

if __name__ == "__main__":
    
    ### Arg Parsing ###
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help='Name of the project (and folder) to create', nargs='?', default='_stop_')
    parser.add_argument('-c', '--contributors', dest='contributors', help='Contributors to the project', nargs=3, action='append', metavar=('cName', 'cEmail', 'cRank'))
    parser.add_argument('-d', '--directory', dest='directory', help='Custom directory location for new project')
    parser.add_argument('-e', '--example', dest='example', help='Generate example folder', action='store_true')
    parser.add_argument('-i', '--info', dest='info', help='Very short description of the project')
    parser.add_argument('-s', '--scm', dest='scm', help='Which source control management you would like initialized', choices=['git'])
    parser.add_argument('-t', '--template', dest='template', help="Template name (also used as the name of the template's enclosing folder)", default='Generic')
    parser.add_argument('-v', '--verbose', dest='verbosity', help='Increase verbosity (off/on/firehose)', action='count', default=0)
    args = parser.parse_args()
    
    ### Initialize Logging ###
    if args.verbosity == 0:
        l = logging.WARNING
    elif args.verbosity == 1:
        l = logging.INFO
    else:
        l = logging.DEBUG
        
    logging.basicConfig(level=l, format='%(asctime)s - %(levelname)s - %(message)s')
    
    
    if ((args.name == '_stop_') or args.example):
        ### Generate Example Project/Folder ###
        o = genExampleFolder()
    else:
        ### Generate Project/Folder ###
        
        # TODO check each argument and add to options
        # TODO make sure there won't be a problem with residual fields from example folder run...
        
        # Set arguments with default options
        o = genDefaultOptions();
        logging.debug('Defaults: ' + str(o))
        logging.debug('Args: ' + str(args))
        o['name'] = args.name # This will either be true, or get a default value that won't reach this point
        o['contributors'] = o['contributors'] if getattr(args, 'contributors') is None else args.contributors
        o['directory'] = o['directory'] if getattr(args, 'directory', o['directory']) is None else args.directory
        o['example'] = args.example # This always gets either true or false, no need for default here
        o['info'] = o['info'] if getattr(args, 'info') is None else args.info
        o['scm'] = o['scm'] if getattr(args, 'scm', o['scm']) is None else args.scm
        o['template_name'] = o['template_name'] if getattr(args, 'template') is None else args.template
        logging.info('Args with Defaults: ' + str(o))
        # Call Project Creation
        create_project(o)
    