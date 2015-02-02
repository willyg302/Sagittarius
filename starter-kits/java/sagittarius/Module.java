/**
 * Sagittarius - Java Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public abstract class Module {

    protected String ID;

    public String getID() {
        return ID;
    }

    protected void SubmitAction(String QueryID, Action a) {
        a.submit(ID, QueryID);
    }
    
    public abstract void OnResponseReceived(String ActionID, SagResponse resp);
}