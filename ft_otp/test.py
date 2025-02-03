import rsa

publicKey, privateKey = rsa.newkeys(512)

# print(publicKey)
# print(privateKey)

message = "TEST"

encMessage = rsa.encrypt(message.encode(), publicKey)

decMessage = rsa.decrypt(encMessage, privateKey).decode()


print("encrypted string: ", encMessage)
print("decrypted string: ", decMessage)