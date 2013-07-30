#!/usr/local/bin/python
# coding: utf-8

from random import randrange


def padstring(text, key, pad):
	ret = ''
	seed = 0
	for i in range(0, len(key)):
		seed += (ord(key[i]) * (1 << i))
	seed *= pad
	for i in range(0, len(text)):
		seed = ((seed * 214013 + 2531011) >> 16) & 0x7fff
		ret += chr(ord(text[i]) ^ (seed & 0xff))
	return ret

def getHexForByte(b):
	hex = '0123456789ABCDEF'
	hi = (b >> 4) & 0x0f
	lo = b & 0x0f
	return hex[hi] + hex[lo]

def getByteFoxHex(s):
	hex = '0123456789ABCDEF'
	hi = hex.find(s[0])
	lo = hex.find(s[1])
	return ((hi << 4) + lo) & 0xff

def encrypt(pt, key):
	ct = ''
	pad = randrange(256)
	temp = padstring(pt, key, pad)
	for i in range(0, len(temp)):
		ct += getHexForByte(ord(temp[i]) & 0xff)
	return "~" + getHexForByte(pad & 0xff) + ct

def decrypt(ct, key):
	temp = ''
	for i in range(3, len(ct), 2):
		temp += chr(getByteFoxHex(ct[i:i+2]))
	return padstring(temp, key, getByteFoxHex(ct[1:3]))


if __name__ == "__main__":
	pass # Do nothing, this is an included script only