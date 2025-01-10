# Scheduler

```mermaid
flowchart TD
    A[Start] --> B[Load Environment Variables]
    B --> C[Connect to MongoDB]
    C --> D[Fetch Tasks from MongoDB]
    D --> E[Check if Tasks Exist]
    E -->|Tasks Found| F[Query GROQ API for Schedule]
    E -->|No Tasks| G[Print "No tasks available."]
    F --> H[Convert Schedule to JSON]
    H --> I[Output Schedule as JSON]
    G --> J[End]
    I --> J[End]

    B -->|Load GROQ_API_KEY| B1[Load .env file]
    C -->|MongoDB URI| C1[Connect using MONGO_URI]
    D -->|User ID| D1[Query tasks collection with userId]
    F -->|Tasks| F1[Send tasks to GROQ API for schedule generation]
    H -->|Generated Schedule| H1[Format schedule into JSON]
    I -->|Schedule JSON| I1[Print JSON for Node.js output]
