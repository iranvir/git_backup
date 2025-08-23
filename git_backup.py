import time
import subprocess
import zipfile
from pathlib import Path

repos = ['ciab.git', 'c_notes.git', 'git_backup', 'numbersandreality.git', 'rust_notes.git', 'playbooks.git', 'wsl2_labs.git' ]
timestamp = str(int(time.time()))
backup_dir = Path("nandr_backups/"+timestamp)
backup_archive = Path(f"./nandr_backups/{timestamp}.zip")
backup_dir.mkdir(parents=True)
hostname = 'www.numbersandreality.com'
user= 'git'
remote_path = '/var/lib/git/ranvir'

for repo in repos:
    repo_path = backup_dir / repo
    repo_path.mkdir()
    subprocess.call(['git','init','--bare','--quiet'], cwd=repo_path)
    ssh_url = user+'@'+hostname+':'+remote_path+'/'+repo
    subprocess.call(['git', 'fetch', '--force', '--prune', '--tags', ssh_url, "refs/heads/*:refs/heads/*"], cwd=repo_path)

with zipfile.ZipFile(backup_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in backup_dir.rglob('*'):
        relative_path = file.relative_to(backup_dir.parent)
        zipf.write(file, relative_path)
