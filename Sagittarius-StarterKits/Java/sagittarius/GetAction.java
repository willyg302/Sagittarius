/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class GetAction extends Action {

    protected int resultLimit, resultOffset;

    public GetAction() {
        this.handler = "/dbget";
        this.resultLimit = 20;
        this.resultOffset = 0;
    }

    public void AddFilter(String field, String value, boolean encrypt) {
        request.addURLPair("f", field + "::" + value, encrypt);
    }
    
    public void AddFilter(String field, String value) {
        AddFilter(field, value, false);
    }

    public void AddProjection(String field, boolean encrypt) {
        request.addURLPair("p", field + (encrypt ? "~" : ""), false);
    }
    
    public void AddProjection(String field) {
        AddProjection(field, false);
    }

    public void SetLimit(int rl) {
        resultLimit = rl;
    }

    public void SetOffset(int ro) {
        resultOffset = ro;
    }

    public void Unique() {
        resultLimit = 1;
    }
    
    @Override
    protected void finalizeRequest() {
        super.finalizeRequest();
        request.addURLPair("rlim", Integer.toString(resultLimit), false);
        request.addURLPair("roff", Integer.toString(resultOffset), false);
    }
}