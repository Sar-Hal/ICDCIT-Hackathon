# Scheduler

```mermaid
flowchart TD
    A[Start] --> B[Load Environment Variables]
    B --> C[Connect to MongoDB]
    C --> D[Fetch Tasks from MongoDB]
    D --> E[Check if Tasks Exist]
    E -->|Tasks Found| F[Query GROQ API for Schedule]
    E -->|No Tasks| G[Print No tasks available]
    F --> H[Convert Schedule to JSON]
    H --> I[Output Schedule as JSON]
    G --> J[End]
    I --> J[End]
