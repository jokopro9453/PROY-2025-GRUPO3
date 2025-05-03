from fuzzywuzzy import fuzz
passwd = "hermano"
upass = "ermano"
similitud_pass = fuzz.ratio(passwd,upass)
print(similitud_pass)