#!/usr/bin/env python3
# Copyright 2019-2020 Lawrence Livermore National Security, LLC and other
# Archspec Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Check that the explicit ``from`` DAG is consistent with feature set inclusion.

Every microarchitecture names a set of features, so feature inclusion defines a
partial order of its own. The ``from`` DAG must agree with it in two directions:

* A descendant must list every feature of its ancestors, up to ``feature_aliases``.
* Within a family, a microarchitecture whose feature set strictly contains
  another's must descend from it when both share a vendor, or when the smaller
  one is a generic level. Cross-vendor lineage is intentionally not required:
  portability between vendors is expressed through the generic levels only.
"""
import itertools
import json
import pathlib
import sys

JSON_DIR = pathlib.Path(__file__).parent.parent / "cpu"


def main() -> int:
    with open(JSON_DIR / "microarchitectures.json") as f:
        data = json.load(f)

    uarchs = data["microarchitectures"]
    aliases = data.get("feature_aliases", {})

    ancestors = {}

    def transitive_ancestors(name):
        if name not in ancestors:
            result = set()
            for parent in uarchs[name]["from"]:
                result.add(parent)
                result |= transitive_ancestors(parent)
            ancestors[name] = result
        return ancestors[name]

    def family(name):
        roots = [a for a in transitive_ancestors(name) | {name} if not uarchs[a]["from"]]
        assert len(roots) == 1, f"{name} has multiple family roots: {roots}"
        return roots[0]

    def closed_features(name):
        """The declared features, closed under the alias rules."""
        result = set(uarchs[name]["features"])
        for feature, rule in aliases.items():
            if "any_of" in rule and result & set(rule["any_of"]):
                result.add(feature)
            if "families" in rule and family(name) in rule["families"]:
                result.add(feature)
        return result

    features = {name: closed_features(name) for name in uarchs}
    violations = []

    for ancestor in uarchs:
        for descendant in uarchs:
            if ancestor not in transitive_ancestors(descendant):
                continue
            missing = features[ancestor] - features[descendant]
            if missing:
                violations.append(
                    f"{descendant} descends from {ancestor} but lacks its features: "
                    f"{', '.join(sorted(missing))}"
                )

    for smaller, larger in itertools.permutations(uarchs, 2):
        if family(smaller) != family(larger):
            continue
        # an entry with no declared features asserts nothing, and alias closure may still
        # give it synthetic ones, so it cannot imply an edge
        if not uarchs[smaller]["features"]:
            continue
        if not features[smaller] < features[larger]:
            continue
        same_vendor = uarchs[smaller]["vendor"] == uarchs[larger]["vendor"]
        if not same_vendor and uarchs[smaller]["vendor"] != "generic":
            continue
        if smaller not in transitive_ancestors(larger):
            violations.append(
                f"{larger} has every feature of {smaller} and more, but does not descend "
                f"from it"
            )

    for violation in violations:
        print(f"ERROR: {violation}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
