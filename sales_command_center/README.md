# Sales Command Center

> AI-Powered Sales Intelligence Dashboard with Voice-Activated Transaction Capabilities

## Overview

The **Sales Command Center** is a specialized, process-specific AI dashboard designed for sales executives and managers. It provides real-time visibility into sales operations, AI-powered insights, and the unique ability to execute transactions through voice commands.

### Key Features

- **Real-Time Sales Dashboard**: Live metrics for orders, pipeline, revenue, and performance
- **AI Conversational Interface**: Ask questions in natural language
- **Voice-Activated Commands**: Create sales orders and query data using voice
- **Transactional Capabilities**: AI-drafted transactions with review-and-approve workflow
- **Live System Integration**: Real-time sync with Salesforce, Netsuite, and other ERP systems
- **AI-Generated Insights**: Proactive recommendations and anomaly detection
- **Mobile-Responsive**: Works on desktop, tablet, and mobile devices

## Architecture

Built with:
- **Backend**: Python, FastAPI, LangGraph (multi-agent orchestration)
- **Frontend**: HTML5, Tailwind CSS, JavaScript, Chart.js
- **AI**: OpenAI GPT-4 / Anthropic Claude
- **Database**: PostgreSQL
- **Cache**: Redis
- **Integrations**: Salesforce, Netsuite

See [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) for detailed architecture.

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Node.js (for frontend tooling, optional)
- Salesforce account with API access
- Netsuite account with SuiteTalk API access
- OpenAI API key

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sales-command-center.git
   cd sales-command-center
   ```

2. **Set up Python environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cd sales_dashboard
   cp .env.template .env
   # Edit .env with your actual API keys and configuration
   ```

4. **Set up database**:
   ```bash
   # Create PostgreSQL database
   createdb sales_command_center

   # Run migrations (if using Alembic)
   alembic upgrade head
   ```

5. **Start Redis** (if not running):
   ```bash
   redis-server
   ```

6. **Run the application**:
   ```bash
   cd sales_dashboard
   python run_server.py
   ```

7. **Access the dashboard**:
   Open your browser to [http://localhost:8000](http://localhost:8000)

## Configuration

All configuration is managed through environment variables in `.env`:

### Required Variables

```env
# LLM
OPENAI_API_KEY=sk-your-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sales_command_center

# Salesforce
SALESFORCE_CLIENT_ID=your_client_id
SALESFORCE_CLIENT_SECRET=your_client_secret
SALESFORCE_USERNAME=your_username
SALESFORCE_PASSWORD=your_password

# Netsuite
NETSUITE_ACCOUNT_ID=your_account_id
NETSUITE_CONSUMER_KEY=your_consumer_key
NETSUITE_CONSUMER_SECRET=your_consumer_secret
NETSUITE_TOKEN_ID=your_token_id
NETSUITE_TOKEN_SECRET=your_token_secret
```

See [sales_dashboard/.env.template](sales_dashboard/.env.template) for all available configuration options.

## Usage

### Natural Language Queries

Ask questions about your sales data:

- "How many orders did I receive today?"
- "Show me pending orders over $100K"
- "Which region is underperforming this quarter?"
- "Compare this month vs last month"
- "What's my pipeline for Q1 2026?"

### Voice Commands

Use the microphone button to:

- **Query data**: "Show me today's sales"
- **Create orders**: "Create a sales order for Disney for 500 hats at $50 each"
- **Compare performance**: "Compare North America to EMEA this quarter"

### Transaction Creation Workflow

1. Click "Create Order" or use voice command
2. AI extracts entities (customer, product, quantity, price)
3. Review the AI-generated draft
4. Edit if needed
5. Approve and submit to Netsuite
6. Receive confirmation

## Project Structure

```
sales-command-center/
├── docs/                           # Documentation
│   ├── architecture/              # Architecture docs & diagrams
│   └── requirements/              # Product requirements
├── sales_dashboard/               # Backend Python application
│   ├── agents/                    # AI agents
│   │   ├── base_agent.py         # Base agent class
│   │   ├── order_agent.py        # Order queries
│   │   ├── pipeline_agent.py     # Pipeline/deals
│   │   ├── transaction_agent.py  # Transaction creation
│   │   └── ...
│   ├── api/                       # FastAPI routes
│   │   ├── routes/
│   │   └── server.py
│   ├── data/                      # Data layer
│   │   ├── connectors/           # External API connectors
│   │   ├── models/               # Database models
│   │   └── repositories/         # Data repositories
│   ├── graph/                     # LangGraph orchestration
│   ├── config.py                  # Configuration
│   └── run_server.py              # Server entry point
├── frontend/                      # Frontend assets
│   └── sales_dashboard.html      # Main dashboard
├── deployment/                    # Deployment configs
├── presentation/                  # Sales presentations
└── README.md
```

## API Endpoints

### Dashboard Endpoints
- `GET /api/v1/dashboard/overview` - Overview metrics
- `GET /api/v1/dashboard/pipeline` - Pipeline data

### Order Endpoints
- `GET /api/v1/orders` - List orders
- `POST /api/v1/orders` - Create order
- `GET /api/v1/orders/{id}` - Get order details

### AI Query Endpoint
- `POST /api/v1/query/ask` - Natural language query

### Transaction Endpoints
- `POST /api/v1/transactions/create` - Create transaction via AI
- `POST /api/v1/transactions/{id}/approve` - Approve draft transaction

Full API documentation available at `/docs` (Swagger UI)

## Integration Setup

### Salesforce Integration

1. Create a Connected App in Salesforce
2. Enable OAuth 2.0
3. Get Client ID and Secret
4. Set up webhooks for real-time updates

See [docs/integrations/SALESFORCE_SETUP.md](docs/integrations/) for detailed instructions.

### Netsuite Integration

1. Enable SuiteTalk Web Services
2. Create integration record
3. Generate Token-Based Authentication credentials
4. Configure webhook endpoints

See [docs/integrations/NETSUITE_SETUP.md](docs/integrations/) for detailed instructions.

## Development

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Format code
black sales_dashboard/

# Lint
flake8 sales_dashboard/

# Type checking
mypy sales_dashboard/
```

### Adding a New Agent

1. Create agent class in `sales_dashboard/agents/`
2. Inherit from `BaseAgent`
3. Implement `get_system_prompt()` and `process_query()`
4. Register in orchestrator

Example:

```python
from agents.base_agent import BaseAgent

class MyNewAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return "You are an expert in..."

    def process_query(self, query: str, context: dict) -> dict:
        # Process query
        return {"success": True, "response": "..."}
```

## Deployment

### Docker Deployment

```bash
docker build -t sales-command-center .
docker run -p 8000:8000 --env-file .env sales-command-center
```

### AWS ECS Deployment

See [deployment/AWS_DEPLOYMENT.md](deployment/) for detailed instructions.

### Environment-Specific Configuration

- **Development**: `.env` with DEBUG=True
- **Staging**: `.env.staging`
- **Production**: `.env.production` (use AWS Secrets Manager)

## Security

- OAuth 2.0 / SSO integration
- JWT token authentication
- Role-based access control (RBAC)
- API rate limiting
- Encryption in transit (TLS 1.3)
- Encryption at rest (AES-256)
- Audit logging

See [docs/SECURITY.md](docs/) for security best practices.

## Monitoring & Logging

- **Application Logs**: CloudWatch / Datadog
- **Performance Metrics**: Response times, error rates
- **Business Metrics**: Query volume, agent usage
- **Alerts**: Critical errors, performance degradation

## Roadmap

### Phase 1 (Months 1-3) - MVP
- ✅ Core dashboard with key metrics
- ✅ Salesforce integration (read-only)
- ✅ AI query engine
- ✅ Basic order management

### Phase 2 (Months 4-6) - Transactions
- Voice command support
- AI-powered sales order creation
- Netsuite write integration
- Approval workflows

### Phase 3 (Months 7-12) - Scale
- Mobile native apps
- Advanced analytics and ML
- Additional integrations (Jira, ADP, etc.)
- Multi-language support

## Support

- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/yourusername/sales-command-center/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/sales-command-center/discussions)
- **Email**: support@salescommandcenter.com

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

[MIT License](LICENSE)

## Acknowledgments

- Based on the Executive Command Center prototype by Pk
- Inspired by feedback from Dipinder Singh
- Built with FastAPI, LangGraph, and OpenAI

---

**Made with ❤️ for sales teams everywhere**
