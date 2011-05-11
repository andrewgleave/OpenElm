//
//  main.m
//  OpenElmApp
//
//  Created by Andrew on 25/01/2011.
//  Copyright 2011 Red Robot Studios Ltd. All rights reserved.
//

#import <UIKit/UIKit.h>

int main(int argc, char *argv[]) {
    
    NSAutoreleasePool * pool = [[NSAutoreleasePool alloc] init];
    int retVal = UIApplicationMain(argc, argv, nil, @"OpenElmAppAppDelegate");
    [pool release];
    return retVal;
}
