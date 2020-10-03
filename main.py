
def check_for_updates(github_url):
	"""
	Check for any new updates posted to GitHub
	"""
	from ota_updater.ota_check import OTACheck
	
	o = OTACheck(github_url)  # Init OTA
	o.start()  # Check for pending updates


def install_updates(github_url):
	"""
	Download an replace existing files with updated files
	"""
	from ota_updater.ota_download import OTADownload
	
	o = OTADownload(github_url)  # Init OTA
	o.start()


def test():
	"""
	Example for OTA
	- Specify the creds below
	- Replace the GitHub repository with the one you want to OTA
	"""
	import gc
	from ota_updater.wifi_conn import connect_to_wifi
	
	# Creds
	wifi_ssid = 'magiceye'
	wifi_pass = 'magiceye'
	github_url= 'https://github.com/prowebber/micropy_ota'
	
	gc.enable()  # Enable automatic garbage collection
	
	# Connect to the WiFI
	has_wifi = connect_to_wifi(wifi_ssid, wifi_pass)
	if has_wifi:  # If WiFi is connected
		check_for_updates(github_url)
		install_updates(github_url)
