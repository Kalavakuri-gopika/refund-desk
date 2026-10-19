# PowerShell Seed Script for RefundDesk Pod
$ErrorActionPreference = "Stop"

$scriptDir = $PSScriptRoot
$podDir = Split-Path -Parent $scriptDir

Write-Host "==> Seeding RefundDesk Pod Data..." -ForegroundColor Cyan

# 1. Upload Knowledge Files
Write-Host "--> Uploading store policies and response templates..." -ForegroundColor Yellow
& lemma files upload (Join-Path $podDir "files\knowledge\store_policies.md") /knowledge/store_policies.md
& lemma files upload (Join-Path $podDir "files\knowledge\email_templates.md") /knowledge/email_templates.md

# 2. Seed Records
Write-Host "--> Importing 30-day synthetic orders..." -ForegroundColor Yellow
& lemma records import orders (Join-Path $scriptDir "orders.json")

Write-Host "--> Importing sample tickets and approval gate state..." -ForegroundColor Yellow
& lemma records import tickets (Join-Path $scriptDir "tickets.json")

Write-Host "==> Seeding complete! RefundDesk is ready for operations." -ForegroundColor Green
