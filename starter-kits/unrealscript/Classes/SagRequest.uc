/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
class SagRequest extends Object;

var string dest, data, mID, qID;
var Sagittarius Parent;
var private string delim;

function SagRequest Initialize(Sagittarius s)
{
	Parent = s;
	return self;
}

function Submit()
{
	Parent.SubmitRequest(self);
}

function AddURLPair(string param, string value, bool bEncryptValue)
{
	if (bEncryptValue)
	{
		value = Parent.Encrypt(value);
	}
	data $= (delim $ param $ "=" $ value);
	delim = "&";
}

function SagRequest SetDestination(string newDest)
{
	dest = newDest;
	return self;
}

function SagRequest SetModuleInfo(string newMID, string newQID)
{
	mID = newMID;
	qID = newQID;
	return self;
}

DefaultProperties
{
	data=""
	delim=""
}