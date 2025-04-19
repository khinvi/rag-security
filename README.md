# Secure RAG Framework

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.10-green.svg)
![Status](https://img.shields.io/badge/status-research_in_progress-yellow.svg)

A comprehensive security framework for Retrieval-Augmented Generation (RAG) systems deployed in cloud environments, with a focus on defending against prompt injection attacks targeting vector database components.

## 🔒 Project Overview

This repository contains the implementation of my research on securing RAG systems against prompt injection and vector database attacks. The project addresses critical security vulnerabilities in RAG deployments that leverage vector databases in production environments.

### Research Goals

1. Identify and analyze RAG-specific security vulnerabilities
2. Design and implement a three-layer defense framework
3. Develop quantitative metrics for evaluating RAG security
4. Provide implementation guidelines for secure cloud deployment

### Three-Layer Defense Framework

The security architecture implements three defense layers:

1. **Pre-retrieval Defense**: Input validation and prompt sanitization to catch attacks before they reach the retrieval system
2. **Vector Database Security**: Embedding verification and access controls to prevent poisoning and unauthorized data access
3. **Post-retrieval Defense**: Response validation to detect and mitigate the effects of successful attacks

## 🚀 Current Status

This project is currently in active development as part of my research at UC San Diego. I am implementing and testing the security framework components outlined in my proposal. Progress by component:

- ✅ Project architecture design
- ✅ Pre-retrieval defense implementation
- 🔄 Vector database security (in progress)
- 🔄 Post-retrieval defense (in progress)
- ⬜ Security monitoring and logging
- ⬜ Comprehensive testing
- ⬜ Cloud deployment automation

## 📋 Implementation Timeline

This is an 8-week research project with the following timeline:

- **Weeks 1-2**: Core framework and pre-retrieval defense
- **Weeks 3-4**: Vector database security
- **Weeks 5-6**: Post-retrieval defense and monitoring
- **Weeks 7-8**: Testing, evaluation, and deployment

## 🛠️ Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key (for embeddings and LLM)
- Pinecone API key (or other vector database)
- Docker and Docker Compose (for containerized deployment)

### Installation

1. Clone the repository
```bash
git clone https://github.com/akhinvasara/secure-rag-framework.git
cd secure-rag-framework
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Running Locally

Start the development server:
```bash
uvicorn app.main:app --reload
```

Or use Docker Compose:
```bash
docker-compose up --build
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [Security Features](docs/security_features.md)
- [API Documentation](docs/api.md)
- [Deployment Guide](docs/deployment.md)
- [Testing Framework](docs/testing.md)

## 📊 Evaluation

The project includes a comprehensive evaluation framework to measure:

- Attack success rates before and after implementing defenses
- Performance impact of security measures
- False positive/negative rates
- Defense layer effectiveness

## 🔍 Research Applications

This research has direct applications for organizations implementing RAG systems in production environments:

- Enterprise AI systems with sensitive data
- Customer-facing AI assistants
- Knowledge management systems
- Internal documentation search tools

## 🤝 Contributing

This is an active research project, and I welcome collaboration and feedback. Please feel free to open issues or reach out directly at akhinvasara@ucsd.edu.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📝 Citation

If you use this framework in your research or implementation, please cite:

```
Khinvasara, A. (2025). Securing Cloud-Based RAG Systems Against Prompt Injection Attacks.
University of California, San Diego.
```

## 🔗 Related Work

- Wei, J., et al. (2023). "Jailbreaking Black Box Large Language Models in Twenty Queries."
- Greshake, K., et al. (2023). "More than you've asked for: A Comprehensive Analysis of Novel Prompt Injection Threats to Application-Integrated Large Language Models."
- Zou, A., et al. (2023). "Universal and Transferable Adversarial Attacks on Aligned Language Models."
