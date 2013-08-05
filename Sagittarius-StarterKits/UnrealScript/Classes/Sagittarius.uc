/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class Sagittarius extends Actor;

var SagittariusLinkClient Link;

var private String SagPass;

struct ModuleStruct
{
	var string ID;
	var Module m;
};

var array<ModuleStruct> Modules;

const LOG_TAG = 'Sagittarius';

var const enum ELogLevel
{
	LOG_None,
	LOG_Error,
	LOG_Warn,
	LOG_Info,
	LOG_Debug
} LogLevel;


function Initialize(string AppID, string Pass)
{
	Link = Spawn(class'SagittariusLinkClient');
	Link.Initialize(self, AppID);
	SagPass = Pass;
}

function Action CreateAction(string Type)
{
	local Action a;
	if (Type == "get")
	{
		a = new class'GetAction';
	}
	else if (Type == "add")
	{
		a = new class'AddAction';
	}
	else if (Type == "mod")
	{
		a = new class'ModAction';
	}
	else if (Type == "del")
	{
		a = new class'DelAction';
	}
	else
	{
		return none;
	}
	a.SetPassword(SagPass);
	return a;
}

function RegisterModule(Module m)
{
	local ModuleStruct ms;
	ms.ID = m.ID;
	ms.m = m;
	Modules.AddItem(ms);
	m.Initialize(self);
}

function Module GetModule(string ID)
{
	local int index;
	index = Modules.Find('ID', ID);
	if (index == INDEX_NONE)
	{
		LogWarn("GetModule() - module with ID " $ ID $ " does not exist");
		return None;
	}
	else
	{
		return Modules[index].m;
	}
}



function SubmitAction(string ModuleID, string ActionID, Action a)
{
	Link.Transmit(true, a.GetHandler(), ModuleID, ActionID, a.GetURLString());
}



/** CALLBACK FUNCTIONS **/

function OnTextReceived(string ModuleID, string ActionID, string Text)
{
	if (ModuleID == "builtin")
	{
		BuiltInOnTextReceived(ActionID, Text);
		return;
	}
	GetModule(ModuleID).OnTextReceived(ActionID, Text);
}

function OnCallbackReceived(string ModuleID, string ActionID)
{
	if (ModuleID == "builtin")
	{
		BuiltInOnCallbackReceived(ActionID);
		return;
	}
	GetModule(ModuleID).OnCallbackReceived(ActionID);
}

function BuiltInOnTextReceived(string ActionID, string Text)
{
	//
}

function BuiltInOnCallbackReceived(string ActionID)
{
	// @TODO: Test
	if (ActionID == "mail")
	{
		class'WorldInfo'.static.GetWorldInfo().Game.Broadcast(self, "Mail successfully sent!");
	}
}



/** MAIL **/

function SendMail(string Receiver, string Subject, string Message, optional string Sender = "")
{
	local string Contents;
	Contents = "recv=" $ Receiver $ "&subj=" $ Subject $ "&mesg=" $ Message;
	if (Sender != "")
	{
		Contents $= ("&send=" $ Sender);
	}
	Link.Transmit(true, "/mail", "builtin", "mail", Contents);
}


/** LOG FUNCTIONS **/

static function LogError(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 0)
	{
		`LogError(cat, msg);
	}
}

static function LogWarn(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 1)
	{
		`LogWarn(cat, msg);
	}
}

static function LogInfo(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 2)
	{
		`LogInfo(cat, msg);
	}
}

static function LogDebug(string msg, optional name cat = LOG_TAG)
{
	if (default.LogLevel > 3)
	{
		`LogDebug(cat, msg);
	}
}


function string GetXMLValue(string XMLTag, string Text)
{
	local int XMLTagStart, XMLTagEnd;
	local string ret;
	XMLTagStart = InStr(Text, "<" $ XMLTag $ ">");
	if (XMLTagStart < 0)
	{
		return "";
	}
	XMLTagStart += (Len(XMLTag) + 2);
	XMLTagEnd = InStr(Text, "</" $ XMLTag $ ">");
	if (XMLTagEnd < XMLTagStart)
	{
		return "";
	}
	ret = Mid(Text, XMLTagStart, XMLTagEnd - XMLTagStart);
	if (InStr(ret, "~") == 0)
	{
		ret = class'Encryption'.static.Decrypt(ret, SagPass);
	}
	return ret;
}


DefaultProperties
{
	LogLevel=LOG_Debug
}
