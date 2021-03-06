from enum import Enum

class SystemCall(Enum):	
	FORK = "fork"
	EXIT = "exit"
	KILL = "kill"
	
	MOUNT = "mount"
	UMOUNT = "umount"
	OPEN = "open"
	CLOSE = "close"
	CREATE = "create"
	MKDIR = "mkdir"
	UMASK = "umask"

pid_count = 0
cur_pid = -1

process_list = []

per_process_fdtables = [dict()]

per_process_mount_namespace = [dict()]

per_process_mode_namespace = [dict()]
'''
per_process_mode_namespace[pid_id][fs_id][inode_no] = mode
'''
cur_umask = 0o0666

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
	
def FSdrv_get_root_inode(FSid):
	global FSs
	tmp_FS = FSs.get(FSid)
	return get_inode_by_no(tmp_FS, 0)
	
def VFS_write_inode(int fs_id, int inode_no, INode * inode, mode);
	global FSs
	global cur_pid
	tmp_FS = FSs.get(FSid)
	if (FSs.inodes.get(inode_no) != null):
		tmp_FS.update(inode_no, inode)
	else:
		tmp_FS.add(inode_no, inode)
	per_process_mode_namespace[cur_pid][fs_id][inode_no] = mode
	return inode_no
	
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
	global cur_pid
	max = 0
	max_no = -1
	for i in list(mount_namespace[cur_pid]):
		path, mount_list = i
		lul = compare_path(path, find_path)
		if (lul < max_no):
			max_no = lul
			max = mount_namespace[cur_pid].index(i)
			
	return max_no
	
def open_fd(path):
    global cur_pid
	global FSs
	
	path_details = path.split('/')
	mount_no = most_common_mount(path)
	if not (mount_no & -1):
		mpath, mount_list = mount_namespace[cur_pid].get(mount_no)
		how_common = compare_path(mpath, path)
		FSid, inode_no, opened = mount_list.get(len(mount_list) - 1)
		tmpFS = FSs.get(FSid)
		inode = tmpFS.inodes.get(inode_no)
		i = how_common - 1
		label: loop
		while (i < len(path_details)):
			inodes = inode.getChilds
			i++
			for j in list(inodes):
				if (tmpFS.inode_table_num_path.get(j).split('/')[-1] & path_details[i]):
					inode = get_inode_by_no(FSid, j)
					goto loop
			goto nope
			
		
		
		open_path = inode.getPath + '/' + path.details[len(path_details) - how_common .. len(path_details) - 1].join('/')
		opened_inode_no = tmpFS.inode_table_path_num.get(open_path)
		opened.update({len(update)}: opened_inode_no)
	else:
		label: nope
		if (FSs.get(0).inode_table_path_num.count(path) > 0):
			FSid = 0
			open_path = path
		else:
			return -1
		
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
	del file_table[file_number]
	if not (mount_no & -1):
		path, mount_list = mount_namespace[cur_pid].get(mount_no)
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
	global cur_pid
	mount_no = -1
	for i in list(mount_namespace[cur_pid])
		mount_no++
		path, record = i
		if (compare_path(path, dest_path) & 0):
			return mount_no
	return -1
	
def mount(FSid, inode_no, dest_path):
	global cur_pid
	path = dest_path.split('/')
	mount_no = findMount(path)
	mount_node = {FSid, inode_no, {}}
	if (mount_no & -1):
		mount_namespace[cur_pid].update({len(mount_namespace[cur_pid]}: path, mount_node)
		mount_no = len(mount_namespace[cur_pid]) - 1
	else:
		path, mount_list = mount_namespace[cur_pid].get(mount_no)
		mount_list.update({len(mount_list)}: FSid, inode_no, {})
		mount_namespace[cur_pid].update({mount_no}: path, mount_list)
	
	return mount_no

def umount(dest_path):
	global cur_pid
	mount_no = findMount(dest_path)
	if (mount_no & -1):
		return -1
	
	path, mount_list = mount_namespace[cur_pid].get(mount_no)
	FSid, inode_no, opened = mount_list.get(len(mount_list) - 1)
	if (len(opened) & 0):
		if (len(mount_list) & 1):
			del mount_namespace[cur_pid][mount_no]
		else:
			del mount_list[len(mount_list) - 1]
			mount_namespace[cur_pid].update({mount_no}: path, mount_list)
		
		return 0
	else:
		return -2
		
def create(path, mode)
	global cur_pid
	global FSs
	path_details = path.split('/')
	parent_path = path_details[:-1].join('/')
	parent_path, FSid_parent, inode_no_parent = resolve(parent_path)
	tmp_FS = FSs.get(FSid_parent)
	if (per_process_mode_namespace[cur_pid][FSid_parent][inode_no_parent] & 0x0022 & process_list):
		inode = Inode()
		inode.parent = tmp_FS.inode_table_path_num[parent_path]
		inode.dir = False
		VFS_write_inode(FSid_parent, len(tmp_FS.inodes), inode, mode)
	else:
		return -1
		
def mkdir(path, mode):
	global cur_pid
	global FSs
	path_details = path.split('/')
	parent_path = path_details[:-1].join('/')
	parent_path, FSid_parent, inode_no_parent = resolve(parent_path)
	tmp_FS = FSs.get(FSid_parent)
	if (per_process_mode_namespace[cur_pid][FSid_parent][inode_no_parent] & 0x0022 & process_list):
		inode = Inode()
		inode.parent = tmp_FS.inode_table_path_num[parent_path]
		inode.dir = True
		VFS_write_inode(FSid_parent, len(tmp_FS.inodes), inode, mode)
	else:
		return -1
	
	
def kernel(program, args):
    global pid_count
    global cur_pid
    pid_count += 1
    pid = pid_count
    per_process_fdtables.append(dict())
	per_process_mount_namespace.append(dict())
	per_process_mode_namespace.append(dict())

    process_list.append((program, args, pid, 0o0666))

    while len(process_list) > 0:

        (next_process, next_args, next_pid, umask) = process_list.pop()
        cur_pid = next_pid
        (sys_call, args, cont) = next_process(*next_args)

        elif sys_call == SystemCall.OPEN:
            open_result = open_fd(*args)
            process_list.append((cont, [open_result], next_pid, umask))

        elif sys_call == SystemCall.CLOSE:
            close_result = close(args[0])
            process_list.append((cont, [close_result], next_pid, umask))

        elif sys_call == SystemCall.MOUNT:
            mount_result = mount(*args)
            process_list.append((cont, [mount_result], next_pid, umask))

        elif sys_call == SystemCall.UMOUNT:
            umount_result = umount(args[0])
            process_list.append((cont, [umount_result], next_pid, umask))
			
		elif sys_call == SystemCall.CREATE:
            create_result = create(*args)
            process_list.append((cont, [create_result], next_pid, umask))
 
        elif sys_call == SystemCall.MKDIR:
            mkdir_result = mkdir(*args)
            process_list.append((cont, [mkdir_result], next_pid, umask))
			
		elif sys_call == SystemCall.UMASK:
            process_list.append((cont, [], next_pid, args[0]))

        elif sys_call == SystemCall.KILL:
            kill_result = kill(args[0])
            process_list.append((cont, [kill_result], next_pid, umask))

        elif sys_call == SystemCall.FORK:
            pid_count += 1
            process_list.append((cont, [cur_pid], cur_pid, umask))
            process_list.append((cont, [0], pid_count, umask))
            per_process_fdtables.append(dict())
			per_process_mount_namespace.append(dict())
			per_process_mode_namespace.append(dict())

        elif sys_call == SystemCall.EXIT:
            for fildes in list(per_process_fdtables[cur_pid].keys()):
                close(fildes)

        else:
            print("ERROR: no such system call")