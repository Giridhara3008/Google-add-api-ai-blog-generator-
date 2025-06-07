import os
secret_key = os.urandom(24)  # generates a random 24-byte string
print("secret key is",secret_key)
