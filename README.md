[![](https://github.com/archspec/archspec-json/workflows/JSON%20Validation/badge.svg)](https://github.com/archspec/archspec-json/actions)

# Archspec-json

The [archspec-json](https://github.com/archspec/archspec-json) repository is part of the
[Archspec](https://github.com/archspec) project. It contains data on various architectural
aspects of a platform stored in JSON format and is meant to be used as a base to develop
language specific APIs.

Currently the repository contains the following JSON files:
```console
cpu/
├── cpuid.json                     # Contains information on CPUID calls to retrieve vendor and features on x86_64
├── cpuid_schema.json              # Schema for the file above
├── microarchitectures.json        # Contains information on CPU microarchitectures
└── microarchitectures_schema.json # Schema for the file above
 ```


## License

Archspec is distributed under the terms of both the MIT license and the
Apache License (Version 2.0). Users may choose either license, at their
option.

All new contributions must be made under both the MIT and Apache-2.0
licenses.

See [LICENSE-MIT](https://github.com/archspec/archspec-json/blob/master/LICENSE-MIT),
[LICENSE-APACHE](https://github.com/archspec/archspec-json/blob/master/LICENSE-APACHE),
[COPYRIGHT](https://github.com/archspec/archspec-json/blob/master/COPYRIGHT), and
[NOTICE](https://github.com/archspec/archspec-json/blob/master/NOTICE) for details.

SPDX-License-Identifier: (Apache-2.0 OR MIT)

LLNL-CODE-811653

## Optional x86 identity preferences

`microarchitectures.json` may contain an `x86_cpu_targets` object. Its keys are
exact vendor strings, then canonical decimal CPU family and model strings:

```json
{"x86_cpu_targets": {"HygonGenuine": {"24": {"7": "c86_4g_m7", "8": "c86_4g_m8"}}}}
```

The Hygon mappings and four target definitions are included in this change;
[source and validation notes](docs/hygon-c86-4g.md) distinguish compiler evidence
from hardware captures. A mapping supplies a target preference, not permission
to execute instructions. Consumers must still check target compatibility. No entry
means no preference; a family/model pair is not assumed to identify every
microarchitecture uniquely. Ambiguous identities should not be entered as a
single unconditional preference. Each entered identity needs supporting evidence.
The Python prototype initially collects these fields only on Linux x86.

With the current Python extension loader, a vendor entry in an extension replaces
that vendor's entire family/model mapping, rather than merging individual models.
A consumer should keep its original selection path when a mapped target does not
exist or fails compatibility checks. Schema validation checks the mapping's shape;
it does not establish hardware identity or validate target references.
