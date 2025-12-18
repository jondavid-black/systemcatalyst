# Data Model - Workflow Definitions

## Entities

### 1. WorkflowDefinition
**Type**: Aggregate Root
**Description**: Container for a full workflow version.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | UUID | Yes | Unique Identifier |
| `name` | String | Yes | Human-readable name |
| `description` | String | No | |
| `use_case_id` | String | No | Traceability link (loose ref) |
| `nodes` | List[WorkflowNode] | Yes | Children nodes |
| `edges` | List[WorkflowEdge] | Yes | Connections |

### 2. WorkflowNode (Polymorphic)
**Type**: Entity
**Description**: A step in the workflow.

| Field | Type | Required | Description |
|---|---|---|---|
| `id` | String/UUID | Yes | Node ID (unique within workflow) |
| `type` | Enum | Yes | `TRIGGER`, `PROCESS`, `DECISION`, `BRANCH`, `JOIN`, `COMPLETION` |
| `label` | String | Yes | Display name |
| `properties` | PydanticModel | Yes | Polymorphic payload (stored as JSONB) |

#### Node Property Schemas (JSONB payloads)
- **ProcessNode**: `{ "description": "...", "handler_ref": "module.fn" }`
- **DecisionNode**: `{ "description": "..." }` (Conditions live on Edges)
- **TriggerNode**: `{ "event_type": "webhook/schedule", "schedule": "..." }`
- **Others**: Empty object `{}` initially.

### 3. WorkflowEdge
**Type**: Value Object
**Description**: Connection between nodes.

| Field | Type | Required | Description |
|---|---|---|---|
| `source_id` | String | Yes | ID of source node |
| `target_id` | String | Yes | ID of target node |
| `condition` | String | No | Logic expression (for Decision outputs) |

## Pydantic Models (Draft)

```python
from typing import Literal, Union, List, Optional
from pydantic import BaseModel, Field
from uuid import UUID

# --- Property Models ---
class ProcessProps(BaseModel):
    description: Optional[str] = None
    handler_ref: Optional[str] = None

class TriggerProps(BaseModel):
    event_type: str

class EmptyProps(BaseModel):
    pass

# --- Node Models (Discriminator) ---
class BaseNode(BaseModel):
    id: str
    label: str

class ProcessNode(BaseNode):
    type: Literal["PROCESS"]
    properties: ProcessProps

class TriggerNode(BaseNode):
    type: Literal["TRIGGER"]
    properties: TriggerProps

# Union Type for Polymorphism
WorkflowNode = Union[ProcessNode, TriggerNode, ...] 

# --- Edge ---
class WorkflowEdge(BaseModel):
    source_id: str
    target_id: str
    condition: Optional[str] = None

# --- Aggregate ---
class WorkflowDefinition(BaseModel):
    id: UUID
    name: str
    use_case_id: Optional[str]
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]
```
