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

LLVM adds SHSTK to M8, while GCC's M8 mask is identical to M7. The feature
entries here describe the GCC-derived profile, not the complete feature mask
of every compiler target. Native mappings retain each compiler's target defaults:
`-march=c86-4g-m8 -mtune=c86-4g-m8`, without a SHSTK override. The compiler-specific
difference is documented rather than changing the compiler's supported target
behavior to match this feature list. Actual shadow-stack enablement also depends
on the operating system and runtime; a compiler feature bit alone does not
establish that it is active for an application.

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

Both production JSON datasets pass their schemas, and all four JSON/schema
files match jq formatting. All four instruction profiles have been compared
with the referenced GCC masks and their generic parent requirements. With the
companion Python implementation, 61 targeted tests pass, covering identity
selection, masked features, compiler mapping boundaries, and the real M4 fixture.

Hardware evidence is from M4. M6/M7/M8 validation uses public compiler sources
and synthetic inputs. Native GCC 16.2/Clang 23.1 compile/run checks have not been
performed; source support and generated flag strings have been checked.

## Live M4 validation

A live run on 2026-11-10 used the actual `/proc/cpuinfo`, with no mocked CPU
identity, flags or detection result. All 128 processor records reported the same
HygonGenuine / family 24 / model 4 / stepping 1 identity and one common flag set.

| Check | Result |
| --- | --- |
| Upstream Archspec e62828a with its original JSON | x86_64_v3 |
| Python contribution 065d961 with JSON data from this branch | c86_4g_m4 |
| GCC version available on the host | 11.4.0 |
| Flags returned by optimization_flags("gcc", "11.4.0") | -march=x86-64-v3 -mtune=generic |
| Compile using those flags, -O2 and -Werror | Exit 0 |
| Eight-lane integer addition and floating-point FMA numerical checks | Exit 0 |
| Instruction inspection | vpaddd and vfmadd132ps present |

This checks the live detection-to-compiler-flags path and the generic fallback
on M4 hardware. It is a numerical smoke test, not a performance result or an
exhaustive ISA test. Native `-march=c86-4g-m4 -mtune=c86-4g-m4` execution with
GCC 16.2/Clang 23.1 has not been checked by this run.
