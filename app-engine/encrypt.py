from random import randrange


def pad_string(text, key, pad):
	ret = ''
	seed = pad * sum([ord(e) * (1 << i) for i, e in enumerate(key)])
	for c in text:
		seed = ((seed * 214013 + 2531011) >> 16) & 0x7fff
		ret += chr(ord(c) ^ (seed & 0xff))
	return ret

def byte_to_hex(b):
	hex = '0123456789ABCDEF'
	hi = (b >> 4) & 0x0f
	lo = b & 0x0f
	return hex[hi] + hex[lo]

def hex_to_byte(s):
	hex = '0123456789ABCDEF'
	hi = hex.find(s[0])
	lo = hex.find(s[1])
	return ((hi << 4) + lo) & 0xff

def encrypt(pt, key):
	pad = randrange(256)
	padded = pad_string(pt, key, pad)
	ct = ''.join([byte_to_hex(ord(c) & 0xff) for c in padded])
	return "~" + byte_to_hex(pad & 0xff) + ct

def decrypt(ct, key):
	temp = ''
	for i in range(3, len(ct), 2):
		temp += chr(hex_to_byte(ct[i:i+2]))
	return pad_string(temp, key, hex_to_byte(ct[1:3]))
