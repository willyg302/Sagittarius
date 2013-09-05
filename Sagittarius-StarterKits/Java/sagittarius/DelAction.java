/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class DelAction extends GetAction {

    protected boolean returnsResults;

    public DelAction() {
        this.handler = "/dbdel";
        this.returnsResults = false;
    }

    public void SetReturnsResults() {
        returnsResults = true;
    }
    
    @Override
    protected void finalizeRequest() {
        super.finalizeRequest();
        if (returnsResults) {
            request.addURLPair("rres", "true", false);
        }
    }
}