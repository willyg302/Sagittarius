import sagittarius.GetAction;
import sagittarius.Handler;
import sagittarius.Module;
import sagittarius.SagResponse;
import sagittarius.Sagittarius;


public class MOTDModule extends Module {

	private String motd;
	
	private Handler handler;

	public MOTDModule(Sagittarius s) {
		super(s);
		this.ID = "motd";
	}
	
	public void RegisterOnMOTDReceivedHandler(Handler h) {
		this.handler = h;
	}

	public String GetMOTD() {
		return motd;
	}

	public void QueryMOTD() {
		GetAction ga = (GetAction)parent.CreateAction("get");
		ga.AddFilter(GetAction.DBTYPE, "motd");
		ga.AddFilter(GetAction.DBNAME, "motd", true);
		ga.AddProjection("message", true);
		ga.Unique();
		SubmitAction("motdquery", ga);
	}

	@Override
	public void OnResponseReceived(String ActionID, SagResponse resp) {
		motd = resp.getDBValue("message");
		handler.invoke();
	}
}
