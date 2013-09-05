/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class AddAction extends Action {

    public AddAction() {
        this.handler = "/dbadd";
    }

    public void AddAttribute(String field, String value, boolean encrypt) {
        request.addURLPair("a", field + "::" + value, encrypt);
    }
    
    public void AddAttribute(String field, String value) {
        AddAttribute(field, value, false);
    }
}