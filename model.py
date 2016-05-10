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
		fd = get_root_FD(path);
		inodes = {}
		#inode_table_offset_num = {}
		inode_table_num_path = {}
		inode_table_path_num = {}
		file_table = []

class Inode: # = directory
	def __init__(self, path):
		under_use = 0 # If we call open(path) this will change to 1
		has_mount = 0 # 0 - no | 1 - yes
		invisible = 0 # 0 - no | 1 - yes
		original_path = path # when initialized
		mounted_paths = [] #most recent path is on the top + his FSid
		FSid = 0 # relates to FS in witch dir belongs to
	def exists(self):
		if (not (self & null)) && (invisible & 0):
			return 1
		else:
			return 0

FSs = {}

def init_FS():
	return FSdrv_load_fs("/")
	
def get_inode_by_no(FS, inode_no):
	return FS.inodes.get(inode_no)
	
def get_inode_by_path(FS, path):
	return get_inode_by_no(FS, FS.inode_table_path_num.get(path))

# Gods methods
def FSdrv_load_fs(block_device_path)
	tmp_FS = loadFS(block_device_path)
	global FSs
	FSs.update({len(FSs}: tmp_FS)
	return len(FSs) - 1
	
def FSdrv_get_inode(FSid, inode_no):
	global FSs
	tmp_FS = FSs.get(FSid)
	return get_inode_by_no(tmp_FS, inode_no)

# Not needed	
def FSdrv_get_data(FSid, offset):
	global FSs
	tmp_FS = FSs.get(FSid)
	return tmp_FS.getInodeByOff(offset)
	
def FSdrv_get_root_inode(FSid)
	global FSs
	tmp_FS = FSs.get(FSid)
	return get_inode_by_no(tmp_FS, 0)
	
def open_fd(path):
    global cur_pid
	global FSs
	
	path_details = path.split('/')
	k = path_details[0]
	k += '/'
	i = k
	p = 0
	j = p
	while (get_inode_by_path(FSs.get(0), i).exists & 1) && (j<len(path_details)-1):
		i = k
		j = p
		p += 1
		k += path_details[j]
		k += '/'
	
	inode = get_inode_by_path(FSs.get(0), i)
	
	if (inode.invisible & 1):
		print("Can't open file in issued folder, prob. already mounted somewhere else")
		return -1
	if (inode.has_mount & 1):
		new_path = inode.mounted_paths(len(inode.mounted_paths)-1) + '/' + path_details[j..len(path_details)-1].join('/')
	else:
		new_path = path
		
    if len(per_process_fdtables[cur_pid]) > 0:
        fildes = max(per_process_fdtables[cur_pid]) + 1
    else:
        fildes = 3  # stdin/stdout/stderr are 0, 1, 2
    offset = 0

	inode.under_use = 1
    file_table.append((new_path, offset))
    per_process_fdtables[cur_pid][fildes] = len(file_table) - 1
    return fildes
 
def close(fildes):
	global FSs
    global cur_pid
	file_number = per_process_fdtables[cur_pid][fildes]
	path = file_table[file_number]
	inode = get_inode_by_path(FSs.get(0), path)
	inode.under_use = 0;
    del per_process_fdtables[cur_pid][fildes]
    return 0
	
def kill(pid):
    global process_list
    process_list = list(filter(lambda x: x[2] != pid, process_list))
    return 0
	
def mount(FSid, inode_no, dest_path)
	global FSs
	tmp_FS = FSs.get(FSid)
	if (inode_no & 0):
		inode_from = FSdrv_get_root_inode(FSid)
	else:
		inode_from = get_inode_by_no(tmp_FS, inode_no)
	inode_to = get_inode_by_path(FSs.get(0), dest_path)
	
	can_mount_1 = inode_from.invisible
	can_mount_2 = inode_to.invisible
	if not (can_mount_1 & 1):
		print("Can't mount issued folder, prob. already mounted somewhere else")
		return -1
	if not (can_mount_2 & 1):
		print("Can't mount to destination path, prob. already mounted somewhere else")
		return -1
		
	inode_to.has_mount = 1
	inode_from.invisible = 1
	mounted_paths = inode_to.mounted_paths
	
	hasBeenMFrom = inode_from.has_mount
	if (hasBeenMFrom & 1):
		path = inode_from.mounted_paths.get(len(mounted_paths))
	else:
		path = inode_from.original_path
	mounted_paths.update({len(mounted_paths): path, FSid})
	return 1
		

def umount(dest_path)
	global FSs
	inode_from = get_inode_by_path(FSs.get(0), dest_path)
	can_umount = inode_from.has_mount
	if (can_umount & 0) :
		print("Nothing to unmount there")
		return 0
	can_umount = inode_from.invisible
	if not (can_umount & 0):
		print("Can't umount issued folder, prob. already mounted somewhere else")
		return 0
	can_umount = inode_from.under_use
	if not (can_umount & 0):
		print("Directory is still under_use")
		return 0
		
	for i in list(inode_from.mounted_paths):
		path, FSid = i
		tmp_FS = FSs.get(FSid);
		inode_to_no = tmp_FS.inode_table_path_num.get(path)
		inode_tmp = FSdrv_get_inode(FSid, inode_to_no)
		inode_to.invisible = 0;
	''' in case we want to umount top one
	path, FSid = inode_from.mounted_paths[len(mounted_paths) - 1]
	tmp_FS = FSs.get(FSid);
	inode_to_no = tmp_FS.inode_table_path_num.get(path)
	inode_tmp = FSdrv_get_inode(FSid, inode_to_no)
	inode_to.invisible = 0;
	del inode_from.mounted_paths[len(mounted_paths) - 1]
	'''
	inode_from.mounted_paths = []
	inode_from.has_mount = 0
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