---
kind: superseded-workplan-record
workplan_id: PROTOCOL-ORCHESTRATOR-SEMIAUTOMATIC-WORKFLOW-CONTROL
protocol_version: 5.16.0
status: superseded
superseded_date: 2026-09-07
superseded_by: orchestrator/ARCHITECTURE_STANDARD.md
former_last_commit: 15282053c3538f395fc70224b095d04c0937edb5
---

# Superseded Protocol Orchestrator Monolithic Workplan

The former active workplan attempted to implement prompt generation, tracking, direct agent integration, benchmark-based recommendations, metering, prediction, and quota-aware scheduling as one large implementation contract.

It is intentionally retired **before implementation**. The stakeholder replaced that implementation shape with a nested capability ladder whose parent authority is now:

`orchestrator/ARCHITECTURE_STANDARD.md`

Still-binding product and architectural semantics from the former plan, including manual web/local separation, private history, ACP-first structured transport, benchmark capability evidence, resource ledgers, metering/prediction separation, and quota-aware scheduling, were reconciled into that architecture standard.

No implementation completion is claimed by this archive record.

Future implementation proceeds through separate module workplans derived losslessly from the architecture standard in this order:

1. Prompt Module;
2. Tracker Module;
3. Adapter Module;
4. Scheduler Module.

This archived record is historical context only and must not compete with the architecture standard or a later active module workplan.