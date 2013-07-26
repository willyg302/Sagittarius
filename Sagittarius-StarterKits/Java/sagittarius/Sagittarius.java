/**
 * Sagittarius - Java Starter Kit
 * Copyright 2013 WillyG Productions
 * @Authors: William Gaul
 */
package sagittarius;

import java.util.HashMap;
import java.io.PrintStream;

public class Sagittarius {

    private SagittariusLinkClient link;
    private HashMap<String, Module> modules;
    private static PrintStream logStream = System.out;
    private static final String LOG_TAG = "Sagittarius";

    public enum ELogLevel {

        LOG_None, LOG_Error, LOG_Warn, LOG_Info, LOG_Debug;
    }
    private static ELogLevel logLevel = ELogLevel.LOG_Debug;

    public Sagittarius(String THost, String TPort) {
        this.link = new SagittariusLinkClient(this, THost, TPort);
        this.modules = new HashMap<String, Module>();
    }

    public void RegisterModule(Module m) {
        modules.put(m.getID(), m);
    }

    public Module GetModule(String ID) {
        Module ret = modules.get(ID);
        if (ret == null) {
            LogWarn("GetModule() - module with ID " + ID + " does not exist");
        }
        return ret;
    }

    public void SubmitAction(String ModuleID, String ActionID, Action a) {
        link.Transmit(true, a.GetHandler(), ModuleID, ActionID, a.GetURLString());
    }

    /**
     * CALLBACK FUNCTIONS
     */
    public void OnTextReceived(String ModuleID, String ActionID, String text) {
        if (ModuleID.equals("builtin")) {
            BuiltInOnTextReceived(ActionID, text);
            return;
        }
        GetModule(ModuleID).OnTextReceived(ActionID, text);
    }

    public void OnCallbackReceived(String ModuleID, String ActionID) {
        if (ModuleID.equals("builtin")) {
            BuiltInOnCallbackReceived(ActionID);
            return;
        }
        GetModule(ModuleID).OnCallbackReceived(ActionID);
    }

    private void BuiltInOnTextReceived(String ActionID, String text) {
        //
    }

    private void BuiltInOnCallbackReceived(String ActionID) {
        // @TODO: Make more robust
        if (ActionID.equals("mail")) {
            LogInfo("Mail successfully sent!");
        }
    }

    /**
     * MAIL
     */
    public void SendMail(String receiver, String subject, String message, String sender) {
        String contents = "recv" + receiver + "&subj=" + subject + "&mesg=" + message;
        if (!sender.equals("")) {
            contents += ("&send=" + sender);
        }
        link.Transmit(true, "/mail", "builtin", "mail", contents);
    }

    /**
     * LOG FUNCTIONS
     */
    public static void SetLogStream(PrintStream ps) {
        logStream = ps;
    }

    public static void SetLogLevel(ELogLevel ll) {
        logLevel = ll;
    }

    private static void log(String msg, String cat, String level) {
        logStream.println("[" + cat + "] " + level + ": " + msg);
    }

    public static void LogError(String msg) {
        LogError(msg, LOG_TAG);
    }

    public static void LogError(String msg, String cat) {
        if (logLevel.ordinal() > 0) {
            log(msg, cat, "ERROR");
        }
    }

    public static void LogWarn(String msg) {
        LogWarn(msg, LOG_TAG);
    }

    public static void LogWarn(String msg, String cat) {
        if (logLevel.ordinal() > 1) {
            log(msg, cat, "WARN");
        }
    }

    public static void LogInfo(String msg) {
        LogInfo(msg, LOG_TAG);
    }

    public static void LogInfo(String msg, String cat) {
        if (logLevel.ordinal() > 2) {
            log(msg, cat, "INFO");
        }
    }

    public static void LogDebug(String msg) {
        LogDebug(msg, LOG_TAG);
    }

    public static void LogDebug(String msg, String cat) {
        if (logLevel.ordinal() > 3) {
            log(msg, cat, "DEBUG");
        }
    }

    public static String GetXMLValue(String XMLTag, String text) {
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