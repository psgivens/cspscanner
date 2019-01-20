# cspscanner
Tests a site for the ability to use Content Security Policy

## Getting started    

### Working with Powershell

As always, I set up and tear down my environments through powershell. 

    $MyPSModulePath = "{0}/.local/share/powershell/Modules" -f (ls -d ~)
    mkdir -p $MyPSModulePath/CspScannerEnv
    Write-Host ("Copying {0}/cspscanner/scripts/CspScannerEnv.psm1 to {1}/CspScannerEnv/" -f $env:PSGIVENS_REPOS,  $MyPSModulePath)
    cp -f $env:PSGIVENS_REPOS/cspscanner/scripts/CspScannerEnv.psm1  $MyPSModulePath/CspScannerEnv/
    Write-Host "Force import-module CspScannerEnv"
    Import-Module -Force CspScannerEnv -Global

Explore available functions thusly    

    Get-Commands -Module CspScannerEnv

I have not yet begun to work with the database. Everything is done through the csps-scanner container. This will drop you into a bash shell for now. 

    # This exposes the container on port 9090, so start any proxies through that. 
    Start-CspsDocker -Container csps-scanner

### Working in the Docker container in Bash

Once in a bash shell you can start working with the scripts and with mitmproxy, which are installed. 

    cd /app/src

    # Record all traffic. CspScannerAddon will add a CSP header to all responses 
    # and auto respond to CSP report violations. 
    mitmdump -w /app/src/dumpfile.dat -s ./CspScannerAddon.py --listen-port 9090

    # Interactively work with the recorded file.
    mitmproxy -r /app/src/dumpfile.dat

    # Shows all of the 'blocked-uri' entries from the report. 
    /app/src/cspreader.py /app/src/dumpfile.dat

### Setup browser

This will allow you to proxy under TLS. 

1. Set your browser proxy to point to localhost:9090. 
2. Visit 'http://mitm.it' 
3. Accept the certificat authority request

### Man in the middle certificate authority

I haven't needed this yet. 

    openssl genrsa -out ca.key 2048
    openssl req -new -x509 -key ca.key -out ca.crt
    cat ca.key ca.crt > ca.pem 
    mitmproxy --cert=ca.pem

## Action Items

* Spider an application through the proxy
* Generate a report
* Make this a simple `docker pull` situation
* Add content security policy through configuration file


