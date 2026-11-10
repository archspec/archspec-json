# Hygon C86-4G targets

These entries represent compiler targets. They do not claim that every physical
CPU implementation has exactly the same complete ISA as a compiler feature mask.

| Archspec target | Parent | Vendor / decimal family / model | Compiler name |
| --- | --- | --- | --- |
| c86_4g_m4 | x86_64_v3 | HygonGenuine / 24 / 4 | c86-4g-m4 |
| c86_4g_m6 | x86_64_v3 | HygonGenuine / 24 / 6 | c86-4g-m6 |
| c86_4g_m7 | x86_64_v4 | HygonGenuine / 24 / 7 | c86-4g-m7 |
| c86_4g_m8 | x86_64_v4 | HygonGenuine / 24 / 8 | c86-4g-m8 |

## Identity and ISA sources

[GCC 16.2.0 cpuinfo.h](https://github.com/gcc-mirror/gcc/blob/releases/gcc-16.2.0/gcc/common/config/i386/cpuinfo.h)
and [LLVM 23.1.0 Host.cpp](https://github.com/llvm/llvm-project/blob/llvmorg-23.1.0/llvm/lib/TargetParser/Host.cpp)
provide all four family/model mappings.

The modeled instruction profile follows the `PTA_C86_4G_M*` masks in
[GCC 16.2.0 i386.h](https://github.com/gcc-mirror/gcc/blob/releases/gcc-16.2.0/gcc/config/i386/i386.h).
M6 aliases M4; M8 aliases M7. The entries explicitly include their generic parent
requirements, since Archspec does not implicitly inherit feature sets.
GCC's AVX-VNNI and VP2INTERSECT features are included in M7 and M8.

Names follow Linux flags: SSE3 is `pni`, 64-bit mode is `lm`, FXSR is `fxsr`,
BMI is `bmi1`, SHA is `sha_ni`, PRFCHW is `3dnowprefetch`, PCLMUL is `pclmulqdq`,
and LZCNT/ABM are represented by `abm`. AVX-512 names follow the existing
Archspec/Linux convention, including `avx512_vnni` and `avx512_vp2intersect`.

LLVM adds SHSTK to M8, while GCC's M8 mask is identical to M7. This contribution
uses the GCC instruction profile rather than inferring a hardware union from
different compiler models. The native Clang M8 mapping explicitly uses
`-mno-shstk` so its defaults do not enable the unmodeled LLVM-only feature.
This preserves the M8 compiler target and scheduling model. It is not a claim
that M8 hardware lacks shadow-stack support. Representing that additional
capability and its OS availability is left for review rather than silently
claiming it was validated. The other LLVM/GCC differences are recorded here;
compiler masks are not independent hardware measurements.

## Compiler ranges

All four names appear in the GCC 16.2.0 target registry and LLVM 23.1.0 parser;
the inspected GCC 16.1.0 and LLVM 22.1.0 registries do not contain them.

The native mappings start at GCC 16.2 and Clang 23.1. Earlier releases use the
existing generic parent mappings. Entries use descending lower bounds and the
existing first-match behavior: native target first, modern generic level next,
then older explicit feature flags. Open upper bounds avoid gaps for patch
releases. Backports that add support earlier can still use the generic fallback.
Other compiler entries are copied from the existing generic parents, without
adding HCC/HGCC integration or claiming new vendor compiler validation.

## Evidence and validation boundary

The Linux fixture `linux-ubuntu22.04-c86_4g_m4` is a real first-processor record
from an M4 host: vendor HygonGenuine, family 24, model 4, stepping 1.
The available machine's CPUID.1 EAX was recorded as `0x00900f41`.
No raw M6/M7/M8 hardware captures are included. Those targets are source-backed
and have synthetic Python integration tests; synthetic records are not fixtures
claimed to come from physical hardware.

The preceding framework/schema prototype passed 686 tests. The four production
entries, this fixture, compiler mappings and their new integration tests have
not been run through a new validation pass. Native GCC 16.2/Clang 23.1 compile/run
checks and M6/M7/M8 hardware checks have not been performed. These changes are
submitted for draft review with these limits explicit.
