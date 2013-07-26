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

    protected void SubmitAction(String ActionID, Action a) {
        parent.SubmitAction(ID, ActionID, a);
    }

    public abstract void OnTextReceived(String ActionID, String text);

    public abstract void OnCallbackReceived(String ActionID);
}