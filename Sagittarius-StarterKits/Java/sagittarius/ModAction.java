/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class ModAction extends DelAction {

    public ModAction() {
        this.handler = "/dbmod";
    }

    public void AddModification(String field, String value, boolean encrypt) {
        request.addURLPair("m", field + "::" + value, encrypt);
    }
    
    public void AddModification(String field, String value) {
        AddModification(field, value, false);
    }
}