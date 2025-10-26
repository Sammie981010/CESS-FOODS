@echo off
echo Creating CESS FOODS Data Backup...

:: Create backup directory
if not exist "backups" mkdir backups

:: Create timestamped backup
set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

:: Copy all JSON files to backup
copy *.json "backups\backup_%timestamp%\"

echo Backup completed: backups\backup_%timestamp%
pause