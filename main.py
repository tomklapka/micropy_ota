import gc
from assets.wifi_conn import connect_to_wifi

# Creds
main_dir = 'project'
wifi_ssid = 'magiceye'
wifi_pass = 'magiceye'
github_url = 'https://github.com/prowebber/micropy_ota'

gc.enable()  # Enable automatic garbage collection


def ota_check():
	"""
	Check for any new updates posted to GitHub
	"""
	has_wifi = connect_to_wifi(wifi_ssid, wifi_pass)
	if has_wifi:  # If WiFi is connected
		from assets.ota_check import OTACheck
		
		o = OTACheck(github_url, tgt_dir=main_dir)
		o.start()  # Check for pending updates


def ota_install():
	"""
	Download an replace existing files with updated files
	"""
	# Connect to the WiFI
	has_wifi = connect_to_wifi(wifi_ssid, wifi_pass)
	if has_wifi:  # If WiFi is connected
		from assets.ota_download import OTADownload
		
		o = OTADownload(github_url, tgt_dir=main_dir)  # Init OTA
		o.start()