# PDF Processing Workflow

graph LR
    A[Input PDF] --> B[Extract PDF Content]
    B --> C[Clean Text]
    C --> D[Split into Chunks]
    D --> E[Rate-Limited Processing]
    E --> F[API Request Queue]
    F --> G[Groq LLM API]
    G --> H[Response Processing]
    H --> I[Combine Summaries]
    I --> J[Final Output]

    subgraph "Text Processing"
    B --> |PyMuPDF| C
    C --> |Remove Empty Lines| D
    D --> |800 token chunks| E
    end

    subgraph "Rate Limiting"
    E --> |Token Counter| F
    F --> |60s Window| G
    end

    subgraph "API Integration"
    G --> |llama-3.3-70b| H
    H --> |Retry Logic| I
    end
