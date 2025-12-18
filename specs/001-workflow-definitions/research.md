# Research Findings - Workflow Definitions

## Decisions

### 1. Polymorphism Strategy
**Decision**: Single Table Inheritance (STI) with JSONB.
**Rationale**:
- Fits the existing `SchemaGenerator` (1:1 Table mapping) without modification.
- Reduces schema migration complexity (adding properties doesn't require DDL).
- Sufficient for "lightweight" workflows where `properties` vary but core identity (`id`, `label`, `type`) is shared.
**Alternatives Considered**:
- **Joined Table Inheritance**: Rejected due to high schema complexity (multiple tables/joins) and high friction for adding new node types.

### 2. Validation Logic
**Decision**: Custom DFS/BFS Implementation.
**Rationale**:
- Zero external dependencies (`networkx` adds unnecessary weight).
- Simple requirements (Cycle & Island detection) are solvable with <60 LOC.
- Easier to customize specific error messages (e.g. "Node X is unreachable from Trigger").
**Alternatives Considered**:
- **networkx**: Rejected as overkill for MVP validation. May be reconsidered if complex graph analysis (e.g. layouting, critical path) is needed later.

### 3. Use Case Linking
**Decision**: Loose String Reference.
**Rationale**:
- Decouples Workflow feature from non-existent Use Case feature.
- Allows workflows to be drafted before Use Cases are formally defined.
- Consistent with "Draft" nature of early workflows.

## Technical Approach

### Data Model Structure
- **WorkflowDefinition**: `id`, `name`, `use_case_id` (str), `nodes` (list), `edges` (list).
- **WorkflowNode**: `id`, `type` (Enum), `label`, `properties` (Pydantic Model via STI).
- **WorkflowEdge**: `source_id`, `target_id`, `condition` (Optional).

### Validation Algorithm
1. **Connectivity**: BFS from all `Trigger` nodes. Collect reachable set. `Islands = AllNodes - ReachableSet`.
2. **Cycles**: DFS with `recursion_stack` tracking. If node in stack is visited again -> Cycle.
