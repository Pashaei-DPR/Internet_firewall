
import subprocess
import ctypes
import sys

def is_admin():
    """run as administrative """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restrict_internet():
    """Block all outbound traffic except for specified applications."""
    print("Configuring firewall to block outbound traffic...")
    
    try:
        # 1. Block all outbound traffic by default
        subprocess.run(
            ["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "allowinbound,blockoutbound"], 
            check=True, stdout=subprocess.DEVNULL
        )
        
        # Allowed applications paths
        
        allowed_apps = {
            "Allow_v2rayN_GUI": r"C:\Users\DPR\Desktop\files\soft\v2rayN-windows-64\v2rayN.exe",
            "Allow_v2rayN_Xray": r"C:\Users\DPR\Desktop\files\soft\v2rayN-windows-64\bin\Xray\xray.exe",
            "Allow_v2rayN_v2ray": r"C:\Users\DPR\Desktop\files\soft\v2rayN-windows-64\bin\v2ray\v2ray.exe",
            "Allow_Chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "Allow_vscode": r"C:\Users\DPR\AppData\Local\Programs\Microsoft VS Code\Code.exe"
        }

        for rule_name, app_path in allowed_apps.items():
            print(f"Creating allow rule for: {rule_name}")

            subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            subprocess.run([
                "netsh", "advfirewall", "firewall", "add", "rule",
                f"name={rule_name}",
                "dir=out",
                "action=allow",
                f"program={app_path}",
                "enable=yes"
            ], check=True, stdout=subprocess.DEVNULL)

        print("Done")

    except subprocess.CalledProcessError as e:
        print(f"Erro: {e}")

def restore_internet():
    """Restore firewall settings to default (allow all outbound traffic)."""
    print("Restoring internet settings to default...")
    try:
        subprocess.run(
            ["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "allowinbound,allowoutbound"], 
            check=True, stdout=subprocess.DEVNULL
        )
        
        rules_to_delete = [
            "Allow_v2rayN_GUI",
            "Allow_v2rayN_Xray",
            "Allow_v2rayN_v2ray",
            "Allow_Chrome",
            "Allow_vscode"
        ]
        
        for rule_name in rules_to_delete:
            subprocess.run(
                ["netsh", "advfirewall", "firewall", "delete", "rule", f"name={rule_name}"], 
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        
        print("Restored")
    except subprocess.CalledProcessError as e:
        print(f" Error restoring settings: {e}")


if __name__ == "__main__":
    if not is_admin():
        print("Error: This script requires Administrator privileges to modify firewall settings.")
        print("Please run your Command Prompt or IDE as Administrator.")
        sys.exit(1)

    print("Created by Dread Pirate Roberts")
    print("Select an option:")
    print("1. Restrict internet (Allow ONLY Chrome and v2rayN)")
    print("2. Restore internet (Allow ALL applications)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == '1':
        restrict_internet()
    elif choice == '2':
        restore_internet()
    else:
        print("Invalid choice. Exiting.")
