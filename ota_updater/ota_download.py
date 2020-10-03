from ota_updater.static import HttpClient
import os
import gc

class OTADownload:
	def __init__(self, github_repo, module='', main_dir='project'):
		self.http_client = HttpClient()
		self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
		self.main_dir = main_dir
		self.module = module.rstrip('/')
		
		
	def start(self):
		if 'next' in os.listdir(self.module):
			if '.version_on_reboot' in os.listdir(self.modulepath('next')):
				latest_version = self.get_version(self.modulepath('next'), '.version_on_reboot')
				print('New update found: ', latest_version)
				print("Free mem 7A: %s" % gc.mem_free())
				self._download_and_install_update(latest_version)
		else:
			print('No new updates found...')
	
	@staticmethod
	def using_network(ssid, password):
		import network
		sta_if = network.WLAN(network.STA_IF)
		if not sta_if.isconnected():
			print('connecting to network...')
			sta_if.active(True)
			sta_if.connect(ssid, password)
			while not sta_if.isconnected():
				pass
		print('network config:', sta_if.ifconfig())
	
	def _download_and_install_update(self, latest_version):
		self.download_all_files(self.github_repo + '/contents/' + self.main_dir, latest_version)
		print("Free mem 9A: %s" % gc.mem_free())
		
		self.rmtree(self.modulepath(self.main_dir))
		print("Free mem 10A: %s" % gc.mem_free())
		os.rename(self.modulepath('next/.version_on_reboot'), self.modulepath('next/.version'))
		os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
		print('Update installed (', latest_version, '), will reboot now')
	
	def rmtree(self, directory):
		for entry in os.ilistdir(directory):
			is_dir = entry[1] == 0x4000
			if is_dir:
				self.rmtree(directory + '/' + entry[0])
			
			else:
				os.remove(directory + '/' + entry[0])
		os.rmdir(directory)
	
	def download_all_files(self, root_url, version):
		print("\t----- Downloading: %s" % root_url)
		print("Free mem 8A: %s" % gc.mem_free())
		
		file_list = self.http_client.get(root_url + '?ref=refs/tags/' + version, dtype='json')
		print(file_list)
		gc.collect()
		
		# Create a much smaller version of the file dict
		file_params = {
			'file': [],
			'dir': []
		}
		for file in file_list:
			file_type = file['type']
			
			file_params[file_type].append({
				'download_url': file['download_url'],
				'path': file['path'],
				'name': file['name'] if 'name' in file else None
			})
			
		del file_list  # Reset/erase data
		print(file_params)
		gc.collect()
		
		print("Free mem 8B: %s" % gc.mem_free())
		
		for file_type in file_params:  # Loop through each file type
			for file in file_params[file_type]:  # Loop through each file
				download_url = file['download_url']
				file_path = file['path']
				file_name = file['name']
				
				if file_type == 'file':
					download_path = self.modulepath('next/' + file_path.replace(self.main_dir + '/', ''))
					self.download_file(download_url.replace('refs/tags/', ''), download_path)
				elif file_type == 'dir':
					path = self.modulepath('next/' + file_path.replace(self.main_dir + '/', ''))
					os.mkdir(path)
					self.download_all_files(root_url + '/' + file_name, version)
			gc.collect()
		
		# for file in file_list:
		# 	if file['type'] == 'file':
		# 		download_url = file['download_url']
		# 		download_path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
		# 		self.download_file(download_url.replace('refs/tags/', ''), download_path)
		# 	elif file['type'] == 'dir':
		# 		path = self.modulepath('next/' + file['path'].replace(self.main_dir + '/', ''))
		# 		os.mkdir(path)
		# 		self.download_all_files(root_url + '/' + file['name'], version)
		# 	gc.collect()
	
	def download_file(self, url, path):
		print('\t----- Downloading: ', path)
		print("Before: %s" % gc.mem_free())
		with open(path, 'w') as outfile:
			try:
				response = self.http_client.get(url, dtype='text')
				outfile.write(response)
			finally:
				outfile.close()
				gc.collect()
		print("After: %s" % gc.mem_free())
	
	def modulepath(self, path):
		return self.module + '/' + path if self.module else path
	
	def get_version(self, directory, version_file_name='.version'):
		if version_file_name in os.listdir(directory):
			f = open(directory + '/' + version_file_name)
			version = f.read()
			f.close()
			return version
		return '0.0'