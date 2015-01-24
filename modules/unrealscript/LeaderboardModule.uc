class LeaderboardModule extends Module;

struct LeaderboardEntry
{
	var string ScoreID;
	var int Score;
};

var array<LeaderboardEntry> Leaderboard;

delegate OnLeaderboardReceivedDelegate();
delegate OnPostCompleteDelegate();

function RegisterOnLeaderboardReceivedDelegate(delegate<OnLeaderboardReceivedDelegate> del)
{
	OnLeaderboardReceivedDelegate = del;
}

function RegisterOnPostCompleteDelegate(delegate<OnPostCompleteDelegate> del)
{
	OnPostCompleteDelegate = del;
}

function string GetScoreID(int index)
{
	return Leaderboard[index].ScoreID;
}

function int GetScore(int index)
{
	return Leaderboard[index].Score;
}

function int NumEntries()
{
	return Leaderboard.Length;
}

/**
 * Updates the leaderboard from Sagittarius.
 */
function QueryLeaderboard(string LeaderboardName, optional int limit = 20, optional int offset = 0)
{
	local SagRequest req;
	req = new class'SagRequest';
	req = req.Initialize(Parent).SetDestination("/ldbds").SetModuleInfo(ID, "getlb");
	req.AddURLPair("act", "get", false);
	req.AddURLPair("n", LeaderboardName, false);
	req.AddURLPair("rlim", string(limit), false);
	req.AddURLPair("roff", string(offset), false);
	req.Submit();
}

/**
 * Posts a new score to Sagittarius.
 */
function PostToLeaderboard(string LeaderboardName, int Score, string ScoreID)
{
	local SagRequest req;
	req = new class'SagRequest';
	req = req.Initialize(Parent).SetDestination("/ldbds").SetModuleInfo(ID, "postlb");
	req.AddURLPair("act", "post", false);
	req.AddURLPair("n", LeaderboardName, false);
	req.AddURLPair("score", string(Score), false);
	req.AddURLPair("sid", ScoreID, false);
	req.Submit();
}

function ParseLeaderboard(SagResponse resp)
{
	local int i;
	local JsonObject data;
	local LeaderboardEntry entry;
	data = resp.GetResponseObject().GetObject("data");
	for (i = 0; i < data.ObjectArray.Length; i++)
	{
		entry.ScoreID = data.ObjectArray[i].GetStringValue("sid");
		entry.Score = data.ObjectArray[i].GetIntValue("score");
		Leaderboard.AddItem(entry);
	}
}

function OnResponseReceived(string ActionID, SagResponse resp)
{
	super.OnResponseReceived(ActionID, resp);
	if (ActionID == "getlb")
	{
		if (resp.bWasSuccessful)
		{
			Leaderboard.Length = 0; // Make sure to clear the leaderboard when we get new results!
			ParseLeaderboard(resp);
		}
		OnLeaderboardReceivedDelegate();
	}
	else if (ActionID == "postlb")
	{
		OnPostCompleteDelegate();
	}
}

DefaultProperties
{
	ID="leaderboard"
}
