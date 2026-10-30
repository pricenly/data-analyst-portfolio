# Publishing updates

The repository is already live at
[github.com/pricenly/data-analyst-portfolio](https://github.com/pricenly/data-analyst-portfolio).

To publish a change:

```powershell
Set-Location "E:\TEST"
git status
git add -A
git commit -m "docs: describe the change"
git push
```

Notes:

- `main` is the default branch and tracks `origin/main`.
- Generated folders (`output/`, `tableau-marketing-roi/data/`, `__pycache__/`)
  are ignored. The one committed dataset is
  `superstore-analytics/data/SampleSuperstore.csv`, because the project should
  run without a download step.
- If Git asks for a password, use a Personal Access Token with `repo` scope.
