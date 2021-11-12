import re
product_count_text = "381 Products found"
product_count_int = int(re.findall(r'(^\d+)', product_count_text)[0])
# print(product_count_int)