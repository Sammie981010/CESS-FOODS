import json
import os
import shutil
from datetime import datetime
import zipfile

class DataBackupSystem:
    def __init__(self):
        self.data_files = [
            'sales.json',
            'purchases.json', 
            'payments.json',
            'orders.json'
        ]
        self.backup_dir = 'backups'
        
    def create_backup(self):
        """Create timestamped backup of all data files"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'cess_backup_{timestamp}.zip'
        backup_path = os.path.join(self.backup_dir, backup_name)
        
        with zipfile.ZipFile(backup_path, 'w') as backup_zip:
            for file in self.data_files:
                if os.path.exists(file):
                    backup_zip.write(file)
        
        return backup_path
    
    def auto_backup_on_save(self, file_path, data):
        """Backup before saving new data"""
        # Create backup
        self.create_backup()
        
        # Save data with error handling
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Save failed: {e}")
            return False
    
    def restore_backup(self, backup_file):
        """Restore from backup file"""
        try:
            with zipfile.ZipFile(backup_file, 'r') as backup_zip:
                backup_zip.extractall('.')
            return True
        except Exception as e:
            print(f"Restore failed: {e}")
            return False

# Global backup system
backup_system = DataBackupSystem()