# ASUS Zenbook S 14 (UX5406)

## Linux Enablement Overview

| Component | Model | Status |
|-|-|-|
| [CPU](#cpu) | Intel Core Ultra 7 258V (Lunar Lake) | 6.12.5 |
| [Audio](#audio) | CS35L56/CS42L43/DMIC on SoundWire | linux-firmware-20241110 / DMIC with quirks |
| GPU | Intel Arc Graphics 140V (PCI 8086:64a0) | 6.12 |
| Bluetooth | Intel BE201 (USB 8087:0037) | linux-firmware-20241110 |
| Wi-Fi | Intel BE201 (PCI 8086:a840) | 6.11 |
| Keyboard backlight | - | 6.11 |
| [USB Type-A Port](#USB) | - | LPM may cause issues for buggy devices |
| Sensors | - | [not working](https://github.com/dantmnf/zenbook-s14-linux/issues/5) |

TL;DR: Use kernel 6.12.5 or later.

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

Install [sof-firmware](https://pkgs.org/search/?q=sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg)

If there is no package for your distribution, install manually from [thesofproject/sof-bin](https://github.com/thesofproject/sof-bin)

### Headphone Jack

Works.

### Speakers

The built-in default tunings will downmix stereo to mono for all 4 speakers. Tuning files for this model is available in `linux-firmware`.

### Microphone Array (DMIC)

Tracking in https://github.com/thesofproject/sof/issues/9759

#### Before necessary patches merged in upstream

* Replace `/usr/share/alsa/ucm2/sof-soundwire/cs42l43.conf` with latest version from https://github.com/alsa-project/alsa-ucm-conf/blob/master/ucm2/sof-soundwire/cs42l43.conf
* If you are using kernel before 6.14, use the [topology file from this repo](firmware/intel/sof-ipc4-tplg/sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg)
  - The upstream topology is for 6.14+
* Add module parameters override in `/etc/modprobe.d/ux5406-dmic.conf`
  ```
  # quirk=RT711_JD1|SOC_SDW_PCH_DMIC|SOC_SDW_CODEC_MIC
  # RT711_JD1: default quirk value
  # SOC_SDW_PCH_DMIC: force enumerate DMIC connected to PCH
  # SOC_SDW_CODEC_MIC: don't enumerate DMIC connected to SoundWire CODEC
  options snd_soc_sof_sdw quirk=0x20041
  options snd_sof_pci tplg_filename=sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg
  ```
* Kernel-side change (seems) targeted 6.15
* An [rpm .spec file](zenbook-s14-dmic.spec) is provided for Fedora Atomic desktop users.  
  Build with:
  ```
  rpmbuild -bb zenbook-s14-dmic.spec
  ```
  and install the resulting rpm with:
  ```
  sudo rpm-ostree install --force-replacefiles $HOME/rpmbuild/RPMS/$(uname -m)/zenbook-s14-dmic-*.rpm
  ```

### USB

The USB-A port supports USB 3.0 link power management (LPM), you may encounter issues with buggy devices (e.g. RTL8156).

To workaround, add `usbcore.quirks=vid:pid:k` to kernel command line (like `usbcore.quirks=0bda:8156:k`)

### Dual-boot issues

> [!NOTE]
> The latest Intel audio driver (20.42.11515.0) from Windows Update seems to have this issue fixed.

The SOF firmware will put Windows drivers to a fu*ky state: only one of every two audio sessions will have sound.


## GPU

The open-source Intel Vulkan driver `anv` does not sound. Expect log spam and rendering errors in Vulkan applications. (and GTK4 apps)
