/*
 * OpenElm
 * GPL v3 
 * Copyright (c) 2011, Red Robot Studios Ltd
 */

package com.redrobotstudios.OpenElm;

import android.app.Activity;
import android.os.Bundle;
import com.phonegap.*;

public class OpenElm extends DroidGap
{
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        super.loadUrl("file:///android_asset/www/index.html");
    }
}

