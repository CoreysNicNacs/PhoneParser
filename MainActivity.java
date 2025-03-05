package com.example.wifigeolocation;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.net.wifi.WifiManager;
import android.net.wifi.ScanResult;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.os.Bundle;
import android.widget.Toast;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import org.json.JSONArray;
import org.json.JSONObject;
import java.util.List;

public class MainActivity extends AppCompatActivity {
    private WifiManager wifiManager;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        wifiManager = (WifiManager) getApplicationContext().getSystemService(Context.WIFI_SERVICE);

        // Check and request necessary permissions
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
        } else {
            // Enable Wi-Fi if disabled
            if (!wifiManager.isWifiEnabled()) {
                wifiManager.setWifiEnabled(true);
                Toast.makeText(this, "Wi-Fi Enabled", Toast.LENGTH_SHORT).show();
            }
            // Start scanning for Wi-Fi networks
            startWifiScan();
        }
    }

    private void startWifiScan() {
        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION}, 1);
            return;
        }

        wifiManager.startScan();
        List<ScanResult> scanResults = wifiManager.getScanResults();
        JSONArray wifiNetworks = new JSONArray();
        for (ScanResult result : scanResults) {
            JSONObject network = new JSONObject();
            try {
                network.put("ssid", result.SSID);
                network.put("bssid", result.BSSID);
                network.put("rssi", result.level);
            } catch (Exception e) {
                e.printStackTrace();
            }
            wifiNetworks.put(network);
        }
        sendGeolocationRequest(wifiNetworks);
    }

    private void sendGeolocationRequest(JSONArray wifiNetworks) {
        String apiKey = "YOUR_WIFI_LOCATION_API_KEY";
        String url = "https://api.wifilocationservice.com/geolocate";

        JSONObject requestBody = new JSONObject();
        try {
            requestBody.put("networks", wifiNetworks);
            requestBody.put("key", apiKey);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Use Volley to send the request
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, requestBody,
            response -> {
                // Handle the response
                try {
                    JSONObject location = response.getJSONObject("location");
                    double latitude = location.getDouble("lat");
                    double longitude = location.getDouble("lng");
                    System.out.println("Latitude: " + latitude + ", Longitude: " + longitude);
                } catch (Exception e) {
                    e.printStackTrace();
                }
            },
            error -> {
                // Handle the error
                error.printStackTrace();
            }
        );
        // Add the request to the RequestQueue
        RequestQueue requestQueue = Volley.newRequestQueue(this);
        requestQueue.add(jsonObjectRequest);
    }

    @Override
    public void onRequestPermissionsResult(int request