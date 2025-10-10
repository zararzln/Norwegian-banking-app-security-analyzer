"""Configuration settings for the analyzer"""

import os

# Output directory
OUTPUT_DIR = "output"

# Banking apps to analyze (Norwegian and Nordic banking apps)
BANKING_APPS = [
    {"name": "DNB Mobile", "package": "no.dnb.mobilbank"},
    {"name": "Nordea Mobile", "package": "com.nordea.mobiletoken"},
    {"name": "Sparebank 1", "package": "no.sparebank1.mobilbank"},
    {"name": "Handelsbanken", "package": "com.handelsbanken.mobile.android.no"},
    {"name": "Skandiabanken", "package": "no.skandiabanken.mobilbank"},
    {"name": "Bank Norwegian", "package": "no.banknorwegian.mobilbank"},
    {"name": "Storebrand Bank", "package": "no.storebrand.mobilbank"},
    {"name": "Cultura Bank", "package": "no.culturabank.mobilbank"},
    {"name": "Komplett Bank", "package": "no.komplettbank.mobilbank"},
    {"name": "Sbanken", "package": "no.sbanken.mobilbank"},
    {"name": "Danske Bank", "package": "com.danskebank.mobilebank3.no"},
    {"name": "SEB", "package": "com.seb.android.no"},
    {"name": "Santander", "package": "no.santander.mobilbank"},
    {"name": "OBOS-banken", "package": "no.obosbanken.mobilbank"},
    {"name": "Vipps", "package": "no.dnb.vipps"},
    {"name": "Swedbank Norway", "package": "com.swedbank.mobilbank.no"},
    {"name": "Nordnet", "package": "com.nordnet.android.no"},
    {"name": "Sparebanken Vest", "package": "no.sparebankenvest.mobilbank"},
    {"name": "Sparebanken Øst", "package": "no.sparebankenost.mobilbank"},
    {"name": "Sparebanken Møre", "package": "no.sparebankenmøre.mobilbank"},
    {"name": "Klarna", "package": "com.myklarnamobile"},
    {"name": "Lunar", "package": "co.lunarway.lunar"},
    {"name": "Revolut", "package": "com.revolut.revolut"},
    {"name": "N26", "package": "de.number26.android"},
    {"name": "Wise", "package": "com.wise.android"}
]


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
