from utime import sleep_ms
from ota_updater.ota_main import OTAUpdate
import gc
import micropython

def check_for_updates():
	git_url = 'https://github.com/prowebber/micropy_ota'
	wifi_ssid = 'magiceye'
	wifi_pass = 'magiceye'

	o = OTAUpdate(git_url)
	o.using_network(wifi_ssid, wifi_pass)
	o.check_for_update_to_install_during_next_reboot()
	# o.download_and_install_update_if_available(wifi_ssid, wifi_pass)


def start():
	print("Starting script...")
	from project.main import start
	start()


def test():
	import ussl
	import usocket
	
	print("Free mem: %s" % gc.mem_free())
	
	# micropython.mem_info()
	# gc.collect()
	
	key = """-----BEGIN RSA PRIVATE KEY-----
		MIIEpAIBAAKCAQEAwU2j3efNHdEE10lyuJmsDnjkOjxKzzoTFtBa5M2jAIin7h5r
		lqdStJDvLXJ6PiSa/LY0rCT1d+AmZIycsCh9odrqjObJHJa8/sEEUrM21KP64bF2
		2JDBYbRmUjaiJlOqq3ReB30Zgtsq2B+g2Q0cLUlm91slc0boC4pPaQy1AJDh2oIQ
		
		-----END RSA PRIVATE KEY-----
		"""
	
	print("Free mem: %s" % gc.mem_free())
	
	# micropython.mem_info()
	# gc.collect()
	
	
	
	s = usocket.socket()
	
	# Get the {IP}{port} of the address in a tuple
	address_tuple = usocket.getaddrinfo('www.dog-learn.com', 80)[0][-1]
	ip_address = address_tuple[0]
	print(address_tuple[0])
	
	s.connect((ip_address, 443))
	# s = ussl.wrap_socket(s, server_side=True, key=key, cert=cert)



def on_boot():
	"""
	Called first
	"""
	check_for_updates()  # Check for any pending updates
	start()  # Start the script
	print("here")


# on_boot()  # Start the script
