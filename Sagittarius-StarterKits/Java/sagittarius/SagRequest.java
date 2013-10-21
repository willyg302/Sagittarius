/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class SagRequest {

    private String dest, data, mID, qID;
    private String delim;

    public SagRequest() {
        this.data = "";
        this.delim = "";
    }
    
    public void submit() {
        Sagittarius.getInstance().SubmitRequest(this);
    }
    
    public void addURLPair(String param, String value, boolean encryptValue) {
        if (encryptValue) {
            value = Sagittarius.getInstance().encrypt(value);
        }
        this.data += (delim + param + "=" + value);
        this.delim = "&";
    }
    
    public SagRequest setDestination(String dest) {
        this.dest = dest;
        return this;
    }
    
    public SagRequest setModuleInfo(String mID, String qID) {
        this.mID = mID;
        this.qID = qID;
        return this;
    }

    public String getDestination() {
        return dest;
    }

    public String getData() {
        return data;
    }

    public String getModuleID() {
        return mID;
    }

    public String getQueryID() {
        return qID;
    }
}