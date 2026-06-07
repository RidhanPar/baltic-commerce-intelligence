$ErrorActionPreference = 'Stop'
$python = if ($env:PYTHON) { $env:PYTHON } else { 'python' }
& $python python/generate_data.py
& $python python/run_pipeline.py
& $python -m unittest discover -s tests -v
& $python dbt/load_seeds.py
$dbt = Join-Path (Split-Path $python) 'Scripts\dbt.exe'
if (-not (Test-Path $dbt)) { $dbt = 'dbt' }
& $dbt build --project-dir dbt --profiles-dir dbt --no-partial-parse
Write-Host 'Built artifacts/dashboard.html and artifacts/finance_analysis.xlsx'
