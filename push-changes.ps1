# PowerShell script to commit and push changes

Write-Host "Committing and pushing changes..." -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or use VS Code Source Control panel or GitHub Desktop" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repo
if (-not (Test-Path .git)) {
    Write-Host "Initializing Git repository..." -ForegroundColor Cyan
    git init
    git add .
    git commit -m "Initial commit: Phase 1 C++ Interface Analyzer MVP"
} else {
    Write-Host "Adding all changes..." -ForegroundColor Cyan
    git add .
    
    Write-Host "Checking status..." -ForegroundColor Cyan
    git status
    
    Write-Host "`nEnter commit message (or press Enter for default):" -ForegroundColor Yellow
    $commitMsg = Read-Host
    if ([string]::IsNullOrWhiteSpace($commitMsg)) {
        $commitMsg = "Update: Add testing guides and documentation"
    }
    
    Write-Host "Committing changes..." -ForegroundColor Cyan
    git commit -m $commitMsg
}

# Check for remote
$remote = git remote -v
if ([string]::IsNullOrWhiteSpace($remote)) {
    Write-Host "`n⚠️  No remote repository configured" -ForegroundColor Yellow
    Write-Host "`nTo add a remote and push:" -ForegroundColor Cyan
    Write-Host "1. Create a repository on GitHub/GitLab/Bitbucket" -ForegroundColor White
    Write-Host "2. Run: git remote add origin <your-repo-url>" -ForegroundColor White
    Write-Host "3. Run: git branch -M main" -ForegroundColor White
    Write-Host "4. Run: git push -u origin main" -ForegroundColor White
    Write-Host "`nOr use VS Code Source Control panel to publish" -ForegroundColor White
} else {
    Write-Host "`nRemote configured:" -ForegroundColor Green
    Write-Host $remote
    
    Write-Host "`nPushing to remote..." -ForegroundColor Cyan
    $branch = git branch --show-current
    if ([string]::IsNullOrWhiteSpace($branch)) {
        git branch -M main
        $branch = "main"
    }
    
    Write-Host "Pushing branch: $branch" -ForegroundColor Cyan
    git push -u origin $branch
    
    Write-Host "`n✅ Changes pushed successfully!" -ForegroundColor Green
}

