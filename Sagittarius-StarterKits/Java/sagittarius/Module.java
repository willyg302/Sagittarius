/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public abstract class Module {

    protected String ID;
    protected Sagittarius parent;

    public Module(Sagittarius s) {
        this.parent = s;
    }

    public String getID() {
        return ID;
    }

    protected void SubmitAction(String QueryID, Action a) {
        a.submit(ID, QueryID);
    }
    
    public abstract void OnResponseReceived(String ActionID, SagResponse resp);
}