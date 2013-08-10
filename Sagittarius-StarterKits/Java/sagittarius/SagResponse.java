/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.ArrayList;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.JSONValue;

public class SagResponse {
    
    private boolean wasSuccessful;
    private JSONArray DBObjects;
    private Sagittarius parent;
    
    public SagResponse(String text, Sagittarius s) {
        JSONObject temp = (JSONObject) JSONValue.parse(text);
        this.wasSuccessful = temp.get("success").equals("y");
        this.DBObjects = (JSONArray) temp.get("dbobjects");
        this.parent = s;
    }
    
    public boolean wasSuccessful() {
        return wasSuccessful;
    }
    
    public String getValue(String key) {
        if (DBObjects == null) {
            return "";
        }
        if (DBObjects.size() == 0) {
            return "";
        }
        String ret = (String) ((JSONObject) DBObjects.get(0)).get(key);
        if (ret.startsWith("~")) {
            ret = parent.decrypt(ret);
        }
        return ret;
    }
    
    public ArrayList<String> getValues(String key) {
        ArrayList<String> ret = new ArrayList<String>();
        if (DBObjects == null) {
            return ret;
        }
        for (int i = 0; i < DBObjects.size(); i++) {
            String temp = (String) ((JSONObject) DBObjects.get(i)).get(key);
            if (temp.startsWith("~")) {
                temp = parent.decrypt(temp);
            }
            ret.add(temp);
        }
        return ret;
    }
    
    public ArrayList<Object> getDBObjects() {
        return DBObjects;
    }
}
