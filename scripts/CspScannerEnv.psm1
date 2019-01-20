#!/usr/bin/pwsh

Function Test-CspsMissing {
    if (-not $env:PSGIVENS_REPOS) {
        Write-Host "Please set the $env:PSGIVENS_REPOS to the location of this repo."
        return $true
    }   
}

Function Update-CspsModule {
    if (Test-CspsMissing) { RETURN }

    $MyPSModulePath = "{0}/.local/share/powershell/Modules" -f (ls -d ~)
    mkdir -p $MyPSModulePath/CspScannerEnv
    Write-Host ("Copying {0}/cspscanner/scripts/CspScannerEnv.psm1 to {1}/CspScannerEnv/" -f $env:PSGIVENS_REPOS,  $MyPSModulePath)
    cp -f $env:PSGIVENS_REPOS/cspscanner/scripts/CspScannerEnv.psm1  $MyPSModulePath/CspScannerEnv/
    Write-Host "Force import-module CspScannerEnv"
    Import-Module -Force CspScannerEnv -Global
}

Function Initialize-CspsEnv {
    Write-Host "Creating volume 'csps-pgsql-volume'"
    docker volume create csps-pgsql-volume
    Write-Host "Creating network 'csps-net'"
    docker network create --driver bridge csps-net
}

Function Start-CspsDocker {
    param(
        [Parameter(
            Mandatory=$true, 
            HelpMessage="Containers not involved in proxy.",
            ParameterSetName="Individual")]
        [ValidateSet(
            "csps-pgsql",
            "csps-scanner"
        )] 
        [string]$Container
    )

    if (Test-CspsMissing) { RETURN }

    switch ($Container) {
        "csps-pgsql" {
            Write-Host "Starting csps-pgsql..."
            # run the database container
            # https://hub.docker.com/_/postgres/
            docker run `
                --name csps-pgsql `
                --mount source=csps-pgsql-volume,target=/var/lib/postgresql/data/pgdata `
                --network csps-net `
                --rm `
                -p 5432:5432 `
                -e POSTGRES_PASSWORD=Password1 `
                -e POSTGRES_USER=samplesam `
                -e POSTGRES_DB=defaultdb `
                -e PGDATA=/var/lib/postgresql/data/pgdata `
                -d `
                csps-pgsql        
        }
        "csps-scanner" {
            docker run `
                --name csps-scanner `
                --network csps-net `
                --rm `
                -it `
                -p 9090:9090 `
                --mount type=bind,source=$env:PSGIVENS_REPOS/cspscanner/scanner/src/,target=/app/src/ `
                csps-scanner
        }        
        default {
            Write-Host ("Start {0} is not yet implemented" -f $Container)
        }
    }
}

Function Start-CspsEnv {
<#
.SYNOPSIS
    Start necessary microservices via docker. 
.DESCRIPTION
    Starts necessary microservices, configures reverse-proxy, and configures mountebank. 
.NOTES
    Author: Phillip Scott Givens
    Date:   January 19th, 2019
#>
    param(
    )

    if (Test-CspsMissing) { RETURN }

}

Function Stop-CspsEnv {
<#
.SYNOPSIS
    Shuts down the docker containers for the environment. 
.DESCRIPTION
    Shuts down all docker containers used for the csps project.
.EXAMPLE
    Stop-CspsEnv 
    Checks if each of the known containers is running, and shutds it down. 
.NOTES
    Author: Phillip Scott Givens
    Date:   November 25th, 2018
#>
    @(  "csps-pgsql",
        "csps-scanner"
    ) | ForEach-Object {
        if (docker container list | grep $_) {
            Write-Host ("Stopping {0}" -f $_)
            docker container stop $_
        } else {
            Write-Host ("Not-running: {0}" -f $_)
        }
    }
}

Function Start-CspsPgAdmin {
<#
.SYNOPSIS
    Starts a container running pgadmin on the csps-net network. 
.DESCRIPTION
    Starts a container running pgadmin on the csps-net network. 
    Uses the following environment variables
    * PGADMIN_DEFAULT_EMAIL=user@domain.com
    * PGADMIN_DEFAULT_PASSWORD=Password1
.EXAMPLE
    Start-PgAdmin
    Starts a container running pgadmin on the csps-net network. 
.NOTES
    Author: Phillip Scott Givens
    Date:   November 25th, 2018
#>

    Write-Host "Starting csps-pgadmin..."
    # Use pgadmin to explore the database
    docker run `
        -p 5002:80 `
        --rm `
        --name csps-pgadmin `
        --network csps-net `
        -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" `
        -e "PGADMIN_DEFAULT_PASSWORD=Password1" `
        -d `
        dpage/pgadmin4
}

Function Stop-CspsPgAdmin {
<#
.SYNOPSIS
    Stops a container running pgadmin on the csps-net network. 
.DESCRIPTION
    Stops a container running pgadmin on the csps-net network. 
.EXAMPLE
    Stop-PgAdmin
    Stops a container running pgadmin on the csps-net network. 
.NOTES
    Author: Phillip Scott Givens
    Date:   November 25th, 2018
#>
    docker container stop csps-pgadmin
}

Function Connect-CspsDocker {
<#
.SYNOPSIS
    Executes /bin/sh in of the available containers for the csps project
.DESCRIPTION
    Executes /bin/sh in of the available containers for the csps project
.PARAMETER Container
    One of the valid containers for the csps project    
.EXAMPLE
    Connect-CspsDocker csps-pgsql
    Executes /bin/sh in the csps-pgsql container
.NOTES
    Author: Phillip Scott Givens
    Date:   November 25th, 2018
#>    
    param(
        [Parameter(Mandatory=$false)]
        [ValidateSet(
            "csps-pgsql", 
            "csps-scanner"
            )] 
        [string]$Container
        # ,

        # [Parameter(Mandatory=$false)]
        # [switch]$Bash
    )

    docker exec -it $Container /bin/bash
}


Function Build-CspsImage {
    <#
    .SYNOPSIS
        Builds the docker container related to the pomodor project.
    .DESCRIPTION
        Builds the docker container related to the pomodor project.
    .PARAMETER Image
        One of the valid images for the csps project
    .EXAMPLE
    .NOTES
        Author: Phillip Scott Givens
    #>    
    param(
        [Parameter(Mandatory=$false)]
        [ValidateSet(
            "csps-pgsql", 
            "csps-scanner"
            )] 
        [string]$Image
    )

    $buildpath = "{0}/cspscanner" -f $env:PSGIVENS_REPOS
    switch($Image) {
        "csps-pgsql" {
            docker build `
                -t csps-pgsql `
                -f "$buildpath/pgsql/Dockerfile" `
                "$buildpath/pgsql/"
        }
        "csps-scanner" {
            docker build `
                -t csps-scanner `
                -f "$buildpath/scanner/Dockerfile" `
                "$buildpath/scanner/"
        }
    }    
}



Function Build-CspsImages {
    param(
    )

    if (Test-CspsMissing) { RETURN }

    @(
            "csps-pgsql", 
            "csps-scanner"
    ) | ForEach-Object { Build-CspsImage -Docker $Docker -Image $_ }
}


Export-ModuleMember -Function Build-CspsImage
Export-ModuleMember -Function Build-CspsImages
Export-ModuleMember -Function Connect-CspsDocker
Export-ModuleMember -Function Initialize-CspsEnv
Export-ModuleMember -Function Start-CspsDocker
Export-ModuleMember -Function Start-CspsEnv
Export-ModuleMember -Function Start-CspsPgAdmin
Export-ModuleMember -Function Stop-CspsEnv
Export-ModuleMember -Function Stop-CspsPgAdmin
Export-ModuleMember -Function Update-CspsModule
