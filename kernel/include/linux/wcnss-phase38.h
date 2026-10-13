/* Diagnostic 38: read-only, source-verified PM8921/GCC/TLMM addresses. */
#include <linux/platform_device.h>
#include <linux/mfd/pm8xxx/core.h>
#include <linux/io.h>
#include <mach/msm_iomap.h>
static void wcnss_phase38(const char *phase)
{
 static const unsigned short pm[]={0xb4,0xc0,0xdc,0x1d0,0x1d2,0x009,0x1d8,0x1da,0x00a,0x1e0,0x1e2,0x00b,0x1e8,0x1ea,0x011,0x060,0x062,0x06c};
 static const unsigned short gcc[]={0x31a0,0x31a4,0x31a8,0x31ac,0x31b4,0x31b8,0x3420,0x35e0,0x3880};
 struct device *gpio;
 unsigned int i;
 int rc;
 u8 value;
 pr_info("phase38 %s BEGIN\n",phase);
 gpio=bus_find_device_by_name(&platform_bus_type,NULL,"pm8xxx-gpio");
 if(gpio && gpio->parent) {
  for(i=0;i<ARRAY_SIZE(pm);i++) {
   value=0;rc=pm8xxx_readb(gpio->parent,pm[i],&value);
   pr_info("phase38 %s PMIC %03x=%02x rc=%d\n",phase,pm[i],value,rc);
  }
 } else pr_info("phase38 %s PMIC device unavailable\n",phase);
 if(gpio) put_device(gpio);
 for(i=0;i<ARRAY_SIZE(gcc);i++)
  pr_info("phase38 %s GCC %04x=%08x\n",phase,gcc[i],readl(MSM_CLK_CTL_BASE+gcc[i]));
 for(i=64;i<=68;i++)
  pr_info("phase38 %s GPIO %u=%08x\n",phase,i,readl(MSM_TLMM_BASE+0x1000+16*i));
}
