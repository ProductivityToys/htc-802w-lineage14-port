/* SPDX-License-Identifier: MIT
 * Copyright (c) 2026 zee */
/* Fixed-purpose 802w WCNSS bootstrap, ARM EABI / Linux 3.4.
 * No shell, arbitrary arguments, or filesystem writes. Runs as init. */
static unsigned char image[8*1024*1024];
static long call(long n,long a,long b,long c) {
 register long r0 __asm__("r0")=a,r1 __asm__("r1")=b,r2 __asm__("r2")=c;
 register long r7 __asm__("r7")=n;
 __asm__ volatile("svc 0" : "+r"(r0) : "r"(r1),"r"(r2),"r"(r7) : "memory");return r0;
}
static void done(long rc) {call(1,rc,0,0);for(;;){} }
static void sleep_sec(long sec) {long t[2]={sec,0},left[2];while(call(162,(long)t,(long)left,0)==-4){t[0]=left[0];t[1]=left[1];}}
void _start(void) {
 long fd,n,size=0,rc;int i;
 if(call(33,(long)"/sys/class/net/wlan0",0,0)==0)done(0);
 /* Opening the node invokes wcnss_trigger_config; reading would wait for calibration. */
 fd=call(5,(long)"/dev/wcnss_wlan",0,0);if(fd<0)done(-fd);call(6,fd,0,0);
 sleep_sec(6);
 fd=call(5,(long)"/system/lib/modules/wlan.ko",0,0);if(fd<0)done(-fd);
 while(size<(long)sizeof(image)) {n=call(3,fd,(long)(image+size),sizeof(image)-size);if(n==-4)continue;if(n<0)done(-n);if(n==0)break;size+=n;}
 call(6,fd,0,0);if(size==0||size==(long)sizeof(image))done(27);
 for(i=0;i<3;i++) {rc=call(128,(long)image,size,(long)"ioctl_debug=0");if(rc==0||rc==-17)done(0);if(rc!=-19)done(-rc);sleep_sec(2);}
 done(-rc);
}
