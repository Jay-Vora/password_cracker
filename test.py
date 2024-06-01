from hashlib import md5

# print(md5(b'password').hexdigest())
wrd_list = md5()

wrd_list.update(b'password')

digest = wrd_list.hexdigest()

print(digest)