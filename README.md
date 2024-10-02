# ASUS Zenbook S 14 (UX5406)

## Linux Enablement Overview

| Component | Status |
|-|-|
| [CPU](#cpu) | Intermittent freezes |
| [Bluetooth](#bluetooth) | Unreleased firmware |
| [Audio](#audio) | Literally audible |
| GPU | 6.12 |
| Wi-Fi | 6.11 |
| Keyboard backlight | 6.11 |

TL;DR: Use `linux-mainline` (as of 2024-10).

## CPU

### Workaround to intermittent freezes

Disable the ACPI C3 state on a random P-core:

```bash
echo 1 > /sys/devices/system/cpu/cpu0/cpuidle/state3/disable
# or
cpupower -c 0 idle-set -d 3
```

However this may increase idle power consumption. You may want to toggle it back before entering s2idle. ~~(left as an exercise to the reader)~~

## Bluetooth

The firmware for the onboard BE201 module is not pushed to `linux-firmware` yet. This repo provides firmware extracted from the [Windows driver](https://www.catalog.update.microsoft.com/Search.aspx?q=%206224ef1f-f878-4665-afd7-412c8425482c).

In case your module is different from mine, try firmwares from the `unsorted` directory:
  - If `ibt-00*` is requested, try firmware files with `A0`.
  - If `ibt-01*` is requested, try firmware files with `B0`.
  - All of them are accompanied by the same `ddc` file (check `dmesg`).


## Audio

Install [sof-firmware](https://pkgs.org/download/sof-firmware)

### Headphone Jack

Works.

### Speakers

Wrong channel assignment: left channel goes to both tweeters and right channel goes to both woofers. (or vice versa, I can't clearly tell which speaker is)

### Microphone Array

Does not work at all.


## GPU

The open-source Intel Vulkan driver `anv` does not sound. Expect log spam and rendering errors in Vulkan applications. (and GTK4 apps)
