def caesar_ciper(message, offset, method = "decode"):
  decoded_message = ''
  alph = 'abcdefghijklmnopqrstuvwxyz'
  if method == "decode":
    for i in message:
      if i not in alph:
        decoded_message += i
      else:
        decoded_message += alph[(alph.find(i) + offset) % len(alph)]
  elif method == "encode":
    for i in message:
      if i not in alph:
        decoded_message += i
      else:
        decoded_message += alph[(alph.find(i) - offset)]
  return decoded_message
