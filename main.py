from ota_updater.ota_main import OTAUpdate


def check_for_updates():
	git_url = 'https://github.com/prowebber/micropy_ota'
	wifi_ssid = 'magiceye'
	wifi_pass = 'magiceye'


	o = OTAUpdate(git_url)
	o.download_and_install_update_if_available(wifi_ssid, wifi_pass)


def start():
	print("Starting script...")
	from project.main import start
	start()


def on_boot():
	"""
	Called first
	"""
	check_for_updates()  # Check for any pending updates
	start()  # Start the script
	print("here")


on_boot()  # Start the script
