/**
 * Sagittarius - Java Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
package com.willyg.sagittarius;

public class Encryption {
    private static String PadString(String text, String key, int pad) {
        String ret = "";
        int seed = 0;
        for (int i = 0; i < key.length(); i++) {
            seed += ((key.charAt(i) & 0xff) * (1 << i));
        }
        seed *= pad;
        for (int i = 0; i < text.length(); i++) {
            seed = ((seed * 214013 + 2531011) >>> 16) & 0x7fff;
            ret += Character.toString((char)((text.charAt(i) & 0xff) ^ (seed & 0xff)));
        }
        return ret;
    }

    private static String GetHexForByte(int b) {
        String hex = "0123456789ABCDEF";
        int hi = (b >>> 4) & 0x0f;
        int lo = b & 0x0f;
        return Character.toString(hex.charAt(hi)) + Character.toString(hex.charAt(lo));
    }

    private static int GetByteForHex(String s) {
        String hex = "0123456789ABCDEF";
        int hi = hex.indexOf(s.charAt(0));
        int lo = hex.indexOf(s.charAt(1));
        return ((hi << 4) + lo) & 0xff;
    }

    public static String Encrypt(String pt, String key) {
        Sagittarius.LogDebug("Encrypting " + pt + " with key: " + key);
        String ct = "";
        int pad = (int)(Math.random() * 256);
        String temp = PadString(pt, key, pad);
        for (int i = 0; i < temp.length(); i++) {
            ct += GetHexForByte(temp.charAt(i) & 0xff);
        }
        return "~" + GetHexForByte(pad & 0xff) + ct;
    }

    public static String Decrypt(String ct, String key) {
        Sagittarius.LogDebug("Decrypting " + ct + " with key: " + key);
        String temp = "";
        for (int i = 3; i < ct.length(); i += 2) {
            temp += Character.toString((char)GetByteForHex(ct.substring(i, i + 2)));
        }
        return PadString(temp, key, GetByteForHex(ct.substring(1, 3)));
    }
}
