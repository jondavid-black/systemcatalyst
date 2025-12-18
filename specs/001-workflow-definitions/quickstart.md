# Quickstart - Workflow Definitions

## Overview
This feature provides the Data Elements to model business workflows. It uses Pydantic for validation and SQLAlchemy for persistence.

## Installation
The models are part of the core source. No extra installation required.

## Usage Guide

### 1. Creating a Workflow (Python)

```python
from src.models.workflow import WorkflowDefinition, ProcessNode, TriggerNode, WorkflowEdge

# 1. Define Nodes
trigger = TriggerNode(
    id="start", 
    label="Start Event", 
    type="TRIGGER",
    properties={"event_type": "manual"}
)

step1 = ProcessNode(
    id="step-1", 
    label="Approver Step", 
    type="PROCESS",
    properties={"handler_ref": "services.approvals.request"}
)

# 2. Define Edges
edge = WorkflowEdge(source_id="start", target_id="step-1")

# 3. Create Workflow
wf = WorkflowDefinition(
    id=uuid4(),
    name="Approval Flow",
    use_case_id="UC-001",
    nodes=[trigger, step1],
    edges=[edge]
)

# 4. Validate (Graph Check)
errors = validate_workflow(wf)
if errors:
    print("Invalid structure:", errors)
```

### 2. Validation Rules
The `validate_workflow` function checks:
- **Connectivity**: All nodes must be reachable from a Trigger.
- **Cycles**: No infinite loops (unless explicitly allowed, currently warnings).
- **Integrity**: Edges must point to existing Node IDs.

### 3. Database Persistence
Use standard SQLAlchemy sessions:
```python
session.add(wf_model)
session.commit()
```
(Note: `wf_model` is the SQLAlchemy mapping of the Pydantic object).
