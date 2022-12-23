# The benchmark of file integrity check

## background

Different integrity check tools and algorithms has different performance.
So, I test some of them to find a suitable one to applied in my project.
Include:

- [cfv](https://github.com/cfv-project/cfv)
- [rhash](https://github.com/rhash/RHash)
- find ./ -type f -exec md5sum/sha1sum/sha256sum {} \; ... supported by most Linux system.

## howto

install cfv and rhash first

```shell
sudo pip3 install cfv
wget https://github.com/rhash/RHash/archive/refs/tags/v1.4.3.tar.gz
tar -xzvf v1.4.3.tar.gz
cd RHash-1.4.3/
./configure --sysconfdir=/etc --exec-prefix=/usr --enable-lib-static
sudo make install install-lib-so-link
```

then

```shell
# show total size
$ du -sh /home/sek/third-app/
184M    /home/sek/third-app/

# show files count
$ find /home/sek/third-app/ -type f |wc -l
138

# start benchmark
$ ./benchmark.py /home/sek/third-app/ > benchmark.output
```

## result

checksum files were saved in /tmp

```shell
$ ls /tmp/test-*
/tmp/test-cfv-crc.sfv               /tmp/test-rhash-btih.sfv              /tmp/test-rhash-sha224.sfv
/tmp/test-cfv-md5.sfv               /tmp/test-rhash-crc32c.sfv            /tmp/test-rhash-sha256.sfv
/tmp/test-cfv-sha1.sfv              /tmp/test-rhash-crc32.sfv             /tmp/test-rhash-sha3-224.sfv
/tmp/test-cfv-sha224.sfv            /tmp/test-rhash-ed2k.sfv              /tmp/test-rhash-sha3-256.sfv
/tmp/test-cfv-sha256.sfv            /tmp/test-rhash-edonr256.sfv          /tmp/test-rhash-sha3-384.sfv
/tmp/test-cfv-sha384.sfv            /tmp/test-rhash-edonr512.sfv          /tmp/test-rhash-sha3-512.sfv
/tmp/test-cfv-sha512.sfv            /tmp/test-rhash-gost12-256.sfv        /tmp/test-rhash-sha384.sfv
/tmp/test-find-x-sum-md5sum.sfv     /tmp/test-rhash-gost12-512.sfv        /tmp/test-rhash-sha512.sfv
/tmp/test-find-x-sum-sha1sum.sfv    /tmp/test-rhash-gost94-cryptopro.sfv  /tmp/test-rhash-snefru128.sfv
/tmp/test-find-x-sum-sha256sum.sfv  /tmp/test-rhash-gost94.sfv            /tmp/test-rhash-snefru256.sfv
/tmp/test-find-x-sum-sha384sum.sfv  /tmp/test-rhash-has160.sfv            /tmp/test-rhash-tiger.sfv
/tmp/test-find-x-sum-sha512sum.sfv  /tmp/test-rhash-md4.sfv               /tmp/test-rhash-tth.sfv
/tmp/test-rhash-aich.sfv            /tmp/test-rhash-md5.sfv               /tmp/test-rhash-whirlpool.sfv
/tmp/test-rhash-blake2b.sfv         /tmp/test-rhash-ripemd160.sfv
/tmp/test-rhash-blake2s.sfv         /tmp/test-rhash-sha1.sfv
```

and the benchmark was saved to `benchmark.output`, see [sample files here](sample-files/)

```text
test path: third-app/
# benchmark for cfv, 3 circle(s)
algorithm           seconds             filesize            
--------------------------------------------------
sha1                0.147               12695               
sha224              0.158               14903               
sha256              0.158               16007               
crc                 0.19                15259               
sha384              0.294               20423               
sha512              0.294               24839               
md5                 0.3                 11591               

# benchmark for rhash, 3 circle(s)
algorithm           seconds             filesize            
--------------------------------------------------
crc32c              0.044               9659                
edonr512            0.094               26219               
sha1                0.118               14075               
btih                0.119               14075               
aich                0.119               12971               
crc32               0.122               22895               
sha224              0.13                16283               
sha256              0.13                17387               
md4                 0.169               12971               
ed2k                0.169               12971               
edonr256            0.175               17387               
has160              0.193               14075               
blake2b             0.219               26219               
sha384              0.265               21803               
sha512              0.265               26219               
md5                 0.271               12971               
tiger               0.284               15179               
tth                 0.327               13937               
blake2s             0.342               17387               
ripemd160           0.37                14075               
sha3-224            0.457               16283               
sha3-256            0.483               17387               
sha3-384            0.621               21803               
whirlpool           0.765               26219               
sha3-512            0.883               26219               
gost12-256          1.486               17387               
gost12-512          1.487               26219               
gost94-cryptopro    2.246               17387               
gost94              2.247               17387               
snefru128           3.789               12971               
snefru256           5.675               17387               

# benchmark for find-x-sum, 3 circle(s)
algorithm           seconds             filesize            
--------------------------------------------------
sha1sum             0.298               14075               
md5sum              0.331               12971               
sha384sum           0.438               21803               
sha512sum           0.439               26219               
sha256sum           0.603               17387              
```

## conclusion

speed sort of main algorithms is

```text
crc32c >> sha1sum > crc32 > md5sum > sha384sum ~ sha512sum
```

in general, on my machine.

```shell
$ uname -a
Linux ubuntu-nas 5.4.0-135-generic #152-Ubuntu SMP Wed Nov 23 20:19:22 UTC 2022 x86_64 x86_64 x86_64 GNU/Linux

$ lsb_release -a
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 20.04.5 LTS
Release:        20.04
Codename:       focal

$ cat /proc/cpuinfo
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 151
model name      : Intel(R) Pentium(R) Gold G7400
stepping        : 5
microcode       : 0x22
cpu MHz         : 1004.211
cache size      : 6144 KB
physical id     : 0
siblings        : 4
core id         : 0
cpu cores       : 2
apicid          : 0
initial apicid  : 0
fpu             : yes
fpu_exception   : yes
cpuid level     : 32
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc cpuid aperfmperf tsc_known_freq pni pclmulqdq dtes64 monitor ds_cpl vmx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch cpuid_fault epb cat_l2 invpcid_single cdp_l2 ssbd ibrs ibpb stibp ibrs_enhanced tpr_shadow vnmi flexpriority ept vpid ept_ad fsgsbase tsc_adjust bmi1 avx2 smep bmi2 erms invpcid rdt_a rdseed adx smap clflushopt clwb intel_pt sha_ni xsaveopt xsavec xgetbv1 xsaves dtherm arat pln pts hwp hwp_notify hwp_act_window hwp_epp hwp_pkg_req umip pku ospke waitpkg gfni vaes vpclmulqdq rdpid movdiri movdir64b md_clear flush_l1d arch_capabilities
bugs            : spectre_v1 spectre_v2 spec_store_bypass swapgs eibrs_pbrsb
bogomips        : 7372.80
clflush size    : 64
cache_alignment : 64
address sizes   : 39 bits physical, 48 bits virtual
power management:
...
```
