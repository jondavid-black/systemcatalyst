# System Catalyst

System Catalyst is an opinionated framework for building digital systems tailored to your custom use cases. It enables rapid, incremental development while enforcing strict architectural principles to ensure long-term maintainability and scalability.

## Core Philosophy

System Catalyst is built on a foundation of strict **Model-View-Controller (MVC)** separation of concerns. By enforcing clear boundaries between data, business logic, and user interface, the framework ensures that systems remain modular, testable, and adaptable to change.

## Architecture & Tech Stack

System Catalyst orchestrates a modern Python stack to deliver a cohesive development experience:

### Model Layer (Data & State)
*   **Version Control First:** We treat data with the same rigor as code.
    *   **Database:** [Dolt](https://www.dolthub.com/) is used as the primary RDBMS, providing Git-like version control for your SQL database.
    *   **File System:** Git is used for version-controlled file management.
*   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) for robust database interactions.
*   **Validation:** [Pydantic](https://docs.pydantic.dev/) for strict data modeling and validation.

### Control Layer (Business Logic)
*   **API:** [FastAPI](https://fastapi.tiangolo.com/) exposes business logic via RESTful endpoints.
*   **Logic:** Pure Python implementations encapsulate core business rules, completely decoupled from the UI.

### View Layer (User Interface)
*   **UI Framework:** [Flet](https://flet.dev/) allows for the rapid construction of consistent, responsive interfaces that run on both desktop and web platforms from a single Python codebase.

## Getting Started

### Prerequisites
*   Python 3.12+
*   [uv](https://github.com/astral-sh/uv) for fast Python package and project management.

### Installation

1.  Clone the repository:
    ```bash
    git clone git@github.com:jondavid-black/systemcatalyst.git
    cd systemcatalyst
    ```

2.  Install dependencies:
    ```bash
    uv sync
    ```

### Development

*   **Run UI:** `uv run flet run src/ui/main.py`
*   **Run Service:** `uv run uvicorn src.service.main:app --reload`
*   **Run Tests:** `uv run pytest`

*   **Lint:** `uv run ruff check .`
*   **Format:** `uv run ruff format .`
*   **Documentation:** `uv run mkdocs serve`

For detailed developer guidelines, please refer to [AGENTS.md](AGENTS.md).

### Development Process
Git-REST development heavily relies on GenAI technology. This repo uses OpenCode and the GitHub Speckit extensions. The general workflow for starting new work should use the Speckit workflow in the OpenCode Agent:

/speckit.specify <Your high level requirements here>
/speckit.clarify
/speckit.plan
/speckit.checklist  (honestly I usually skip this step)
/speckit.tasks
/speckit.analyze

Review the checklists.  Mark all items that have been completed.  Ask any questions you need to mark the others.

Completing these commands should establish a detailed plan to guide GitHub Copilot through the implementation phases. Occasionally you may need to nudge the AI as you work through this process by answering questions or providing clarification. Before proceeding review any files in the /specs/<item>/checklists folder to ensure everything is marked complete. Once you have completed these AI commands it is recommended to commit and push before beginning implementation. Note that this process will automatically create and work within a new branch based on the first few words you enter into the high level requirements text. I like to create a new PR at this time so I can easily monitor CI throughout the implementation process.

/speckit.implement

To implement the plan use the /speckit.implement command in the GitHub Copilot Agent. This will cause the AI to step through the generated plan and tasks. The AI will fequently ask you questions such as 'do you want to begin the first implementation phase' or 'do you want to proceed'. I've found simply responding with 'Yes, begin the first phase' or 'Yes, proceed' results in very good outcomes. I've found it is sometimes best to review and approve commands individually as the AI works. This allows you to tweak things (i.e. add uv run in front of a command) to avoid unnecessary errors along the way that can spiral out of control. When the AI pauses and asks if you'd like to proceed, be sure to review the changes it has made up to that point and click the Keep button before telling the AI to proceed. Occasionally the GitHub Copilot may pause and say something to the effect of 'Continue to iterate?' As long as the AI hasn't fallen into a non-productive loop just click 'Continue'. The end result is the AI writing almost all the code with you occasionally typing 'Yes, proceed' to push it along.

The final step tends to focus on testing and QA steps. This is where you usually have to get more involved: running linting and formatting, running unit and BDD tests manually, pasting errors back into the AI to generate corrections, etc.

## Data Definition to SQL

You can now use this method to drive the generation process safely:
1. Load Registry
```python
registry.load_from_directory(...)
```
2. Get safe creation order
```python
try:
    ordered_tables = registry.get_ordered_schemas()
except ValueError as e:
    print(f"Cannot generate schema: {e}")
    exit(1)
```
3. Generate DDL
```python
generator.generate_ddl(ordered_tables)
```

## License

[MIT License](LICENSE)
