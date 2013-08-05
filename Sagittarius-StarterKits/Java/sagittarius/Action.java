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
    private String password;
    
    public void SetPassword(String password) {
        this.password = password;
    }
    
    protected String Encrypt(String text, boolean encrypt) {
        if (encrypt) {
            text = Encryption.Encrypt(text, password);
        }
        return text;
    }

    public String GetHandler() {
        return handler;
    }

    public abstract String GetURLString();
}