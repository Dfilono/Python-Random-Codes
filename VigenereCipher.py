def vigenere_cipher(message, key, method = "decode"):
  decoded_message = ''
  keyphrase = ''
  alph = 'abcdefghijklmnopqrstuvwxyz'
  letter_point = 0
  for i in range(len(message)):
    if message[i] not in alph:
      keyphrase += message[i]
    else:
      keyphrase += key[letter_point]
      letter_point = (letter_point + 1) % len(key) 
  if method == "decode":
    for i in range(len(message)):
      if message[i] not in alph:
        decoded_message += message[i]
      else:
        decoded_message += alph[(alph.find(message[i]) + alph.find(keyphrase[i])) % len(alph)]
  elif method == "encode":
    for i in range(len(message)):
      if message[i] not in alph:
        decoded_message += message[i]
      else:
        decoded_message += alph[(alph.find(message[i]) - alph.find(keyphrase[i])) % len(alph)]
  return decoded_message
