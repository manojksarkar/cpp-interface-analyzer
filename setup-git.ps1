# PowerShell script to set up Git repository for C++ Interface Analyzer

Write-Host "Setting up Git repository..." -ForegroundColor Green

# Check if git is available
try {
    $gitVersion = git --version
    Write-Host "Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host "Or use GitHub Desktop: https://desktop.github.com/" -ForegroundColor Yellow
    exit 1
}

# Initialize repository
Write-Host "`nInitializing Git repository..." -ForegroundColor Cyan
git init

# Add all files
Write-Host "Adding files..." -ForegroundColor Cyan
git add .

# Check status
Write-Host "`nRepository status:" -ForegroundColor Cyan
git status

# Create initial commit
Write-Host "`nCreating initial commit..." -ForegroundColor Cyan
git commit -m "Initial commit: Phase 1 C++ Interface Analyzer MVP"

Write-Host "`n✅ Git repository initialized successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Create a repository on GitHub/GitLab/Bitbucket" -ForegroundColor White
Write-Host "2. Add remote: git remote add origin <your-repo-url>" -ForegroundColor White
Write-Host "3. Push: git branch -M main && git push -u origin main" -ForegroundColor White

