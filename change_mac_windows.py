import subprocess
import random
import re
import winreg
import time
import sys

def generate_random_mac():
    """
    Generate a random MAC address as a 12-digit hex string (without separators).
    The first byte is modified to be a locally administered, unicast address.
    """
    first_byte = random.randint(0, 255)
    # Set the locally administered bit (0x02) and clear the multicast bit (0x01)
    first_byte = (first_byte | 0x02) & 0xFE
    # Generate remaining 5 octets randomly
    mac = [first_byte] + [random.randint(0, 255) for _ in range(5)]
    # Format the MAC as a continuous hex string (e.g., "02A1B2C3D4E5")
    return ''.join(f'{byte:02X}' for byte in mac)

def get_wifi_adapter_guid(adapter_name="Wi-Fi"):
    """
    Uses WMIC to obtain the GUID (NetCfgInstanceId) of the adapter with the
    specified connection name (default is "Wi-Fi").
    """
    try:
        # This command returns something like "GUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
        output = subprocess.check_output(
            ["wmic", "nic", "where", f"NetConnectionID='{adapter_name}'", "get", "GUID", "/value"],
            shell=True,
            stderr=subprocess.DEVNULL,
            universal_newlines=True
        )
        # Extract the GUID value using a regular expression
        match = re.search(r'GUID=(\S+)', output)
        if match:
            return match.group(1).strip()
        else:
            print("Could not find adapter GUID. Ensure the adapter name is correct.")
            sys.exit(1)
    except subprocess.CalledProcessError as e:
        print("Error occurred while fetching the Wi-Fi adapter GUID:", e)
        sys.exit(1)

def update_registry_mac(new_mac, adapter_guid):
    """
    Searches for the network adapter's registry subkey (inside the class key for network adapters)
    by matching the "NetCfgInstanceId" with the Wi-Fi adapter's GUID. If found, the "NetworkAddress"
    value is set to the new MAC address.
    
    The registry path used is:
    HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Class\
        {4d36e972-e325-11ce-bfc1-08002be10318}\<subkey>
    """
    reg_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e972-e325-11ce-bfc1-08002be10318}"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS)
    except PermissionError:
        print("Permission denied. Please run the script as an administrator.")
        sys.exit(1)

    i = 0
    found = False
    # Iterate through each subkey (e.g., "0000", "0001", etc.) to find a match.
    while True:
        try:
            subkey_name = winreg.EnumKey(key, i)
            subkey = winreg.OpenKey(key, subkey_name, 0, winreg.KEY_ALL_ACCESS)
            try:
                # Read the NetCfgInstanceId value from the subkey
                instance_id, _ = winreg.QueryValueEx(subkey, "NetCfgInstanceId")
                if instance_id.lower() == adapter_guid.lower():
                    # If matching, set the NetworkAddress to the new MAC address
                    winreg.SetValueEx(subkey, "NetworkAddress", 0, winreg.REG_SZ, new_mac)
                    print(f"Updated MAC address in registry to {new_mac} for adapter with GUID {adapter_guid}")
                    found = True
                    winreg.CloseKey(subkey)
                    break
            except FileNotFoundError:
                # The key might not have the NetCfgInstanceId value; simply ignore and continue.
                pass
            winreg.CloseKey(subkey)
            i += 1
        except OSError:
            # No more subkeys available.
            break
    winreg.CloseKey(key)
    
    if not found:
        print("Could not find the registry entry for the adapter. Your adapter may not support MAC address changes via the registry.")
        sys.exit(1)

def set_interface_state(adapter_name, state="disable"):
    """
    Changes the network adapter state using the netsh command.
    state: "disable" to turn off, "enable" to turn on.
    """
    try:
        subprocess.check_call(
            ["netsh", "interface", "set", "interface", adapter_name, f"admin={state}"],
            shell=True
        )
        print(f"{adapter_name} has been set to {state}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to {state} the interface {adapter_name}:", e)
        sys.exit(1)

def main():
    # Specify your adapter's connection name here (default is "Wi-Fi")
    adapter_name = "Wi-Fi"
    
    # Step 1: Turn off (disable) the Wi-Fi adapter.
    print("Disabling the Wi-Fi adapter...")
    set_interface_state(adapter_name, "disable")
    time.sleep(2)  # Allow a short pause for the adapter to be disabled.
    
    # Step 2: Retrieve the adapter's GUID.
    wifi_guid = get_wifi_adapter_guid(adapter_name)
    print("Wi-Fi adapter GUID:", wifi_guid)
    
    # Step 3: Generate a new random MAC address.
    new_mac = generate_random_mac()
    print("Generated random MAC address:", new_mac)
    
    # Step 4: Update the registry with the new MAC address.
    update_registry_mac(new_mac, wifi_guid)
    time.sleep(2)  # Pause briefly to help ensure the registry change is processed.
    
    # Step 5: Turn the Wi-Fi adapter back on (enable it).
    print("Enabling the Wi-Fi adapter...")
    set_interface_state(adapter_name, "enable")
    
    print("Done. If the MAC address change does not take effect immediately, a system reboot may be required.")

if __name__ == "__main__":
    main()
