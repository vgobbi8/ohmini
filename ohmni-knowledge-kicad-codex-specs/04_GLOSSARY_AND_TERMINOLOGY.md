# 04 — Glossary and Terminology

## Knowledge Engine

Application-level service responsible for querying one or more knowledge providers and returning normalized, traceable knowledge bundles.

## Knowledge Base

The collection of reusable knowledge available through providers. It may consist of Markdown files, structured records, KiCad libraries, databases, retrieved documents, external APIs, or other sources.

## Knowledge Provider

Adapter capable of searching or retrieving knowledge from a particular source and normalizing it to Ohmni knowledge items.

## Knowledge Item

A normalized, typed unit of reusable knowledge with identity, classification, payload, applicability, provenance, and optional relationships.

## Knowledge Bundle

A query result containing relevant normalized knowledge items, provenance, warnings, and unresolved requests.

## Ingestion

The process of introducing externally authored or imported knowledge into a provider/repository.

## Pipeline State

Run-specific evidence: current requirement, generated artifacts, validator results, assumptions, attempts, and errors. Pipeline state is not automatically reusable knowledge.

## Agent Memory

Experience accumulated by an agent across attempts or sessions. Future memory may expose knowledge through a provider, but memory is not the definition of the Knowledge Engine.

## EDA Adapter

Adapter used to execute deterministic Electronic Design Automation operations, such as KiCad ERC, exports, or other toolchain operations.

## Authority Scope

The specific subject area for which a source should be treated as authoritative. A KiCad symbol library can be authoritative about its configured symbol definition but not necessarily about electrical maximum ratings.
