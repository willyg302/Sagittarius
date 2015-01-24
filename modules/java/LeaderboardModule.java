import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.Map.Entry;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import sagittarius.Handler;
import sagittarius.Module;
import sagittarius.SagRequest;
import sagittarius.SagResponse;
import sagittarius.Sagittarius;


public class LeaderboardModule extends Module {
	
	private LinkedHashMap<String, Integer> leaderboard;

	private Handler onGetHandler, onPostHandler;

	public LeaderboardModule(Sagittarius s) {
		super(s);
		this.ID = "leaderboard";
		leaderboard = new LinkedHashMap<String, Integer>();
	}
	
	public void RegisterOnLeaderboardReceivedHandler(Handler h) {
		this.onGetHandler = h;
	}
	
	public void RegisterOnPostCompleteHandler(Handler h) {
		this.onPostHandler = h;
	}
	
	/**
	 * Returns an iterator that can be used to go through the leaderboard
	 * starting from first place. Use it like so:
	 * 
	 * Iterator<Entry<String, Integer>> it = GetLeaderboard();
	 * while (it.hasNext()) {
	 *     Entry<String, Integer> next = it.next();
	 *     // ScoreID: next.getKey();
	 *     // Score: next.getValue();
	 * }
	 */
	public Iterator<Entry<String, Integer>> GetLeaderboard() {
		return leaderboard.entrySet().iterator();
	}
	
	public void QueryLeaderboard(String leaderboardName) {
		this.QueryLeaderboard(leaderboardName, 20, 0);
	}
	
	public void QueryLeaderboard(String leaderboardName, int limit, int offset) {
		SagRequest req = new SagRequest(parent).setDestination("/ldbds").setModuleInfo(ID, "getlb");
		req.addURLPair("act", "get", false);
		req.addURLPair("n", leaderboardName, false);
		req.addURLPair("rlim", Integer.toString(limit), false);
		req.addURLPair("roff", Integer.toString(offset), false);
		req.submit();
	}
	
	public void PostToLeaderboard(String leaderboardName, int score, String scoreID) {
		SagRequest req = new SagRequest(parent).setDestination("/ldbds").setModuleInfo(ID, "postlb");
		req.addURLPair("act", "post", false);
		req.addURLPair("n", leaderboardName, false);
		req.addURLPair("score", Integer.toString(score), false);
		req.addURLPair("sid", scoreID, false);
		req.submit();
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		if (ActionID.equals("getlb")) {
			if (resp.wasSuccessful()) {
				leaderboard.clear();
				JSONArray data = (JSONArray) resp.getResponseObject().get("data");
				for (int i = 0; i < data.size(); i++) {
					JSONObject obj = (JSONObject) data.get(i);
					leaderboard.put((String) obj.get("sid"), ((Number) obj.get("score")).intValue());
				}
			}
			onGetHandler.invoke();
		} else if (ActionID.equals("postlb")) {
			onPostHandler.invoke();
		}
	}
}
