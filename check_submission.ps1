# ----------------------------
# Pre-Submission Checker
# ----------------------------

# Config: Update these values
$repoUrl = "https://github.com/achsah01/llm-project-demo"
$pagesUrl = "https://achsah01.github.io/llm-project-demo/"
$serverEndpoint = "https://victualless-violeta-unprohibitively.ngrok-free.dev/api-endpoint"
$secret = "mysecret123"
$email = "23f3003822@ds.study.iitm.ac.in"

# Test GitHub Pages URL
Write-Host "`nTesting GitHub Pages..."
try {
    $response = Invoke-WebRequest -Uri $pagesUrl -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ GitHub Pages reachable: $pagesUrl"
    } else {
        Write-Host "❌ GitHub Pages returned status: $($response.StatusCode)"
    }
} catch {
    Write-Host "❌ GitHub Pages not reachable. $_"
}

# Test Round 1 POST
Write-Host "`nTesting Round 1 POST..."
$body1 = @{
    secret = $secret
    brief = "Pre-submission Round 1 Test"
    task = "demo-task"
    round = 1
    nonce = "check1"
    evaluation_url = "https://webhook.site/2952113c-3260-41c2-abef-b59f14777371"
} | ConvertTo-Json

try {
    $res1 = Invoke-RestMethod -Uri $serverEndpoint -Method POST -ContentType "application/json" -Body $body1
    Write-Host "✅ Round 1 POST sent successfully."
} catch {
    Write-Host "❌ Round 1 POST failed. $_"
}

# Test Round 2 POST
Write-Host "`nTesting Round 2 POST..."
$body2 = @{
    secret = $secret
    brief = "Pre-submission Round 2 Test"
    task = "demo-task"
    round = 2
    nonce = "check2"
    evaluation_url = "https://webhook.site/2952113c-3260-41c2-abef-b59f14777371"
} | ConvertTo-Json

try {
    $res2 = Invoke-RestMethod -Uri $serverEndpoint -Method POST -ContentType "application/json" -Body $body2
    Write-Host "✅ Round 2 POST sent successfully."
} catch {
    Write-Host "❌ Round 2 POST failed. $_"
}

# Check if server.py / generated_app exists
Write-Host "`nChecking generated app..."
if (Test-Path ".\generated_app\index.html") {
    Write-Host "✅ generated_app/index.html exists."
} else {
    Write-Host "❌ generated_app/index.html missing!"
}

# Check README.md
Write-Host "`nChecking README.md..."
if (Test-Path ".\README.md") {
    Write-Host "✅ README.md exists."
} else {
    Write-Host "❌ README.md missing!"
}

# Check LICENSE
Write-Host "`nChecking MIT LICENSE..."
if (Test-Path ".\LICENSE") {
    $licenseText = Get-Content .\LICENSE
    if ($licenseText -match "MIT") {
        Write-Host "✅ LICENSE is MIT."
    } else {
        Write-Host "❌ LICENSE is not MIT."
    }
} else {
    Write-Host "❌ LICENSE missing!"
}

Write-Host "`n✅ Pre-submission check complete!"
