/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
class ModAction extends DelAction;

function AddModification(string field, string value, optional bool bEncrypt = false)
{
	request.AddURLPair("m", field $ "::" $ value, bEncrypt);
}

DefaultProperties
{
	Handler="/dbmod"
}