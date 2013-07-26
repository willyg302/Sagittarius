/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class DelAction extends GetAction {

    private boolean returnsResults;

    public DelAction() {
        this.handler = "/dbdel";
        this.returnsResults = false;
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
        return str;
    }
}