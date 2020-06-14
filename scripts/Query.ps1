param (
  [Parameter(Mandatory=$true)]
  [string]$query,
  [bool]$generate=$false,
  [int]$pages=2,
  [int]$limit=0,
  [string]$sort="none", 
  [bool]$ascending=$false,
  [bool]$email=$false
)
C:/.../python.exe C:/...Amazon-Bot/src/Query.py $query $generate $pages $limit $sort $ascending $email

<#
.SYNOPSIS
  Queries and retrieves product information from Amazon
.DESCRIPTION
  Queries and retrieves product information from Amazon
.PARAMETER query
  Search string to query
.PARAMETER generate
  Generates a runnable script if true
.PARAMETER pages
  Retrieves items from the first X pages
.PARAMETER limit
  Retrieves a maximum of X items
.PARAMETER sort
  Sorts items by list price, price, rating, reviews, or stock
.PARAMETER ascending
  Sorts items in ascending or descending order
.PARAMETER email
  Emails query results if true
#>