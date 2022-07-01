from .http_requests import HttpClient
import os
import gc
from machine import reset


class OTADownload:
    def __init__(self, github_repo, module='', src_dir='', tgt_dir='', headers={}):
        self.headers = headers
        self.http_client = HttpClient()
        self.github_repo = github_repo.rstrip('/').replace('https://github.com', 'https://api.github.com/repos')
        self.main_dir = tgt_dir
        self.module = module.rstrip('/')
        self.src_dir = src_dir.rstrip('/') + '/' if src_dir else ''

    def __del__(self):
        self.http_client = None

    def start(self, ssid, password):
        if 'next' in os.listdir(self.module):
            if '.version_on_reboot' in os.listdir(self.modulepath('next')):
                latest_version = self.get_version(self.modulepath('next'), '.version_on_reboot')
                print('New update found: ', latest_version)
                OTADownload._using_network(ssid, password)
                self._download_and_install_update(latest_version)
        else:
            print('No new updates found...')

    @staticmethod
    def _using_network(ssid, password):
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
        self.download_all_files(self.github_repo + '/contents/' + self.src_dir + self.main_dir, latest_version)
        self.rmtree(self.modulepath(self.main_dir))
        os.rename(self.modulepath('next/.version_on_reboot'), self.modulepath('next/.version'))
        os.rename(self.modulepath('next'), self.modulepath(self.main_dir))
        print('Update installed (', latest_version, '), will reboot now')
        reset()

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
        file_list = self.http_client.get(root_url + '?ref=refs/tags/' + version, headers=self.headers, dtype='json')

        # Create a much smaller version of the data
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
        gc.collect()

        for file_type in file_params:  # Loop through each file type
            for file in file_params[file_type]:  # Loop through each file
                download_url = file['download_url']
                file_path = file['path']
                file_name = file['name']

                if file_type == 'file':
                    download_path = self.modulepath(
                        'next/' + file_path.replace(self.main_dir + '/', '').replace(self.src_dir, ''))
                    self.download_file(download_url.replace('refs/tags/', ''), download_path)
                elif file_type == 'dir':
                    path = self.modulepath(
                        'next/' + file_path.replace(self.main_dir + '/', '').replace(self.src_dir, ''))
                    self.mkdir(path)
                    self.download_all_files(root_url + '/' + file_name, version)
            gc.collect()

    def download_file(self, url, path):
        print('\t----- Downloading: ', path)
        self.http_client.get(url, headers=self.headers, dtype='content', saveToFile=path)

    def modulepath(self, path):
        return self.module + '/' + path if self.module else path

    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            f = open(directory + '/' + version_file_name)
            version = f.read()
            f.close()
            return version
        return '0.0'

    def mkdir(self, path):
        try:
            os.mkdir(path)
        except OSError as exc:
            if exc.args[0] == 17:
                pass
