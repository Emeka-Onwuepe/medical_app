import secrets
from random import randint
def generate_otp():
  
  otp = str(secrets.randbits(20))
  length = len(otp)
  if length == 6:
    otp = otp
    
  elif length > 6:
    otp = otp[:6]
  else:
    needed = 6 - length
    num = str(randint(100000, 999999))[:needed]
    otp = f'{otp}{num}'
    
  return int(otp)