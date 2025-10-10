"""Configuration settings for the analyzer"""

import os

# Output directory
OUTPUT_DIR = "output"

# Banking apps to analyze (Norwegian and Nordic banking apps)
BANKING_APPS = {
    "DNB Mobile": "no.dnb.mobilbank",
    "Nordea Mobile": "com.nordea.mobiletoken",
    "Sparebank 1": "no.sparebank1.mobilbank",
    "Handelsbanken": "com.handelsbanken.mobile.android.no",
    "Skandiabanken": "no.skandiabanken.mobilbank",
    "Bank Norwegian": "no.banknorwegian.mobilbank",
    "Storebrand Bank": "no.storebrand.mobilbank",
    "Cultura Bank": "no.culturabank.mobilbank",
    "Komplett Bank": "no.komplettbank.mobilbank",
    "Sbanken": "no.sbanken.mobilbank",
    "Danske Bank": "com.danskebank.mobilebank3.no",
    "SEB": "com.seb.android.no",
    "Santander": "no.santander.mobilbank",
    "OBOS-banken": "no.obosbanken.mobilbank",
    "Vipps": "no.dnb.vipps",
    "Swedbank Norway": "com.swedbank.mobilbank.no",
    "Nordnet": "com.nordnet.android.no",
    "Sparebanken Vest": "no.sparebankenvest.mobilbank",
    "Sparebanken Øst": "no.sparebankenost.mobilbank",
    "Sparebanken Møre": "no.sparebankenmøre.mobilbank",
    "Klarna": "com.myklarnamobile",
    "Lunar": "co.lunarway.lunar",
    "Revolut": "com.revolut.revolut",
    "N26": "de.number26.android",
    "Wise": "com.wise.android"
}

# Protection signatures to look for
PROTECTION_SIGNATURES = {
    "Promon SHIELD": ["promon", "shield", "com.promon"],
    "Arxan": ["arxan", "guardit"],
    "Irdeto": ["irdeto", "cloakware"],
    "Verimatrix": ["verimatrix", "vcas"],
    "Inside Secure": ["insidesecure", "teegris"],
    "Root Detection": ["rootbeer", "rootdetection", "safetynet"],
    "SSL Pinning": ["pinning", "certificate", "trustmanager"],
    "Anti Debug": ["antidebug", "debugger", "ptrace"],
    "Obfuscation": ["obfuscation", "proguard", "dexguard"]
}

# Bypass test configurations
BYPASS_TESTS = {
    "root_detection": {
        "name": "Root Detection Bypass",
        "description": "Tests common root detection bypass techniques",
        "techniques": ["Magisk Hide", "RootCloak", "Frida Scripts"]
    },
    "ssl_pinning": {
        "name": "SSL Pinning Bypass", 
        "description": "Tests certificate pinning bypass methods",
        "techniques": ["Frida SSL Kill Switch", "objection", "Manual patching"]
    },
    "anti_debug": {
        "name": "Anti-Debug Bypass",
        "description": "Tests anti-debugging bypass techniques", 
        "techniques": ["ptrace patching", "Frida anti-anti-debug", "Native hooks"]
    },
    "tampering": {
        "name": "Tampering Detection Bypass",
        "description": "Tests app integrity bypass methods",
        "techniques": ["Signature bypass", "Hash modification", "Runtime patching"]
    }
}