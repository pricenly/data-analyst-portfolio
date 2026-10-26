 # GitHub Deployment Guide
 
 Follow these step-by-step commands in your PowerShell terminal to initialize Git and publish your portfolio to GitHub under `@pricenly`.
 
 ---
 
 ## Step 1: Create a New Repository on GitHub
 
 1. Open your browser and go to: **[https://github.com/new](https://github.com/new)**
 2. Set **Repository name**: `data-analyst-portfolio` (or keep it as your main portfolio repo).
 3. Select **Public**.
 4. **Do NOT** check "Add a README file", "Add .gitignore", or "Choose a license" (we already created them locally).
 5. Click **Create repository**.
 
 ---
 
 ## Step 2: Open PowerShell in Your Project Folder
 
 Make sure your current directory is `E:\TEST`:
 
 ```powershell
 Set-Location "E:\TEST"
 ```
 
 ---
 
 ## Step 3: Initialize Git & Commit
 
 Run the following commands in order:
 
 ```powershell
 # 1. Initialize local Git repository (if not already initialized)
 git init
 
 # 2. Verify git status and check tracked files
 git status
 
 # 3. Stage all portfolio files (.gitignore will exclude heavy and unnecessary files)
 git add .
 
 # 4. Create your first commit
 git commit -m "feat: complete data analyst portfolio (SQL, Python EDA, Tableau ROI)"
 
 # 5. Rename default branch to main
 git branch -M main
 ```
 
 ---
 
 ## Step 4: Link Remote & Push
 
 Replace the URL below with your actual repository URL if different:
 
 ```powershell
 # Link your local repo to GitHub
 git remote add origin https://github.com/pricenly/data-analyst-portfolio.git
 
 # Push everything to GitHub
 git push -u origin main
 ```
 
 > **Note on Authentication:**  
 > If prompted for GitHub credentials, use your GitHub username (`pricenly`) and a **Personal Access Token (Classic)** as your password (with `repo` scope enabled). You can generate one at: `https://github.com/settings/tokens`.
 
 ---
 
 ## Step 5: Verify on GitHub
 
 1. Refresh your GitHub repository page: `https://github.com/pricenly/data-analyst-portfolio`
 2. You should see:
    - The beautifully rendered root `README.md` on the homepage.
    - Three structured folders: `sql-ecomm-funnel`, `superstore-analytics`, and `tableau-marketing-roi`.
 3. Go to your GitHub profile settings and pin this repository to your profile overview!
