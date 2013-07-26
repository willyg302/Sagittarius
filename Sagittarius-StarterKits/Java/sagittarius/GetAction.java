/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.ArrayList;

public class GetAction extends Action {

    protected int resultLimit, resultOffset;
    protected ArrayList<String> filters, projections;

    public GetAction() {
        this.handler = "/dbget";
        this.filters = new ArrayList<String>();
        this.projections = new ArrayList<String>();
        this.resultLimit = 20;
        this.resultOffset = 0;
    }

    public void AddFilter(String field, String value) {
        filters.add(field + "::" + value);
    }

    public void AddProjection(String field) {
        projections.add(field);
    }

    public void SetLimit(int rl) {
        resultLimit = rl;
    }

    public void SetOffset(int ro) {
        resultOffset = ro;
    }

    public void Unique() {
        resultLimit = 1;
    }

    @Override
    public String GetURLString() {
        String str = "rlim=" + resultLimit + "&roff=" + resultOffset;
        if (!filters.isEmpty()) {
            for (int i = 0; i < filters.size(); i++) {
                str += ("&f=" + filters.get(i));
            }
        }
        if (!projections.isEmpty()) {
            for (int i = 0; i < projections.size(); i++) {
                str += ("&p=" + projections.get(i));
            }
        }
        return str;
    }
}