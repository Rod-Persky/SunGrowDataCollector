
Param (
    [string]$SunGrowConfigFile
)

# Prompt for the stored configuration file if it is not provided
if (-not $SunGrowConfigFile) {
    $SunGrowConfigFile = Join-Path $psScriptRoot "StatsDCollector.config.ini"
}

# Load the configuration file
$INFLUX_TOKEN = ""

try {
    $INFLUX_TOKEN = $(Get-Content $SunGrowConfigFile | Select-String -Pattern "^APIToken=(.*)").Matches.Groups[1].Value
    $INFLUX_TOKEN = $INFLUX_TOKEN.Trim()
}
catch {
    Write-Error "Missing configuration file or configuration file missing APIToken. Please provide a valid configuration file."
    exit
}


$TELEGRAF_CONFIG_FILE = Join-Path $psScriptRoot "StatsDCollector.telegraf.conf"

# Set the environment variables
$env:INFLUX_TOKEN = $INFLUX_TOKEN

# Start the telegraf service
telegraf  --config-directory $psScriptRoot