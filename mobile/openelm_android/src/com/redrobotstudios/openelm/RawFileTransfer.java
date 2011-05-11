/*
 * RawFileTransfer
 * Based on PhoneGap's FileUpload plugin class
 * Copyright (c) 2011, Red Robot Studios
 * Copyright (c) 2005-2010, Nitobi Software Inc.
 * Copyright (c) 2010, IBM Corporation
 */
package com.redrobotstudios.OpenElm;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.Iterator;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLException;
import javax.net.ssl.SSLSession;
import javax.net.ssl.SSLSocketFactory;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import android.net.Uri;
import android.util.Log;
import android.webkit.CookieManager;

import com.phonegap.api.Plugin;
import com.phonegap.api.PluginResult;

public class RawFileTransfer extends Plugin {
    
    private static final String LOG_TAG = "RawFileTransfer";
    
    public static int FILE_NOT_FOUND_ERR = 1;
    public static int INVALID_URL_ERR = 2;
    public static int CONNECTION_ERR = 3;
    
    private SSLSocketFactory defaultSSLSocketFactory = null;
    private HostnameVerifier defaultHostnameVerifier = null;
    
    /* (non-Javadoc)
    * @see com.phonegap.api.Plugin#execute(java.lang.String, org.json.JSONArray, java.lang.String)
    */
    @Override
    public PluginResult execute(String action, JSONArray args, String callbackId) {
        String filePath = null;
        String serverUri = null;
        String mimeType = null;
        String method = null;
        try {
            filePath = args.getString(0);
            serverUri = args.getString(1);
            mimeType = args.getString(2);
            method =  args.getString(3);
        }
        catch (JSONException e) {
            Log.d(LOG_TAG, "Missing file path, server uri, mime type or method");
            return new PluginResult(PluginResult.Status.JSON_EXCEPTION, "Missing file path, server uri, mime type or method");
        }
        
        try {
            boolean trustEveryone = false;
            
            if (action.equals("upload")) {
                upload(filePath, serverUri, mimeType, method, trustEveryone);
                Log.d(LOG_TAG, "****** About to return a result from upload");
                return new PluginResult(PluginResult.Status.OK);
            } else {
                return new PluginResult(PluginResult.Status.INVALID_ACTION);
            }
        } catch (FileNotFoundException e) {
            Log.e(LOG_TAG, e.getMessage(), e);
            JSONObject error = createRawFileTransferError(FILE_NOT_FOUND_ERR);
            return new PluginResult(PluginResult.Status.IO_EXCEPTION, error);
        } catch (IllegalArgumentException e) {
            Log.e(LOG_TAG, e.getMessage(), e);
            JSONObject error = createRawFileTransferError(INVALID_URL_ERR);
            return new PluginResult(PluginResult.Status.IO_EXCEPTION, error);
        } catch (SSLException e) {
            Log.e(LOG_TAG, e.getMessage(), e);
            Log.d(LOG_TAG, "Got my ssl exception!!!");
            JSONObject error = createRawFileTransferError(CONNECTION_ERR);
            return new PluginResult(PluginResult.Status.IO_EXCEPTION, error);
        } catch (IOException e) {
            Log.e(LOG_TAG, e.getMessage(), e);
            JSONObject error = createRawFileTransferError(CONNECTION_ERR);
            return new PluginResult(PluginResult.Status.IO_EXCEPTION, error);
        }
    }
    
    // always verify the host - don't check for certificate
    final static HostnameVerifier DO_NOT_VERIFY = new HostnameVerifier() {
        public boolean verify(String hostname, SSLSession session) {
            return true;
        }
    };
    
    /**
     * This function will install a trust manager that will blindly trust all SSL
     * certificates.  The reason this code is being added is to enable developers
     * to do development using self signed SSL certificates on their web server.
     *
     * The standard HttpsURLConnection class will throw an exception on self
     * signed certificates if this code is not run.
     */
    private void trustAllHosts() {
        // Create a trust manager that does not validate certificate chains
        TrustManager[] trustAllCerts = new TrustManager[] { new X509TrustManager() {
            public java.security.cert.X509Certificate[] getAcceptedIssuers() {
                return new java.security.cert.X509Certificate[] {};
            }
            
            public void checkClientTrusted(X509Certificate[] chain,
                            String authType) throws CertificateException {
            }
            
            public void checkServerTrusted(X509Certificate[] chain,
                            String authType) throws CertificateException {
            }
        } };
        
        // Install the all-trusting trust manager
        try {
            // Backup the current SSL socket factory
            defaultSSLSocketFactory = HttpsURLConnection.getDefaultSSLSocketFactory();
            // Install our all trusting manager
            SSLContext sc = SSLContext.getInstance("TLS");
            sc.init(null, trustAllCerts, new java.security.SecureRandom());
            HttpsURLConnection.setDefaultSSLSocketFactory(sc.getSocketFactory());
        } catch (Exception e) {
            Log.e(LOG_TAG, e.getMessage(), e);
        }
    }
    
    /**
     * Create an error object based on the passed in errorCode
     * @param errorCode     the error
     * @return JSONObject containing the error
     */
    private JSONObject createRawFileTransferError(int errorCode) {
        JSONObject error = null;
        try {
            error = new JSONObject();
            error.put("code", errorCode);
        } catch (JSONException e) {
            Log.e(LOG_TAG, e.getMessage(), e);
        }
        return error;
    }
    
    /**
     * Convenience method to read a parameter from the list of JSON args.
     * @param args          the args passed to the Plugin
     * @param position      the position to retrieve the arg from
     * @param defaultString the default to be used if the arg does not exist
     * @return String with the retrieved value
     */
    private String getArgument(JSONArray args, int position, String defaultString) {
        String arg = defaultString;
        if(args.length() >= position) {
            arg = args.optString(position);
            if (arg == null || "null".equals(arg)) {
                arg = defaultString;
            }
        }
        return arg;
    }
    
    /**
     * Uploads the specified file to the server URL provided using raw HTTP request.
     * @param filePath      Full path of the file on the file system
     * @param serverUri        URL of the server to receive the file
     * @param mimeType      Describes file content type
     * @param method        HTTP method
     */
    public void upload(String filePath, String serverUri, final String mimeType,
        final String method, boolean trustEveryone) throws IOException, SSLException {
        // Create return object
        
        // Get a input stream of the file on the phone
        InputStream fileInputStream = getPathFromUri(filePath);
        
        HttpURLConnection conn = null;
        DataOutputStream dos = null;
        
        int bytesRead, bytesAvailable, bufferSize;
        long totalBytes;
        byte[] buffer;
        int maxBufferSize = 8096;
        
        //------------------ CLIENT REQUEST
        // open a URL connection to the server
        URL url = new URL(serverUri);
        
        // Open a HTTP connection to the URL based on protocol
        if (url.getProtocol().toLowerCase().equals("https")) {
            // Using standard HTTPS connection. Will not allow self signed certificate
            if (!trustEveryone) {
                conn = (HttpsURLConnection) url.openConnection();
            }
            // Use our HTTPS connection that blindly trusts everyone.
            // This should only be used in debug environments
            else {
                // Setup the HTTPS connection class to trust everyone
                trustAllHosts();
                HttpsURLConnection https = (HttpsURLConnection) url.openConnection();
                // Save the current hostnameVerifier
                defaultHostnameVerifier = https.getHostnameVerifier();
                // Setup the connection not to verify hostnames
                https.setHostnameVerifier(DO_NOT_VERIFY);
                conn = https;
            }
        }
        // Return a standard HTTP conneciton
        else {
            conn = (HttpURLConnection) url.openConnection();
        }
        
        // Allow Inputs
        conn.setDoInput(true);
        
        // Allow Outputs
        conn.setDoOutput(true);
        
        // Don't use a cached copy.
        conn.setUseCaches(false);
        
        conn.setRequestMethod(method);
        conn.setRequestProperty("Connection", "Keep-Alive");
        conn.setRequestProperty("Content-Type", mimeType);
        
        // Set the cookies on the response
        String cookie = CookieManager.getInstance().getCookie(serverUri);
        if (cookie != null) {
            conn.setRequestProperty("Cookie", cookie);
        }
        
        dos = new DataOutputStream( conn.getOutputStream() );
        
        
        // create a buffer of maximum size
        bytesAvailable = fileInputStream.available();
        bufferSize = Math.min(bytesAvailable, maxBufferSize);
        buffer = new byte[bufferSize];
        
        bytesRead = fileInputStream.read(buffer, 0, bufferSize);
        totalBytes = 0;
        
        while (bytesRead > 0) {
            totalBytes += bytesRead;
            dos.write(buffer, 0, bufferSize);
            bytesAvailable = fileInputStream.available();
            bufferSize = Math.min(bytesAvailable, maxBufferSize);
            bytesRead = fileInputStream.read(buffer, 0, bufferSize);
        }
        
        // close streams
        fileInputStream.close();
        dos.flush();
        dos.close();
        
        //------------------ read the SERVER RESPONSE
        StringBuffer responseString = new StringBuffer("");
        DataInputStream inStream;
        try {
            inStream = new DataInputStream ( conn.getInputStream() );
        } catch(FileNotFoundException e) {
            throw new IOException("Received error from server");
        }
        
        String line;
        while (( line = inStream.readLine()) != null) {
            responseString.append(line);
        }
        Log.d(LOG_TAG, "got response from server");
        Log.d(LOG_TAG, responseString.toString());
        
        inStream.close();
        conn.disconnect();
        
        // Revert back to the proper verifier and socket factories
        if (trustEveryone && url.getProtocol().toLowerCase().equals("https")) {
            ((HttpsURLConnection)conn).setHostnameVerifier(defaultHostnameVerifier);
            HttpsURLConnection.setDefaultSSLSocketFactory(defaultSSLSocketFactory);
        }
    }
    
    /**
     * Get an input stream based on file path or content:// uri
     *
     * @param path
     * @return an input stream
     * @throws FileNotFoundException
     */
    private InputStream getPathFromUri(String path) throws FileNotFoundException {
        if (path.startsWith("content:")) {
            Uri uri = Uri.parse(path);
            return ctx.getContentResolver().openInputStream(uri);
        }
        else {
            return new FileInputStream(path);
        }
    }

}