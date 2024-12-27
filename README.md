# ASUS Zenbook S 14 (UX5406)

## Linux Enablement Overview

| Component | Model | Status |
|-|-|-|
| [CPU](#cpu) | Intel Core Ultra 7 258V (Lunar Lake) | 6.12.5 |
| [Audio](#audio) | CS35L56/CS42L43/DMIC on SoundWire | linux-firmware-20241110 / DMIC doesn't work |
| GPU | Intel Arc Graphics 140V (PCI 8086:64a0) | 6.12 |
| Bluetooth | Intel BE201 (USB 8087:0037) | linux-firmware-20241110 |
| Wi-Fi | Intel BE201 (PCI 8086:a840) | 6.11 |
| Keyboard backlight | - | 6.11 |

TL;DR: Use `linux-mainline` (as of 2024-12).

## CPU

Patch available: https://lore.kernel.org/all/a4aa8842a3c3bfdb7fe9807710eef159cbf0e705.1731463305.git.len.brown@intel.com/ (merged in 6.13-rc2/6.12.5)

### Workaround to intermittent freezes

In case updating or patching the kernel is not an option, disable the ACPI C3 state on a random P-core:

```bash
echo 1 > /sys/devices/system/cpu/cpu0/cpuidle/state3/disable
# or
cpupower -c 0 idle-set -d 3
```

However this may increase idle power consumption. You may want to toggle it back before entering s2idle. ~~(left as an exercise to the reader)~~

## Audio

Install [sof-firmware](https://pkgs.org/search/?q=sof-lnl-cs42l43-l0-cs35l56-l23.tplg)

If there is no package for your distribution, install manually from [thesofproject/sof-bin](https://github.com/thesofproject/sof-bin)

### Headphone Jack

Works.

### Speakers

The built-in default tunings will downmix stereo to mono for all 4 speakers. Tuning files for this model is available in `linux-firmware`.

### Microphone Array (DMIC)

Does not work at all.

### Dual-boot issues

> [!NOTE]
> The latest Intel audio driver (20.42.11515.0) from Windows Update seems to have this issue fixed.

The SOF firmware will put Windows drivers to a fu*ky state: only one of every two audio sessions will have sound.

To workaround it, remove all Dolby extensions from device manager "drivers by type" view:

* `IntcOED_OemLibPath_Dolby.inf`
* `IntelStreamingExt_Dolby.inf`
* `dax3_ext_cirrus.inf`

Alternatively, disable and re-enable "Intel Smart Sound Techonology OED" in device manager each time you reboot to Windows, or with command line:

```cmd
pnputil /disable-device /deviceid "INTELAUDIO\DSP_CTLR_DEV_A828&VEN_8086&DEV_0222&SUBSYS_1E131043"
pnputil /enable-device /deviceid "INTELAUDIO\DSP_CTLR_DEV_A828&VEN_8086&DEV_0222&SUBSYS_1E131043"
```


## GPU

The open-source Intel Vulkan driver `anv` does not sound. Expect log spam and rendering errors in Vulkan applications. (and GTK4 apps)
