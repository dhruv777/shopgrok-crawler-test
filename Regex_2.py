import re

generic_urls = ["https://www.genericdomain.com/abc/def/1290aodwb23-ghi.img", "https://www.genericdomain.com/ab-c/31287bdwakj-jkl.img", "https://www.genericdomain.com/19unioawd02-jkl.img"]

for url in generic_urls:
	special_sequence = [re.findall(r'([^\/]+)-\w+.\w+$', url)[0]]
	# print(special_sequence)

