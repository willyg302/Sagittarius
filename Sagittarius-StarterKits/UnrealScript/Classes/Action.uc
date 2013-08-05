/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class Action extends Object abstract;

const DBTYPE = "object_type";
const DBNAME = "object_name";

var private string Handler, Password;

function SetPassword(string Pass)
{
	Password = Pass;
}

function string Encrypt(string Text, bool bEncrypt)
{
	if (bEncrypt)
	{
		Text = class'Encryption'.static.Encrypt(Text, Password);
	}
	return Text;
}

function string GetHandler()
{
	return Handler;
}

function string GetURLString()
{
	return "";
}