import test_file as example
import sys
# sys.path.append('/path/to/application/app/folder')
# from .project.steven import start
# from project import steven



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


# on_boot()  # Start the script
