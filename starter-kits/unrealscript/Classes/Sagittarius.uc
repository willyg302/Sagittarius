/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright WillyG Productions
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
	local SagRequest sr;
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
	sr = new class'SagRequest';
	a.InitializeRequest(sr.Initialize(self));
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



function SubmitRequest(SagRequest sr)
{
	Link.TransmitRequest(sr);
}



/** CALLBACK FUNCTIONS **/

function OnResponseReceived(string ModuleID, string ActionID, SagResponse resp)
{
	if (ModuleID == "builtin")
	{
		BuiltInOnResponseReceived(ActionID, resp);
		return;
	}
	GetModule(ModuleID).OnResponseReceived(ActionID, resp);
}

function BuiltInOnResponseReceived(string ActionID, SagResponse resp)
{
	// @TODO: Make more robust
	if (ActionID == "mail")
	{
		class'WorldInfo'.static.GetWorldInfo().Game.Broadcast(self, "Mail successfully sent!");
	}
}



/** SPECIAL FUNCTIONS **/

function SendMail(string Receiver, string Subject, string Message, optional string Sender = "")
{
	local SagRequest mail;
	mail = new class'SagRequest';
	mail = mail.Initialize(self).SetDestination("/mail").SetModuleInfo("builtin", "mail");
	mail.AddURLPair("recv", Receiver, false);
	mail.AddURLPair("subj", Subject, false);
	mail.AddURLPair("mesg", Message, false);
	if (Sender != "")
	{
		mail.AddURLPair("send", Sender, false);
	}
	SubmitRequest(mail);
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


function string Encrypt(string pt)
{
	return class'Encryption'.static.Encrypt(pt, SagPass);
}

function string Decrypt(string ct)
{
	return class'Encryption'.static.Decrypt(ct, SagPass);
}


DefaultProperties
{
	LogLevel=LOG_Debug
}
