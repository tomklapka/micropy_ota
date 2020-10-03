import gc
from ota_updater.wifi_conn import connect_to_wifi
from machine import reboot

# Creds
main_dir = 'project'
wifi_ssid = 'magiceye'
wifi_pass = 'magiceye'
github_url = 'https://github.com/prowebber/micropy_ota'

gc.enable()  # Enable automatic garbage collection


def check_for_updates():
	"""
	Check for any new updates posted to GitHub
	"""

	# Connect to the WiFI
	has_wifi = connect_to_wifi(wifi_ssid, wifi_pass)
	if has_wifi:  # If WiFi is connected
		from ota_updater.ota_check import OTACheck

		o = OTACheck(github_url, main_dir = main_dir)  # Init OTA
		o.start()  # Check for pending updates


def install_updates():
	"""
	Download an replace existing files with updated files
	"""

	# Connect to the WiFI
	has_wifi = connect_to_wifi(wifi_ssid, wifi_pass)
	if has_wifi:  # If WiFi is connected
		from ota_updater.ota_download import OTADownload

		o = OTADownload(github_url, main_dir = main_dir)  # Init OTA
		o.start()
