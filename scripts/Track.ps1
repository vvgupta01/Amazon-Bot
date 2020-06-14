param (
  [Parameter(Mandatory=$true)]
  [string]$url,
  [bool]$generate=$true,
  [double]$low=0,
  [double]$high=0,
  [double]$change=0,
  [int]$discount=0,
  [int]$stock=0
)
C:/.../python.exe C:/...Amazon-Bot/src/Track.py $url $generate $low $high $change $discount $stock

<#
.SYNOPSIS
  Retrieves and tracks item information from Amazon
.DESCRIPTION
  Retrieves and tracks item information from Amazon
.PARAMETER url
  Item URL to retrieve information
.PARAMETER generate
  Generates runnable script if true
.PARAMETER low
  Sends email if price is below $X
.PARAMETER high
  Sends email if price is above $X
.PARAMETER change
  Sends email if price changed by at least $X
.PARAMETER discount
  Sends email if item is at least X% off
.PARAMETER stock
  Sends email if left in stock is below X
#>
      