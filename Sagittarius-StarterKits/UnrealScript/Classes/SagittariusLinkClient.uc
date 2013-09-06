/**
 * Sagittarius - UnrealScript Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
class SagittariusLinkClient extends TcpLink;

var string TargetHost;
var int TargetPort;

/* The only class that this link client actually communicates with. In this way
 * Sagittarius.uc serves as a middleman and "masks" this class.
 */
var Sagittarius Parent;

// To avoid multiple TCP connections from overriding each other.
var bool bIsBusy;

/* Queue of connections to handle multiple requests and prevent them from overriding
 * each other. They are in FIFO order, so RequestQueue[0] is always executed next.
 */
var array<SagRequest> RequestQueue;

var SagRequest CurrentRequest;

var private string CachedResponseText;

function Initialize(Sagittarius s, string THost)
{
	Parent = s;
	TargetHost = THost $ ".appspot.com";
	TargetPort = 80;
}

/**
 * Begins the transmission process by storing a SagRequest in the
 * RequestQueue. If the client is currently serving another request, this
 * request waits in the queue until it can be taken.
 */
function TransmitRequest(SagRequest request)
{
	RequestQueue.AddItem(request);
	if (!bIsBusy)
	{
		StartTransmission();
	}
}

function StartTransmission()
{
	if (RequestQueue.Length == 0)
	{
		return;
	}
	bIsBusy = true;
	CachedResponseText = "";
	CurrentRequest = RequestQueue[0];
	RequestQueue.Remove(0, 1);
	Parent.LogDebug("Resolving: " $ TargetHost);
	Resolve(TargetHost);
}

event Resolved(IpAddr Addr)
{
	Parent.LogInfo(TargetHost $ " resolved to "$ IpAddrToString(Addr));
	Addr.Port = TargetPort;
	Parent.LogDebug("Bound to port: " $ BindPort());
	if (!Open(Addr))
	{
		Parent.LogError("Failed to open port");
	}
}

event ResolveFailed()
{
	Parent.LogError("Unable to resolve " $ TargetHost);
	// @TODO: Should return a SagResponse anyway!
}

event Opened()
{
	local string newline;
	newline = chr(13) $ chr(10);

	Parent.LogInfo("TCP connection opened for module " $ CurrentRequest.mID $ " and query " $ CurrentRequest.qID);

	SendText("POST " $ CurrentRequest.dest $ " HTTP/1.0" $ newline);
	SendText("Host: " $ TargetHost $ newline);
	SendText("User-Agent: SagittariusLinkClient/1.0" $ newline);
	SendText("Content-Type: application/x-www-form-urlencoded" $ newline);
	SendText("Content-Length: " $ Len(CurrentRequest.data) $ newline);
	SendText(newline);
	SendText(CurrentRequest.data $ newline);
	SendText(newline);
	SendText(newline);

	Parent.LogDebug("Sent text: " $ CurrentRequest.data $ " to destination " $ CurrentRequest.dest);
	Parent.LogDebug("End TCP connection");
}

event Closed()
{
	local SagResponse resp;
	Parent.LogInfo("TCP connection closed for module " $ CurrentRequest.mID $ " and query " $ CurrentRequest.qID);

	resp = new class'SagResponse';
	resp.Decode(CachedResponseText, Parent);
	Parent.OnResponseReceived(CurrentRequest.mID, CurrentRequest.qID, resp);
	bIsBusy = false;

	// Retry transmission in case there are any queued messages (if not, nothing happens)
	StartTransmission();
}

event ReceivedText(string Text)
{
	Parent.LogDebug("Received Text: " $ Text);
	CachedResponseText $= Text;
}

DefaultProperties
{
	bIsBusy=false
}