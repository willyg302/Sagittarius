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
    
    private JSONObject response;
    private boolean wasSuccessful;
    private String errorMsg;
    
    public SagResponse(String text) {
        this.response = (JSONObject) JSONValue.parse(text);
        this.wasSuccessful = response.get("success").equals("y");
        this.errorMsg = (String) response.get("success");
    }
    
    public boolean wasSuccessful() {
        return wasSuccessful;
    }
    
    public String getErrorMessage() {
        return errorMsg;
    }
    
    public JSONObject getResponseObject() {
        return response;
    }
    
    public String getDBValue(String key) {
        JSONArray DBObjects = (JSONArray) response.get("dbobjects");
        if (DBObjects == null) {
            return "";
        }
        if (DBObjects.size() == 0) {
            return "";
        }
        String ret = (String) ((JSONObject) DBObjects.get(0)).get(key);
        if (ret.startsWith("~")) {
            ret = Sagittarius.getInstance().decrypt(ret);
        }
        return ret;
    }
    
    public ArrayList<String> getDBValues(String key) {
        JSONArray DBObjects = (JSONArray) response.get("dbobjects");
        ArrayList<String> ret = new ArrayList<String>();
        if (DBObjects == null) {
            return ret;
        }
        for (int i = 0; i < DBObjects.size(); i++) {
            String temp = (String) ((JSONObject) DBObjects.get(i)).get(key);
            if (temp.startsWith("~")) {
                temp = Sagittarius.getInstance().decrypt(temp);
            }
            ret.add(temp);
        }
        return ret;
    }
    
    public ArrayList<Object> getDBObjects() {
        return (JSONArray) response.get("dbobjects");
    }
}
