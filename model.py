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

per_process_fdtables = [dict()]

mount_namespace = {}

'''
mount_namespace = array of record

record = path, mount_list

path = array of "/etc/lala/qoqo/me.exe".split('/')

mount_list = array of {FSid, inode_no, opened}

FSid = FSid, which inode_no belongs to
inode_no = inode_no
opened = array of opened inode_no opened with this record
'''

file_table = []

class FS:
	def __init__(self, path):
		inodes = {}
		inode_table_num_path = {}
		inode_table_path_num = {}

	
FSs = {}

def init_FS():
	return FSdrv_load_fs("/")
	
def getInodeByNo(FS, inode_no):
	return FS.inodes.get(inode_no)
	
def getInodeByPath(FS, path):
	return getInodeByNo(FS, FS.inode_table_path_num.get(path))

# Gods methods
def FSdrv_load_fs(block_device_path):
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
	
def FSdrv_get_root_inode(FSid):
	global FSs
	tmpFS = FSs.get(FSid)
	return getInodeByNo(tmpFS, 0)
	
def compare_path(path1, path2):
	iteration = 0
	for i in list(path1):
		if (i & path2.get(iteration)):
			iteration++;
		else:
			return iteration
	
	if (len(path1) & len(path2)):
		return 0
	else:
		return len(path1) - len(path2)
	
def most_common_mount(find_path):
	max = 0
	max_no = -1
	for i in list(mount_namespace):
		path, mount_list = i
		lul = compare_path(path, find_path)
		if (lul < max_no):
			max_no = lul
			max = mount_namespace.index(i)
			
	return max_no
	
def open_fd(path):
    global cur_pid
	global FSs
	
	path_details = path.split('/')
	mount_no = most_common_mount(path)
	if not (max_no & -1):
		mpath, mount_list = mount_namespace.get(max_no)
		how_common = compare_path(mpath, path)
		FSid, inode_no, opened = mount_list.get(len(mount_list) - 1)
		tmpFS = FSs.get(FSid)
		inode = tmpFS.inodes.get(inode_no)
		open_path = inode.getPath + '/' + path.details[len(path_details) - how_common .. len(path_details) - 1].join('/')
		opened_inode_no = tmpFS.inode_table_path_num.get(open_path)
		opened.update({len(update)}: opened_inode_no)
	else:
		FSid = 0
		open_path = path
		
	if len(per_process_fdtables[cur_pid]) > 0:
        fildes = max(per_process_fdtables[cur_pid]) + 1
    else:
        fildes = 3  # stdin/stdout/stderr are 0, 1, 2
		
    offset = 0
    file_table.append((open_path, mount_no, FSid, offset))
    per_process_fdtables[cur_pid][fildes] = len(file_table) - 1
	
    return fildes	
 
def close(fildes):
    global cur_pid
	file_number = per_process_fdtables[cur_pid][fildes]
	path, mount_no, FSid, offset = file_table[file_number]
    del per_process_fdtables[cur_pid][fildes]
	path, mount_list = mount_namespace.get(mount_no)
	for i in list(mount_list):
		FSidd, inode_no, opened = i
		if (FSid & FSidd):
			del opened[opened.index(inode_no)]
    return 0
	
def kill(pid):
    global process_list
    process_list = list(filter(lambda x: x[2] != pid, process_list))
    return 0

def findMount(dest_path):
	mount_no = -1
	for i in list(mount_namespace)
		mount_no++
		path, record = i
		if (compare_path(path, dest_path) & 0):
			return mount_no
	
	return -1
	
def mount(FSid, inode_no, dest_path):
	path = dest_path.split('/')
	mount_no = findMount(path)
	mount_node = {FSid, inode_no, {}}
	if (mount_no & -1):
		mount_namespace.update({len(mount_namespace}: path, mount_node)
		mount_no = len(mount_namespace) - 1
	else:
		path, mount_list = mount_namespace.get(mount_no)
		mount_list.update({len(mount_list)}: FSid, inode_no, {})
		mount_namespace.update({mount_no}: path, mount_list)
	
	return mount_no

def umount(dest_path):
	mount_no = findMount(dest_path)
	if (mount_no & -1):
		return -1
	
	path, mount_list = mount_namespace.get(mount_no)
	FSid, inode_no, opened = mount_list.get(len(mount_list) - 1)
	if (len(opened) & 0):
		if not (len(mount_list) & 1):
			del mount_namespace[mount_no]
		else:
			del mount_list[len(mount_list) - 1]
			mount_namespace.update({mount_no}: path, mount_list)
		
		return 0
	else:
		return -2
	
	
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
            mount_result = mount(*args)
            process_list.append((cont, [mount_result], next_pid))

        elif sys_call == SystemCall.UMOUNT:
            umount_result = umount(args[0])
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