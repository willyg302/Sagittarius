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

    public String GetHandler() {
        return handler;
    }

    public abstract String GetURLString();
}