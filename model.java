enum SystemCall {
	FORK("fork"),
	EXIT("exit"),
	KILL("kill"),
	
	MOUNT("mount"),
	UMOUNT("umount"),
	OPEN("open"),
	CLOSE("close"),
	CREATE("create"),
	MKDIR("mkdir"),
	UMASK("mask")
}

int pid_count = 0
int cur_pid = -1

int mask = 0x111111111;

process_list = []
fdtable = [dict()]
file_table = [dict()]

Record[] mount_namespace = [dict()]
Record = (String[] path, Mount_list)
Mount_list[] = (int FSid, int inode_no, int[] opened)

cur_umask = 0o0666

FSid FSdrv_load_fs(path block_device_path) {
	return FSid;
}

Inode FSdrv_get_inode(int FSid, int inode_no) {
	return inode;
}

data FSdrv_get_data(int FSid, int offset) {
	return data;
}

Inode FSdrv_get_root_inode(int FSid) {
	return inode;
}

int VFS_write_inode(int FSid, int inode_no, Inode inode) {
	return write(FSid, inode_no, inode);
}

// returns number > 0 if path1 is prefix of path2
// 0 if path1 == path2
// number < 0 if path2 is prefix of path1
// takes: path1, path2
// returns: number
int common_length(String[] path1, String[] path2) {
	int answer = 0;
	for (String s1 : path1) {
		if (s1 == path2[answer]) {
			answer++;
		} else {
			return answer;
		}
	}
	
	if (path1.length == path2.length) {
		return 0;
	} else {
		return path1.length - path2.length;
	}
}

// returns mount_no of the most common suting mount from mount_namespace
// takes: path
// returns: mount_no
int most_common_mount(String[] find_path) {
	int max = 0;
	int max_no = -1;
	for (path in mount_namespace) {
		int tmp = common_length(path, find_path);
		if (tmp > max_no) {
			max = tmp;
			max_no = mount_namespace.get_no_by_path(path);
		}
	}
	return max_no;
}

// construstes path from root inode to requested
// takes: inode, inode_no
// returnes: path
path dfs(inode, inode_no) {
	if (inode_no == inode.number) {
		return inode.name;
	}
	for (i : inode.children) {
		if (dfs(i, inode_no) != null) {
			return inode.name + '/' + dfs(i, inode_no);
		}
	}
	return null;
}

// gets inode_no by moving from inode using path to destenation
// takse: inode, path
// returnes: inode_no
inode_no dfs2(inode, path) {
	if (path[0] = inode.name) {
		return inode.number;
	}
	return dfs2(inode.children.get(path[0]), path[1..])
}

// returns original path in FSid given midpoint inode_no and end of path - path
// takes:FSid, inode_no, path
// returns: path, inode_no
path, inode_no resolve_path(FSid, inode_no, path) {
	root_inode = FSdrv_get_root_inode(FSid);
	half_path = dfs(root_inode, inode_no);
	half_path2, answer_no = dfs2(FSdrv_get_inode(FSid, inode_no), path);
	return half_path + '/' + half_path2, answer_no;
}

int open_fd(String path) {
	String[] path_parts = path.split('/');
	int moun_no = most_common_mount(path);
	if (moun_no != -1) {
		mpath, mount_list = mount_namespace.get(moun_no);
		FSis, inode_no, opened = mount_list.get(mount_list.size() - 1);
		how_common = common_length(mpath, path);
		
		open_path, inode_no_open = resolve_path(FSid, inode_no, path[how_common..])
		
		opened.add(inode_no_open);
	} catch {
		FSid = 0
		open_path = path
	}
	
	if (fdtable.length() > 0) {
		fildes = fdtable.length() + 1;
	} else {
		fildes = 3;
	}
	
	offset = 0;
	file_table.add((open_path, moun_no, FSid, offset))
	fdtable[fildes] = file_table.size() - 1;
	
	return fildes;
}

int close(fildes) {
	file_number = fdtable[fildes];
	path, moun_no, FSid, offset = file_table[file_number]
	fdtable.remove(fildes);
	file_table.remove(file_number);
	if (moun_no != -1) {
		path, mount_list = mount_namespace
		for (FSid2, inode_no, opened : mount_list) {
			if (Fsid2 == FSid) {
				opened.remove(inode_no);
			}
		}
	}
	return 0;
}

// returns moun_no from mount_namespace if present by its path
// takes: path
// returns: mount_no
int find_mount(String path) {
	return mount_namespace.get_no(path);
}

int mount(int FSid, int inode_no, String dest_path) {
	String[] path = dest_path.split('/');
	int mount_no = find_mount(dest_path);
	mount_tmp = {FSid, inode_no, []}
	if (moun_no == -1) {
		mount_namespace.add(new Record(path, [mount_tmp]))
		return mount_namespace.size() - 1;
	} else {
		path, mount_list = mount_namespace.get(moun_no);
		mount_list.add(mount_tmp);
		mount_namespace.replace(this.size() - 1 : path, mount_list);
		return moun_no;
	}
}

int umount(String dest_path) {
	int moun_no = find_mount(dest_path);
	if (moun_no == -1) {
		print("Umount: requested paht has no mounts");
		return -1;
	}
	
	path, mount_list = mount_namespace.get(moun_no);
	FSid, inode_no, opened = mount_list.pop();
	if (opened.size() == 0) {
		if (mount_list.size() == 0) {
			mount_namespace.remove(moun_no);
		} else {
			mount_namespace.put(path, mount_list);
		}
		return 0;
	} else {
		return -2;
	}
}

int creat(path, mode) {
	path_details = path.split('/');
	parent_path = path_details[0..-1];
	FSid_parent, inode_no_parent = resolve(parent_path);
	if (mode[1] == 1) {
		inode = Inode()
		inode.parent = inode_no_parent;
		inode.type = FILE;
		inode.mode = !mode xor umask;
		VFS_write_inode(FSid_parent, -1, inode);
		VFS_write_inode(FSid_parent, inode_no_parent, FSdrv_get_inode(FSdrv_get_inode(FSid_parent, inode_no_parent).children.add(inode));
		return 0;
	} else {
		return -1;
	}
}

int mkdir(path, mode) {
	path_details = path.split('/');
	parent_path = path_details[0..-1];
	FSid_parent, inode_no_parent = resolve(parent_path);
	if (mode[1] == 1) {
		inode = Inode()
		inode.parent = inode_no_parent;
		inode.type = DIR;
		inode.mode = !mode xor umask;
		VFS_write_inode(FSid_parent, -1, inode);
		VFS_write_inode(FSid_parent, inode_no_parent, FSdrv_get_inode(FSdrv_get_inode(FSid_parent, inode_no_parent).children.add(inode));
		return 0;
	} else {
		return -1;
	}
}

int kill(int pid) {
	process_list.remove(pid);
	return 0;
}

void kernel(program, args) {
	global int pid_count;
	global int cur_pid;
	pid_count++;
	pid = pid_count;
	fdtable = dict();
	mount_namespace = dict();
	
	process_list.add((program, args, pid))
	
	while (process_list.size() > 0) {
		(next_process, next_args, next_pid, umask) = process_list.pop()
		cur_pid = next_pid;
		(sys_call, args, cont) = next_process(next_args)
		
		switch (sys_call) {
			OPEN:
				open_result = open_fd(args);
				process_list.add((cont, [open_result], next_pid));
				break;
				
			CLOSE:
				close_result = close(args[0]);
				process_list.add((cont, [close_result], next_pid));
				break;
				
			MOUNT:
				mount_result = mount(args);
				process_list.add((cont, [mount], next_pid));
				break;
				
			UMOUNT:
				umount_result = umount(args[0]);
				process_list.add((cont, [umount_result], next_pid));
				break;
				
			CREATE:
				create_result = create(args);
				process_list.add((cont, [create], next_pid));
				break;
				
			MKDIR:
				mkdir_result = mkdir(args);
				process_list.add((cont, [mkdir_result], next_pid));
				break;
				
			UMASK:
				mask = args[0];
				process_list.add((cont, [], next_pid));
				break;
				
			KILL:
				kill_result = kill(args[0]);
				process_list.add((cont, [kill_result], next_pid));
				break;
				
			FORK:
				pid_count++;
				process_list.add((cont, [cur_pid], cur_pid));
				process_list.add((cont, [fdtable, mount_namespace], pid_count));
				break;
				
			EXIT:
				break;
				
			default:
				print("No such call");
		}
	}
}


