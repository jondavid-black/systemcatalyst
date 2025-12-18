# Implementation Plan - Workflow Definitions

**Feature**: Workflow Definitions
**Status**: APPROVED
**Spec**: [spec.md](./spec.md)

## Technical Context

### Architecture & Patterns
- **Language/Framework**: Python (Pydantic, SQLAlchemy)
- **Architecture**: MVC - Models only for this phase.
- **Pattern**: 
    - `WorkflowDefinition` as aggregate root.
    - `WorkflowNode` and `WorkflowEdge` as child entities.
    - `Discriminator` pattern for Node Types (Polymorphic Pydantic models).
- **Validation**: Pydantic `model_validator` or custom methods for graph integrity (cycles/islands).

### Dependencies & Libraries
- **Standard**: `typing`, `uuid`, `enum`, `datetime`
- **Third-party**: 
    - `pydantic`: Data validation and serialization.
    - `sqlalchemy`: Database ORM.
    - `networkx`: **REJECTED** (Overkill). Using Custom DFS/BFS.

### Interfaces & Contracts
- **Inputs**: Python object instantiation / Dictionary payloads.
- **Outputs**: Validated model objects or validation errors.
- **Storage**: SQL Tables (via SQLAlchemy models).

### Decisions & Resolutions
- **Polymorphism**: Single Table Inheritance (STI) with JSONB.
- **Validation**: Custom DFS/BFS implementation (<60 LOC).
- **Nodes Schema**: `properties` column as JSONB.

## Constitution Check

### Principles
- **Library-First**: N/A (Constitution is generic/templated). Project follows MVC/Greenfield Python.
- **Test-First**: Yes, spec mandates independent tests (script-based).
- **Simplicity**: Yes, scope reduced to just Data Elements.

### Gate Evaluation
- [x] **Spec Clear**: Yes.
- [x] **Research Complete**: Yes, Strategy defined in `research.md`.
- [x] **Design Approved**: Yes, `data-model.md` created.

## Phase 0: Outline & Research

### Tasks
- [x] Research: SQL Polymorphism strategy (JSONB vs Table Inheritance) for Workflow Nodes.
- [x] Research: Graph validation library vs custom implementation.

## Phase 1: Design & Contracts

### Tasks
- [x] Design: `data-model.md` defining Entity Relationships and Pydantic Schemas.
- [x] Design: `seed_workflow.py` script structure.
- [x] Update: `quickstart.md` with instructions on how to use the models.

## Phase 2: Implementation & Validation

### Tasks
- [ ] Scaffold: Directory structure for `src/models/workflow`.
- [ ] Implement: `WorkflowDefinition` model.
- [ ] Implement: `WorkflowNode` and subtypes.
- [ ] Implement: `WorkflowEdge` model.
- [ ] Implement: Validation logic (Cycle/Island detection).
- [ ] Implement: `seed_workflow.py` script.
- [ ] Verify: Run seed script and assert success.
