#! /bin/bash
#
# Called as filter-modules.sh list-of-modules Arch

# This script filters the modules into the kernel-core and kernel-modules
# subpackages.  We list out subsystems/subdirs to prune from the installed
# module directory.  What is left is put into the kernel-core package.  What is
# pruned is contained in the kernel-modules package.
#
# This file contains the default subsys/subdirs to prune from all architectures.
# If an architecture needs to differ, we source a per-arch filter-<arch>.sh file
# that contains the set of override lists to be used instead.  If a module or
# subsys should be in kernel-modules on all arches, please change the defaults
# listed here.

# Set the default dirs/modules to filter out
driverdirs="atm auxdisplay bcma bluetooth firewire fmc fpga infiniband isdn leds media memstick mfd mmc mtd nfc ntb pcmcia platform power ssb soundwire staging tty uio uwb w1"

chardrvs="mwave pcmcia"

netdrvs="appletalk can dsa hamradio ieee802154 irda ppp slip usb wireless"

ethdrvs="3com adaptec alteon amd aquantia atheros broadcom cadence calxeda chelsio cisco dec dlink emulex icplus marvell mellanox neterion nvidia oki-semi packetengines qlogic rdc renesas sfc silan sis smsc stmicro sun tehuti ti wiznet xircom"

inputdrvs="gameport tablet touchscreen"

scsidrvs="aacraid advansys aic7xxx aic94xx be2iscsi bfa bnx2i bnx2fc csiostor cxgbi esas2r fcoe fnic isci libsas lpfc megaraid mpt2sas mpt3sas mvsas pm8001 qla2xxx qla4xxx sym53c8xx_2 ufs qedf wd719x"

usbdrvs="atm image misc serial wusbcore"

fsdrvs="affs befs coda cramfs dlm ecryptfs hfs hfsplus jfs jffs2 minix ncpfs nilfs2 ocfs2 reiserfs romfs squashfs sysv ubifs ufs"

netprots="6lowpan appletalk atm ax25 batman-adv bluetooth can dccp dsa ieee802154 irda l2tp mac80211 mac802154 mpls netrom nfc rds rfkill rose sctp smc wireless"

drmdrvs="amd ast bridge gma500 i2c i915 mgag200 nouveau panel radeon"

iiodrvs="accel adc afe common dac gyro health humidity light magnetometer multiplexer orientation potentiometer potentiostat pressure temperature"

singlemods="ntb_netdev iscsi_ibft iscsi_boot_sysfs megaraid pmcraid qedi qla1280 9pnet_rdma rpcrdma nvmet-rdma nvme-rdma hid-picolcd hid-prodikeys hwa-hc hwpoison-inject target_core_user sbp_target cxgbit iw_cxgb3 iw_cxgb4 cxgb3i cxgb3i cxgb3i_ddp cxgb4i chcr chtls parport_serial regmap-sdw hid-asus"

# Grab the arch-specific filter list overrides
source ./filter-$2.sh

filter_dir() {
	filelist=$1
	dir=$2

	grep -v -e "${dir}/" ${filelist} > ${filelist}.tmp

	if [ $? -ne 0 ]
	then
		echo "Couldn't remove ${dir}.  Skipping."
	else
		grep -e "${dir}/" ${filelist} >> k-d.list
		mv ${filelist}.tmp $filelist
	fi
	
	return 0
}

filter_ko() {
	filelist=$1
	mod=$2

	grep -v -e "${mod}.ko" ${filelist} > ${filelist}.tmp

	if [ $? -ne 0 ]
	then
		echo "Couldn't remove ${mod}.ko  Skipping."
	else
		grep -e "${mod}.ko" ${filelist} >> k-d.list
		mv ${filelist}.tmp $filelist
	fi
	
	return 0
}

# Filter the drivers/ subsystems
for subsys in ${driverdirs}
do
	filter_dir $1 drivers/${subsys}
done

# Filter the networking drivers
for netdrv in ${netdrvs}
do
	filter_dir $1 drivers/net/${netdrv}
done

# Filter the char drivers
for char in ${chardrvs}
do
	filter_dir $1 drivers/char/${input}
done

# Filter the ethernet drivers
for eth in ${ethdrvs}
do
	filter_dir $1 drivers/net/ethernet/${eth}
done

# SCSI
for scsi in ${scsidrvs}
do
	filter_dir $1 drivers/scsi/${scsi}
done

# Input
for input in ${inputdrvs}
do
	filter_dir $1 drivers/input/${input}
done

# USB
for usb in ${usbdrvs}
do
	filter_dir $1 drivers/usb/${usb}
done

# Filesystems
for fs in ${fsdrvs}
do
	filter_dir $1 fs/${fs}
done

# Network protocols
for prot in ${netprots}
do
	filter_dir $1 kernel/net/${prot}
done

# DRM
for drm in ${drmdrvs}
do
	filter_dir $1 drivers/gpu/drm/${drm}
done

# Just kill sound.
filter_dir $1 kernel/sound

# Now go through and filter any single .ko files that might have deps on the
# things we filtered above
for mod in ${singlemods}
do
        filter_ko $1 ${mod}
done

# Go through our generated drivers list and remove the .ko files.  We'll
# restore them later.
for mod in `cat k-d.list`
do
	rm -rf $mod
done
