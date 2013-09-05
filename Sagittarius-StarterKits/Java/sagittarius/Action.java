/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public abstract class Action {

    public static final String DBTYPE = "object_type";
    public static final String DBNAME = "object_name";
    protected String handler;
    protected SagRequest request;
    
    public void submit(String ModuleID, String QueryID) {
        finalizeRequest();
        request.setModuleInfo(ModuleID, QueryID);
        request.submit();
    }
    
    public void initializeRequest(SagRequest sr) {
        sr.setDestination(handler);
        this.request = sr;
    }
    
    protected void finalizeRequest() {
        //
    }
}