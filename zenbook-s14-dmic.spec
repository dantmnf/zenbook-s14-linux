%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Name: zenbook-s14-dmic
Version: 0.1
Release: %autorelease
Summary: Patch to enable microphone in ASUS Zenbook S14

License: GPL+
URL: https://github.com/dantmnf/zenbook-s14-linux

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-BuildRoot

%description
%{summary}

%prep


%build
wget "https://raw.githubusercontent.com/alsa-project/alsa-ucm-conf/refs/heads/master/ucm2/sof-soundwire/cs42l43.conf"
wget "https://github.com/dantmnf/zenbook-s14-linux/raw/refs/heads/master/firmware/intel/sof-ipc4-tplg/sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg"
echo "\
# quirk=RT711_JD1|SOC_SDW_PCH_DMIC|SOC_SDW_CODEC_MIC
# RT711_JD1: default quirk value
# SOC_SDW_PCH_DMIC: force enumerate DMIC connected to PCH
# SOC_SDW_CODEC_MIC: don't enumerate DMIC connected to SoundWire CODEC
options snd_soc_sof_sdw quirk=0x20041
options snd_sof_pci tplg_filename=sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg\
" > ./ux5406-dmic.conf


%install
mkdir -p %{buildroot}/usr/share/alsa/ucm2/sof-soundwire
cp ./cs42l43.conf %{buildroot}/usr/share/alsa/ucm2/sof-soundwire/
mkdir -p %{buildroot}/lib/firmware/intel/sof-ipc4-tplg
cp ./sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg %{buildroot}/lib/firmware/intel/sof-ipc4-tplg/
mkdir -p %{buildroot}/etc/modprobe.d
cp ./ux5406-dmic.conf %{buildroot}/etc/modprobe.d/


%files
/usr/share/alsa/ucm2/sof-soundwire/cs42l43.conf
/lib/firmware/intel/sof-ipc4-tplg/sof-lnl-cs42l43-l0-cs35l56-l23-2ch.tplg
/etc/modprobe.d/ux5406-dmic.conf


%changelog
%autochangelog
