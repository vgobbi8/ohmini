---
id: electronics.procedure.design-rc-low-pass
family: procedural
kind: procedure
title: Design a first-order RC low-pass filter
tags: [electronics, filter, rc, low-pass, design]
authority: curated
authority_scope: design_procedure
---

# Design Procedure

## Goal

Choose practical `R` and `C` values for a requested first-order RC low-pass cutoff.

## Steps

1. Identify the requested cutoff frequency and relevant source/load conditions.
2. Select a practical capacitor or resistor value.
3. Calculate the complementary value using the cutoff-frequency formula.
4. Select a realizable preferred value.
5. Calculate the resulting nominal cutoff.
6. Record assumptions and value substitutions.
7. Validate frequency response using an AC analysis when available.

## Expected outputs

- selected `R`;
- selected `C`;
- calculated nominal cutoff;
- assumptions;
- validation strategy.
