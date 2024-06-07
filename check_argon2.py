from argon2 import PasswordHasher

ph = PasswordHasher()
hash = ph.hash("hey there")
print(hash)
print(ph.verify(hash, "hey ther"))
