#! /bin/bash

# This is the armv7hl override file for the core/drivers package split.  The
# module directories listed here and in the generic list in filter-modules.sh
# will be moved to the resulting kernel-modules package for this arch.
# Anything not listed in those files will be in the kernel-core package.
#
# Please review the default list in filter-modules.sh before making
# modifications to the overrides below.  If something should be removed across
# all arches, remove it in the default instead of per-arch.

driverdirs="atm auxdisplay bcma bluetooth firewire fmc infiniband isdn media memstick message mwave nfc ntb pcmcia platform ssb staging tty uio uwb w1"

ethdrvs="3com adaptec alteon altera amd atheros broadcom cadence chelsio cisco dec dlink emulex icplus mellanox micrel myricom natsemi neterion nvidia oki-semi packetengines qlogic rdc renesas sfc silan sis sun tehuti via wiznet xircom"

drmdrvs="amd armada bridge ast exynos etnaviv hisilicon i2c imx meson mgag200 msm omapdrm panel nouveau radeon rockchip sti sun4i tegra tilcdc tinydrm via vc4"

singlemods="ntb_netdev iscsi_ibft iscsi_boot_sysfs megaraid pmcraid qedi qla1280 9pnet_rdma rpcrdma nvmet-rdma nvme-rdma hid-picolcd hid-prodikeys hwa-hc hwpoison-inject target_core_user sbp_target cxgbit iw_cxgb3 iw_cxgb4 cxgb3i cxgb3i cxgb3i_ddp cxgb4i chcr bq27xxx_battery_hdq"
