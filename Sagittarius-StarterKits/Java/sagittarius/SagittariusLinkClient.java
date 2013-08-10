/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.ArrayList;
import com.ning.http.client.*;
import com.ning.http.client.AsyncHttpClient.BoundRequestBuilder;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class SagittariusLinkClient {

    private String TargetHost;
    private String TargetPort;
    private Sagittarius parent;
    private boolean isBusy;
    private ArrayList<Connection> connectionQueue;
    private Connection currentConnection;
    private AsyncHttpClient c = new AsyncHttpClient();

    public SagittariusLinkClient(Sagittarius s, String THost) {
        this.parent = s;
        this.TargetHost = "http://" + THost + ".appspot.com";
        this.TargetPort = "80";
        this.connectionQueue = new ArrayList<Connection>();
        this.isBusy = false;
    }

    /**
     * Begins the transmission process by storing a connection in the
     * ConnectionQueue. If the client is currently serving another connection,
     * this connection waits in the queue until it can be taken.
     *
     * @param post - true if this is a POST request (false if it's a GET)
     * @param dest - the destination webpage on the TargetHost
     * @param mID - ID of the module that generated this transmission
     * @param qID - ID of the query/message (for callback handling)
     * @param data - the data to transmit, or the null string "" if no data is
     * specified
     */
    public void Transmit(boolean post, String dest, String mID, String qID, String data) {
        Connection conn = new Connection(post, dest, mID, qID, data);
        connectionQueue.add(conn);
        if (!isBusy) {
            StartTransmission();
        }
    }

    private void StartTransmission() {
        if (connectionQueue.isEmpty()) {
            return;
        }
        isBusy = true;
        currentConnection = connectionQueue.remove(0);
        parent.LogDebug("Resolving: " + TargetHost);
        if (currentConnection.isPost()) {
            postData();
        }
    }
    
    private void postData() {
        try {
            asyncPost();
            Sagittarius.LogInfo("TCP connection opened for module " + currentConnection.getModuleID() + " and query " + currentConnection.getQueryID());
        } catch (IOException ex) {
            Sagittarius.LogError("Connection error (is server running at " + currentConnection.getDestination() + "?): " + ex.getMessage());
        }
    }
    
    private void asyncPost() throws IOException {
        BoundRequestBuilder brb = c.preparePost(TargetHost + currentConnection.getDestination());
        String[] params = currentConnection.getData().split("&");
        for (String s : params) {
            String[] parts = s.split("=");
            brb.addParameter(parts[0], parts[1]);
        }
        brb.execute(new AsyncHandler<String>() {
            private ByteArrayOutputStream bytes = new ByteArrayOutputStream();

            @Override
            public void onThrowable(Throwable thrwbl) {
                Sagittarius.LogError("Connection error (is server running at " + currentConnection.getDestination() + "?): " + thrwbl.getMessage());
            }

            @Override
            public AsyncHandler.STATE onBodyPartReceived(HttpResponseBodyPart hrbp) throws Exception {
                bytes.write(hrbp.getBodyPartBytes());
                return STATE.CONTINUE;
            }

            @Override
            public AsyncHandler.STATE onStatusReceived(HttpResponseStatus hrs) throws Exception {
                if (hrs.getStatusCode() != 200) {
                    Sagittarius.LogError("HTTP response status not 200");
                    return STATE.ABORT;
                }
                return STATE.CONTINUE;
            }

            @Override
            public AsyncHandler.STATE onHeadersReceived(HttpResponseHeaders hrh) throws Exception {
                return STATE.CONTINUE;
            }

            @Override
            public String onCompleted() throws Exception {
                String ret = bytes.toString();
                Sagittarius.LogDebug("Sent text: " + currentConnection.getData() + " to destination " + currentConnection.getDestination());
                Sagittarius.LogDebug("End TCP connection");
                if (ret != null) {
                    String text = GetXMLValue("resp", ret);
                    Sagittarius.LogDebug("Received Text: " + text);
                    parent.OnTextReceived(currentConnection.getModuleID(), currentConnection.getQueryID(), new SagResponse(text, parent));
                }
                // In any case, our connection is done
                Sagittarius.LogInfo("TCP connection closed for module " + currentConnection.getModuleID() + " and query " + currentConnection.getQueryID());
                parent.OnCallbackReceived(currentConnection.getModuleID(), currentConnection.getQueryID());
                isBusy = false;

                // Retry transmission in case there are any queued messages (if not, nothing happens)
                StartTransmission();
                return ret;
            }
        });
    }
    
    private String GetXMLValue(String XMLTag, String text) {
        int XMLTagStart = text.indexOf("<" + XMLTag + ">");
        if (XMLTagStart < 0) {
            return "";
        }
        XMLTagStart += (XMLTag.length() + 2);
        int XMLTagEnd = text.indexOf("</" + XMLTag + ">");
        if (XMLTagEnd < XMLTagStart) {
            return "";
        }
        return text.substring(XMLTagStart, XMLTagEnd);
    }
}