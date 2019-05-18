param(
    # Parameter help description
    [Parameter(Mandatory=$true,HelpMessage="Subscription ID to deploy to")]
    [string]
    $SubscriptionID,
    # Parameter help description
    [Parameter(Mandatory=$true,HelpMessage="Resource Group to deploy to")]
    [string]
    $ResourceGroupName,
    # Parameter help description
    [Parameter(Mandatory=$false,"Region to deploy to")]
    [string]
    $Region = "eastus2",
    # Parameter help description
    [Parameter(Mandatory=$false,"Name of CosmosDB")]
    [string]
    $ResourceName = "rddt-discordbot-CosmoDB",
    # Parameter help description
    [Parameter(Mandatory=$false,"Name of Collection")]
    [string]
    $CollectionName = "RDDTDiscordBot"
)
Import-Module Az
Connect-AzAccount
$locations = @(@{"locationName"="$($region)"; "failoverPriority"=0})
