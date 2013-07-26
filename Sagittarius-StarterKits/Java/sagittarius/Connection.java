/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class Connection {

    private boolean post;
    private String dest, data, mID, qID;

    public Connection(boolean post, String dest, String mID, String qID, String data) {
        this.post = post;
        this.dest = dest;
        this.data = data;
        this.mID = mID;
        this.qID = qID;
    }

    public boolean isPost() {
        return post;
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