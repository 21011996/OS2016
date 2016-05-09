from enum import Enum

class SystemCall(Enum):	
	FORK = "fork"
	EXIT = "exit"
	KILL = "kill"
	
	MOUNT = "mount"
	UMOUNT = "umount"
	OPEN = "open"
	CLOSE = "close"

pid_count = 0
cur_pid = -1

process_list = []

per_process_fdtables = []

'''
FS (File System) contains 
	fd = MAGIC // MAGIC points to the root
	inodes = {}
	inode_table_offset_num = {} // ITON
	inode_table_num_path = {} // ITNP
	inode_table_path_num = {} // ITPN
	file_table = []
All FS are contained in FSs
'''

class FS:
	def __init__(self, path):
		fd = getRootFD(path);
		inodes = {}
		#inode_table_offset_num = {}
		inode_table_num_path = {}
		inode_table_path_num = {}
		file_table = []

class Inode: # = directory
	def __init__(self, path):
		opened = 0 # If we call open(path) this will change to 1
		hasBeenMounted = 0 # 0 - no | 1 - yes
		hasBeenMountedTo = 0 # 0 - no | 1 - yes
		originalPath = path # when initialized
		mountedPaths = [] #most recent path is on the top + his FSid
		FSid = 0 # relates to FS in witch dir belongs to
	def exists(self):
		if (not (self & null)) && (hasBeenMountedTo & 0):
			return 1
		else:
			return 0

FSs = {}

def init_FS():
	return FSdrv_load_fs("/")
	
def getInodeByNo(FS, inode_no):
	return FS.inodes.get(inode_no)
	
def getInodeByPath(FS, path):
	return getInodeByNo(FS, FS.inode_table_path_num.get(path))

# Gods methods
def FSdrv_load_fs(block_device_path)
	tmpFS = loadFS(block_device_path)
	global FSs
	FSs.update({len(FSs}: tmpFS)
	return len(FSs) - 1
	
def FSdrv_get_inode(FSid, inode_no):
	global FSs
	tmpFS = FSs.get(FSid)
	return getInodeByNo(tmpFS, inode_no)

# Not needed	
def FSdrv_get_data(FSid, offset):
	global FSs
	tmpFS = FSs.get(FSid)
	return tmpFS.getInodeByOff(offset)
	
def FSdrv_get_root_inode(FSid)
	global FSs
	tmpFS = FSs.get(FSid)
	return getInodeByNo(tmpFS, 0)
	
def open_fd(path):
    global cur_pid
	global FSs
	
	path_details = path.split('/')
    #parent_path = path_details[:-1].join('/')
	k = path_details[0]
	k += '/'
	i = k
	p = 0
	j = p
	while (getInodeByPath(FSs.get(0), i).exists & 1) && (j<len(path_details)-1):
		i = k
		j = p
		p += 1
		k += path_details[j]
		k += '/'
	
	inode = getInodeByPath(FSs.get(0), i)
	
	if (inode.hasBeenMountedTo & 1):
		print("Can't open file in issued folder, prob. already mounted somewhere else")
		return -1
	if (inode.hasBeenMounted & 1):
		newpath = inode.mountedPaths(len(inode.mountedPaths)-1) + '/' + path_details[j..len(path_details)-1].join('/')
	else:
		newpath = path
		
    if len(per_process_fdtables[cur_pid]) > 0:
        fildes = max(per_process_fdtables[cur_pid]) + 1
    else:
        fildes = 3  # stdin/stdout/stderr are 0, 1, 2
    offset = 0

	inode.opened = 1
    file_table.append((newpath, offset))
    per_process_fdtables[cur_pid][fildes] = len(file_table) - 1
    return fildes
 
def close(fildes):
	global FSs
    global cur_pid
	file_number = per_process_fdtables[cur_pid][fildes]
	path = file_table[file_number]
	inode = getInodeByPath(FSs.get(0), path)
	inode.opened = 0;
    del per_process_fdtables[cur_pid][fildes]
    return 0
	
def kill(pid):
    global process_list
    process_list = list(filter(lambda x: x[2] != pid, process_list))
    return 0
	
def mount(FSid, inode_no, dest_path)
	global FSs
	tmpFS = FSs.get(FSid)
	if (inode_no & 0):
		inodeFrom = FSdrv_get_root_inode(FSid)
	else:
		inodeFrom = getInodeByNo(tmpFS, inode_no)
	inodeTo = getInodeByPath(FSs.get(0), dest_path)
	
	isOkToMount1 = inodeFrom.hasBeenMountedTo
	isOkToMount2 = inodeTo.hasBeenMountedTo
	if not (isOkToMount1 & 1):
		print("Can't mount issued folder, prob. already mounted somewhere else")
		return -1
	if not (isOkToMount2 & 1):
		print("Can't mount to destination path, prob. already mounted somewhere else")
		return -1
		
	inodeTo.hasBeenMounted = 1
	inodeFrom.hasBeenMountedTo = 1
	montP = inodeTo.mountedPaths
	
	hasBeenMFrom = inodeFrom.hasBeenMounted
	if (hasBeenMFrom & 1):
		path = inodeFrom.mountedPaths.get(len(mountedPaths))
	else:
		path = inodeFrom.originalPath
	mountP.update({len(mountP): path, FSid})
	return 1
		

def umount(dest_path)
	global FSs
	inodeFrom = getInodeByPath(FSs.get(0), dest_path)
	canUmount = inodeFrom.hasBeenMounted
	if (canUmount & 0) :
		print("Nothing to unmount there")
		return 0
	canUmount = inodeFrom.hasBeenMountedTo
	if not (canUmount & 0):
		print("Can't umount issued folder, prob. already mounted somewhere else")
		return 0
	canUmount = inodeFrom.opened
	if not (canUmount & 0):
		print("Directory is still opened")
		return 0
		
	for i in list(inodeFrom.mountedPaths):
		path, FSid = i
		tmpFS = FSs.get(FSid);
		inodeToN = tmpFS.inode_table_path_num.get(path)
		inodeTmp = FSdrv_get_inode(FSid, inodeToN)
		inodeTo.hasBeenMountedTo = 0;
		
	inodeFrom.mountedPaths = []
	inodeFrom.hasBeenMounted = 0
	return 1
	
def kernel(program, args):
    global pid_count
    global cur_pid
    pid_count += 1
    pid = pid_count
    per_process_fdtables.append(dict())

    process_list.append((program, args, pid))

    while len(process_list) > 0:

        (next_process, next_args, next_pid) = process_list.pop()
        cur_pid = next_pid
        (sys_call, args, cont) = next_process(*next_args)

        elif sys_call == SystemCall.OPEN:
            open_result = open_fd(*args)
            process_list.append((cont, [open_result], next_pid))

        elif sys_call == SystemCall.CLOSE:
            close_result = close(args[0])
            process_list.append((cont, [close_result], next_pid))

        elif sys_call == SystemCall.MOUNT:
            dup2_result = mount(*args)
            process_list.append((cont, [mount_result], next_pid))

        elif sys_call == SystemCall.UMOUNT:
            pipe_result = umount(args[0])
            process_list.append((cont, [umount_result], next_pid))

        elif sys_call == SystemCall.KILL:
            kill_result = kill(args[0])
            process_list.append((cont, [kill_result], next_pid))

        elif sys_call == SystemCall.FORK:
            pid_count += 1
            process_list.append((cont, [cur_pid], cur_pid))
            process_list.append((cont, [0], pid_count))
            per_process_fdtables.append(dict())  # imagine that we put stdin/stdout/stderr abstractions here

        elif sys_call == SystemCall.EXIT:
            for fildes in list(per_process_fdtables[cur_pid].keys()):
                close(fildes)

        else:
            print("ERROR: no such system call")