import gc


print("Free mem 0A: %s" % gc.mem_free())

def check_for_updates():
	from ota_updater.ota_main import OTAUpdate
	
	git_url = 'https://github.com/prowebber/micropy_ota'
	wifi_ssid = 'magiceye'
	wifi_pass = 'magiceye'
	
	print("Free mem 2A: %s" % gc.mem_free())
	
	o = OTAUpdate(git_url)  # Init OTA
	o.using_network(wifi_ssid, wifi_pass)  # Connect to WiFi
	
	print("Free mem 3A: %s" % gc.mem_free())
	
	o.check_for_update_to_install_during_next_reboot()  # Check for pending updates


def install_updates():
	from ota_updater.ota_download import OTADownload
	
	print("Free mem 5A: %s" % gc.mem_free())
	
	git_url = 'https://github.com/prowebber/micropy_ota'
	wifi_ssid = 'magiceye'
	wifi_pass = 'magiceye'
	
	o = OTADownload(git_url)  # Init OTA
	o.using_network(wifi_ssid, wifi_pass)  # Connect to WiFi
	
	print("Free mem 6A: %s" % gc.mem_free())
	
	o.start()



def working():
	import ussl
	import usocket
	
	s = usocket.socket()
	
	# Get the {IP}{port} of the address in a tuple
	address_tuple = usocket.getaddrinfo('www.dog-learn.com', 80)[0][-1]
	ip_address = address_tuple[0]
	print(address_tuple[0])
	
	s.connect((ip_address, 443))
	s = ussl.wrap_socket(s, server_hostname='dog-learn.com')
	print(s)


def test():
	print("Free mem 1A: %s" % gc.mem_free())
	gc.enable()  # Enable automatic garbage collection
	# check_for_updates()
	install_updates()


# on_boot()  # Start the script
