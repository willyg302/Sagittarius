/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
class Encryption extends Object;

private static function string PadString(string text, string key, int pad)
{
	local int seed, i;
	local string ret;
	ret = "";
	seed = 0;
	for (i = 0; i < Len(key); i++)
	{
		seed += (Asc(Mid(key, i, 1)) * (1 << i));
	}
	seed *= pad;
	for (i = 0; i < Len(text); i++)
	{
		seed = ((seed * 214013 + 2531011) >> 16) & 0x7fff;
		ret $= Chr(byte(Asc(Mid(text, i, 1))) ^ byte(seed));
	}
	return ret;
}

private static function string GetHexForByte(byte b)
{
	local int hi, lo;
	local string hex;
	hex = "0123456789ABCDEF";
	hi = (b >> 4) & 0x0f;
	lo = b & 0x0f;
	return Mid(hex, hi, 1) $ Mid(hex, lo, 1);
}

private static function byte GetByteForHex(string s)
{
	local int hi, lo;
	local string hex;
	hex = "0123456789ABCDEF";
	hi = InStr(hex, Mid(s, 0, 1));
	lo = InStr(hex, Mid(s, 1, 1));
	return byte((hi << 4) + lo);
}

static function string Encrypt(string pt, string key)
{
	local int pad, i;
	local string ct, temp;
	class'Sagittarius'.static.LogDebug("Encrypting " $ pt $ " with key: " $ key);
	ct = "";
	pad = Rand(256);
	temp = PadString(pt, key, pad);
	for (i = 0; i < Len(temp); i++)
	{
		ct $= GetHexForByte(byte(Asc(Mid(temp, i, 1))));
	}
	return "~" $ GetHexForByte(byte(pad)) $ ct;
}

static function string Decrypt(string ct, string key)
{
	local int i;
	local string temp;
	class'Sagittarius'.static.LogDebug("Decrypting " $ ct $ " with key: " $ key);
	temp = "";
	for (i = 3; i < Len(ct); i += 2)
	{
		temp $= Chr(GetByteForHex(Mid(ct, i, 2)));
	}
	return PadString(temp, key, GetByteForHex(Mid(ct, 1, 2)));
}