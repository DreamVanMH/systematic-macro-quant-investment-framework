@echo off
cd /d "C:\Users\yingl\Documents\New folder\OneDrive\systematic-macro-quant-investment-framework"

echo ================================ >> task_scheduler_debug.log
echo Task started at %date% %time% >> task_scheduler_debug.log
echo Current directory: %cd% >> task_scheduler_debug.log
echo BAT file location: %~dp0 >> task_scheduler_debug.log
where python >> task_scheduler_debug.log 2>&1

"C:\Program Files\Python313\python.exe" scripts\run_daily_pipeline.py >> task_scheduler_debug.log 2>&1

echo Task finished at %date% %time% >> task_scheduler_debug.log
echo ================================ >> task_scheduler_debug.log