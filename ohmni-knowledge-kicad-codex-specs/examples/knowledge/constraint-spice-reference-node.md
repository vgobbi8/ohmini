---
id: electronics.constraint.spice-reference-node
family: declarative
kind: constraint
title: SPICE circuits require a reference node
tags: [electronics, spice, simulation, constraint]
authority: curated
authority_scope: spice_modeling_rule
---

# Constraint

A SPICE circuit intended for ngspice simulation must contain an appropriate reference node (`0`).

## Strength

Hard for the supported simulation representation.

## Rationale

The simulator requires a reference potential for nodal analysis.
