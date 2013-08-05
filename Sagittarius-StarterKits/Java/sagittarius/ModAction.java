/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.ArrayList;

public class ModAction extends GetAction {

    private ArrayList<String> modifications;
    private boolean returnsResults;

    public ModAction() {
        this.handler = "/dbmod";
        this.modifications = new ArrayList<String>();
        this.returnsResults = false;
    }

    public void AddModification(String field, String value, boolean encrypt) {
        modifications.add(Encrypt(field + "::" + value, encrypt));
    }
    
    public void AddModification(String field, String value) {
        AddModification(field, value, false);
    }

    public void SetReturnsResults() {
        returnsResults = true;
    }

    @Override
    public String GetURLString() {
        String str = super.GetURLString();
        if (returnsResults) {
            str += "&rres=true";
        }
        if (!modifications.isEmpty()) {
            for (int i = 0; i < modifications.size(); i++) {
                str += ("&m=" + modifications.get(i));
            }
        }
        return str;
    }
}