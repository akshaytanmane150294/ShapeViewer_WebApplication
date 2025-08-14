import os
import subprocess
import tempfile
import shutil

def install_plugin_from_github(url, plugin_name):
    plugins_dir = os.path.join(os.path.dirname(__file__), '..', 'plugins')
    os.makedirs(plugins_dir, exist_ok=True)
    target = os.path.join(plugins_dir, plugin_name)

    if os.path.exists(target):
        return False, f"Plugin '{plugin_name}' already exists."

    with tempfile.TemporaryDirectory() as tmp:
        subprocess.check_call(['git', 'clone', url, tmp])
        if not os.path.exists(os.path.join(tmp, 'plugin.py')):
            return False, "plugin.py not found"
        shutil.copytree(tmp, target)
        return True, f"Installed {plugin_name}"
