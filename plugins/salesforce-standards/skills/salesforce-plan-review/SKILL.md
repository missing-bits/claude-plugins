---
name: salesforce-plan-review
description: Plan-review checklist for Salesforce — metadata blast radius, governor limits at target volumes, security model, automation overlap, deployment dependencies and ordering; invoked by the plan-adversary agent.
---

# Salesforce plan-review checklist

Walk every dimension against the reviewed plan; nothing passes by
default. Every finding cites a plan quote or file path as evidence.
Severities noted per dimension bind — do not re-grade them.

## 1. Metadata blast radius

- The plan names every metadata type it touches and the components
  affected. A silent touch of shared metadata (profiles, permission
  sets, layouts, shared objects) → Important.
- A change to a shared object or field without listing its consumers
  (code, flows, reports, integrations) → Important.

## 2. Governor limits at target volumes

- SOQL or DML inside a loop planned on a trigger or bulk path →
  Critical.
- The plan states expected record volumes for every bulk path;
  unstated volumes on triggers, batch, or record-triggered flows →
  Important.

## 3. Security model

- A new object or field without a stated org-wide default, FLS, and
  permission-set assignment → Important.
- Planned Apex without a sharing declaration, or `without sharing`
  lacking a stated justification → Important.
- A capability granted to a profile where a permission set is the
  standard → Important.

## 4. Automation overlap

- A new trigger or record-triggered flow on an object that already has
  one for the same trigger moment, without an interaction note →
  Important.
- Any new Workflow Rule or Process Builder automation → Critical
  (retired surface; Flow is the target). Deliberately one grade above
  the severity `flow-retired-automation` carries in its rule tag: at
  plan time the design can still change; post-hoc review grades by
  that rule tag.

## 5. Deployment dependencies and ordering

- Metadata with deploy-order dependencies (fields before permission
  sets and layouts, CMT types before their records) not sequenced in
  the plan → Important.
- Org changes outside sf CLI deployments (manual Setup steps) not
  flagged as manual steps with an owner → Important.
