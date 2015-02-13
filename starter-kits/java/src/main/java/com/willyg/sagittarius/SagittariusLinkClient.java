/**
 * Sagittarius - Java Starter Kit
 * Copyright WillyG Productions
 * @Authors: William Gaul
 */
package com.willyg.sagittarius;

import java.util.ArrayList;
import com.ning.http.client.*;
import com.ning.http.client.AsyncHttpClient.BoundRequestBuilder;
import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class SagittariusLinkClient {

    private String TargetHost;
    private boolean isBusy;
    private AsyncHttpClient ahc;

    private ArrayList<SagRequest> requestQueue;
    private SagRequest currentRequest;

    public SagittariusLinkClient(String THost) {
        this.TargetHost = "http://" + THost + ".appspot.com";
        this.requestQueue = new ArrayList<SagRequest>();
        this.ahc = new AsyncHttpClient();
        this.isBusy = false;
    }

    /**
     * Begins the transmission process by storing a SagRequest in the
     * requestQueue. If the client is currently serving another request, this
     * request waits in the queue until it can be taken.
     */
    public void TransmitRequest(SagRequest request) {
        requestQueue.add(request);
        if (!isBusy) {
            StartTransmission();
        }
    }

    private void StartTransmission() {
        if (requestQueue.isEmpty()) {
            return;
        }
        isBusy = true;
        currentRequest = requestQueue.remove(0);
        Sagittarius.LogDebug("Resolving: " + TargetHost);
        try {
            asyncPost();
            Sagittarius.LogInfo("TCP connection opened for module " + currentRequest.getModuleID() + " and query " + currentRequest.getQueryID());
        } catch (IOException ex) {
            Sagittarius.LogError("Connection error (is server running at " + currentRequest.getDestination() + "?): " + ex.getMessage());
        }
    }

    private void asyncPost() throws IOException {
        BoundRequestBuilder brb = ahc.preparePost(TargetHost + currentRequest.getDestination());
        String[] params = currentRequest.getData().split("&");
        for (String s : params) {
            String[] parts = s.split("=");
            brb.addFormParam(parts[0], parts[1]);
        }
        brb.execute(new AsyncHandler<String>() {
            private ByteArrayOutputStream bytes = new ByteArrayOutputStream();
            private String error = "";

            @Override
            public void onThrowable(Throwable thrwbl) {
                error = thrwbl.toString();
                Sagittarius.LogError("Connection error (is server running at " + currentRequest.getDestination() + "?): " + thrwbl.getMessage());
            }

            @Override
            public AsyncHandler.STATE onBodyPartReceived(HttpResponseBodyPart hrbp) throws Exception {
                bytes.write(hrbp.getBodyPartBytes());
                return STATE.CONTINUE;
            }

            @Override
            public AsyncHandler.STATE onStatusReceived(HttpResponseStatus hrs) throws Exception {
                if (hrs.getStatusCode() != 200) {
                    error = hrs.getStatusCode() + " " + hrs.getStatusText();
                    Sagittarius.LogError("HTTP response status " + error);
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
                Sagittarius.LogDebug("Sent text: " + currentRequest.getData() + " to destination " + currentRequest.getDestination());
                Sagittarius.LogDebug("End TCP connection");

                // If nothing has been returned, we know an error has occurred
                if (ret == null || ret.equals("")) {
                    ret = "{\"success\":\"" + error + "\"}";
                }
                Sagittarius.LogDebug("Received Text: " + ret);

                // In any case, our connection is done
                Sagittarius.LogInfo("TCP connection closed for module " + currentRequest.getModuleID() + " and query " + currentRequest.getQueryID());
                Sagittarius.getInstance().OnResponseReceived(currentRequest.getModuleID(), currentRequest.getQueryID(), new SagResponse(ret));
                isBusy = false;

                // Retry transmission in case there are any queued messages (if not, nothing happens)
                StartTransmission();
                return ret;
            }
        });
    }
}
