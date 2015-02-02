/**
 * Sagittarius - Java Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

public class Action {

    private static final int FILTER = 0x1;
    private static final int PROJECT = 0x2;
    private static final int ADD_ATTR = 0x4;
    private static final int MOD_ATTR = 0x8;
    private static final int LIMIT = 0x10;
    private static final int OFFSET = 0x20;
    private static final int RETURNS = 0x40;
    
    private static final int GET = FILTER + PROJECT + LIMIT + OFFSET;
    private static final int ADD = ADD_ATTR;
    private static final int DEL = GET + RETURNS;
    private static final int MOD = DEL + MOD_ATTR;

    public enum ActionType {

        GET, ADD, MOD, DEL
    }
    
    public static final String DBTYPE = "object_type";
    public static final String DBNAME = "object_name";
    
    private String handler;
    private int actionType;
    private SagRequest request;
    protected int resultLimit, resultOffset;
    protected boolean returnsResults;

    public Action(ActionType type) {
        this.handler = ("/db" + type.name()).toLowerCase();
        this.request = new SagRequest().setDestination(this.handler);
        this.actionType = new int[]{GET, ADD, MOD, DEL}[type.ordinal()];
        this.resultLimit = 20;
        this.resultOffset = 0;
        this.returnsResults = false;
    }
    
    private boolean check(int checkVal) {
        boolean ret = ((actionType & checkVal) == checkVal);
        if (!ret) {
            Sagittarius.LogWarn("This action does not support that behavior! Error code: " + checkVal);
        }
        return ret;
    }

    public void submit(String ModuleID, String QueryID) {
        finalizeRequest();
        request.setModuleInfo(ModuleID, QueryID).submit();
    }

    protected void finalizeRequest() {
        if (returnsResults) {
            request.addURLPair("rres", "true", false);
        }
        if (resultLimit != 20) {
            request.addURLPair("rlim", Integer.toString(resultLimit), false);
        }
        if (resultOffset != 0) {
            request.addURLPair("roff", Integer.toString(resultOffset), false);
        }
    }

    public void AddFilter(String field, String value, boolean encrypt) {
        if (check(FILTER)) {
            request.addURLPair("f", field + "::" + value, encrypt);
        }
    }

    public void AddFilter(String field, String value) {
        AddFilter(field, value, false);
    }

    public void AddProjection(String field, boolean encrypt) {
        if (check(PROJECT)) {
            request.addURLPair("p", field + (encrypt ? "~" : ""), false);
        }
    }

    public void AddProjection(String field) {
        AddProjection(field, false);
    }

    public void SetLimit(int rl) {
        if (check(LIMIT)) {
            resultLimit = rl;
        }
    }

    public void SetOffset(int ro) {
        if (check( OFFSET)) {
            resultOffset = ro;
        }
    }

    public void Unique() {
        SetLimit(1);
    }

    public void AddAttribute(String field, String value, boolean encrypt) {
        if (check(ADD_ATTR)) {
            request.addURLPair("a", field + "::" + value, encrypt);
        }
    }

    public void AddAttribute(String field, String value) {
        AddAttribute(field, value, false);
    }

    public void SetReturnsResults() {
        if (check(RETURNS)) {
            returnsResults = true;
        }
    }

    public void AddModification(String field, String value, boolean encrypt) {
        if (check(MOD_ATTR)) {
            request.addURLPair("m", field + "::" + value, encrypt);
        }
    }

    public void AddModification(String field, String value) {
        AddModification(field, value, false);
    }
}