# cspscanner
Tests a site for the ability to use Content Security Policy

## Getting started    

The authoritative place for starting the scanner container is in CspScannerEnv.psm1 under the Start-CspsDocker function.

### Working with Powershell

As always, I set up and tear down my environments through powershell. Since there is only one container, this is overkill at the moment. 

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

### Recording from within the docker container csps-scanner

Once in a bash shell you can start working with the scripts and with mitmproxy, which are installed. 

    cd /app/src

    # Record all traffic. CspScannerAddon will add a CSP header to all responses 
    # and auto respond to CSP report violations. 
    mitmdump -s ./CspScannerAddon.py --listen-port 9090 -w /app/src/sameorigin.dat

    mitmdump -s ./CspScannerAddon.py --listen-port 9090 -w /app/src/no-origin.dat --set csp_reports_allow_none

    # Example for exploring stackoverflow.com
    mitmdump -s ./CspScannerAddon.py --listen-port 9090 -w /app/src/with-policy.dat --set csp_reports_policy="script-src 'self'; style-src 'self'; img-src 'self' data: https://tpc.googlesyndication.com; connect-src 'self'; font-src 'self'; object-src 'self'; media-src 'self'; frame-src 'self'; child-src 'self'; frame-ancestors 'self'; default-src 'self'; report-uri /cspscannerreport", 

### Easily proxy your browser

I've created a script which uses selenium to launch firefox with proxy already set up.

    scripts/launchfirefox.py

The default page already points to mitm.it. Accept the certificat authority request. Now you can explore any page you choose. 


### Interactively work with the recorded file.

    mitmproxy -r /app/src/dumpfile.dat

    # Shows all of the 'blocked-uri' entries from the report. 
    /app/src/cspreader.py /app/src/dumpfile.dat

### Exploring the dumped files. 

    # Getting help
    ./cspreader.py --help

    # Reading the report where the report was 'sameorigin'
    ./cspreader.py ./sameorigin.dat --it --ic --data --eval --else

    # Reading the report where the report was 'sameorigin'
    ./cspreader.py ./no-origin.dat --it --ic --data --eval --else

    # Reading the report where the report was 'sameorigin'
    ./cspreader.py ./with-policy.dat --it --ic --data --eval --else



### Man in the middle certificate authority

I haven't needed this yet. 

    openssl genrsa -out ca.key 2048
    openssl req -new -x509 -key ca.key -out ca.crt
    cat ca.key ca.crt > ca.pem 
    mitmproxy --cert=ca.pem

## Action Items

I would like to make this much more automated. I would classify this as Proof of Concept. In order to get to Minimal Viable Product, it will need to 

* proxy and report with simple `docker run` commands
* load the csp from a text file
* configure the firefox with the mitmproxy CA from the launch screen
* generate a json file which cuold be read by other systems. 

Beyond MVP, I would like automation

* Spider an application through the proxy
* Authentication to be stored in a key-ring
* Sticky Session
* Potentially record and replay a session 
* Storing results in a database

## Lessons learned

* mitmproxy:clientplayback.py blows up if we have an addon which automatically responds to a request. 

