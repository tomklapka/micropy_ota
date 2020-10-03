import uos

# Specify what files need to be moved/deleted
file_list = {
	'delete': {
		'project/my_file.txt': None,
		'test_file.py': None,
	},
	'move': {
		'ota_updater\\__init__.py': 'ota_updater/__init__.py',
		'ota_updater\\ota_check.py': 'ota_updater/ota_check.py',
		'ota_updater\\ota_download.py': 'ota_updater/ota_download.py',
		'ota_updater\\ota_main.py': 'ota_updater/ota_main.py',
		'ota_updater\\static.py': 'ota_updater/static.py',
		'project\\__init__.py': 'project/__init__.py',
		'project\\steven.py': 'project/steven.py'
	},
}

"""
Search for and move files that have been mislabeled by flashing
"""

# Loop through each file
files_moved = 0
files_deleted = 0

for action in file_list:
	for bad_path, new_path in file_list[action].items():
		# Check if the file exists
		# Path module is not included in MicroPython so use this method
		try:
			f = open(bad_path)
			exists = True
			f.close()
		except OSError:
			exists = False
			
		# Modify the file
		if exists:
			if action == 'move':
				uos.rename(bad_path, new_path)
				files_moved += 1
			elif action == 'delete':
				uos.remove(bad_path)
				files_deleted += 1
		
print("Files moved: %s" % files_moved)
print("Files deleted: %s" % files_deleted)