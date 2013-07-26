/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.ArrayList;

public class AddAction extends Action {

    private ArrayList<String> attributes;

    public AddAction() {
        this.handler = "/dbadd";
        this.attributes = new ArrayList<String>();
    }

    public void AddAttribute(String field, String value) {
        attributes.add(field + "::" + value);
    }

    @Override
    public String GetURLString() {
        String str = "";
        String delim = "";
        for (int i = 0; i < attributes.size(); i++) {
            str += (delim + "a=" + attributes.get(i));
            delim = "&";
        }
        return str;
    }
}