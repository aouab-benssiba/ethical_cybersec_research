# Tails OS Virtual Machine Setup Guide

## Step 1: Prepare the Disk Image

1. **Download the Tails USB image** from the [official Tails website](https://tails.net/).
2. **Convert the image to VDI format** (for VirtualBox compatibility):
   ```bash
   VBoxManage convertfromraw Tails-amd64-5.1.img Tails.vdi --format vdi
```
Note: The .img file can be deleted after conversion.

Resize the VDI to accommodate the OS and persistent storage:
```bash
VBoxManage modifyhd Tails.vdi --resize 16384
```
Note: Use 8000 MB + [desired-persistent-storage-size-in-MB] as the resize value (e.g., 8000 + 8192 = 16192 for an 8 GB persistent volume).

Step 2: Configure the Virtual Machine
Virtual Machine Settings
Create a new VM in VirtualBox using the official Tails setup instructions.

Adjust the following settings:

System → Motherboard → Extended Features
☑ Enable EFI (special OSes only) (required for USB boot).

Storage

Add a USB storage controller (click the leftmost "Add Controller" icon).

Under the USB controller, attach the Tails.vdi (click the third "Add Disk" icon).

Optional: Set VM Resolution
```bash
VBoxManage setextradata <vm-name> VBoxInternal2/EfiGraphicsResolution <resolution>
```
Example:
1600x900 for a 1600x900 resolution.

Step 3: Boot Tails and Enable Persistent Storage
Start the VM.

From the boot menu, select:
Tails (External Hard Disk)
(To permanently skip the boot menu, follow this guide).

Set up the persistent volume after booting:
Applications → Tails → Configure persistent volume.
