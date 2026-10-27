E-Commerce Analytics Engine
A graph-powered analytics platform built to extract real-time insights, personalized recommendation networks, and customer behavioral patterns using Python, Streamlit, and Neo4j.
Project Overview
The E-Commerce Analytics Engine transitions traditional relational data into a high-performance graph database architecture. By modeling customers, products, categories, and order events as interconnected nodes and relationships, the platform performs real-time graph traversal algorithms to surface deep behavioral insights, detect purchasing fraud patterns, and serve personalized cross-sell and up-sell recommendations.

The interactive front-end dashboard is powered by Streamlit, allowing non-technical business analysts and product managers to execute complex Cypher queries through intuitive visualizations, filtering controls, and graph metrics.
Key Features
Real-Time Recommendation Pipeline: Leverages Collaborative Filtering and PageRank graph algorithms to generate personalized product recommendations based on co-purchase paths ((:Customer)-[:PURCHASED]->(:Order)-[:CONTAINS]->(:Product)).
Interactive Graph Visualization: Embedded dynamic graph layouts that allow users to inspect customer clusters, product category hierarchies, and implicit preference connections.
Customer Segmentation & Churn Analysis: Evaluates customer centrality metrics (Degree, Betweenness, Closeness) to isolate high-value brand advocates and segment users based on purchasing velocity.
Fraud & Anomaly Detection: Flags suspicious buying behaviors, such as shared payment profiles across distinct shipping addresses or rapid automated order generation.
Dynamic Executive Dashboard: High-level operational metrics including Total Revenue, Average Order Value (AOV), Conversion Flow, and Product Network Density.
Tech Stack & Architecture
Component
Technology
Purpose
Language
Python 3.10+
Core processing engine, data transformation, and orchestration
Database
Neo4j Enterprise / AuraDB
Graph database storing entities and relationship topologies
Query Language
Cypher
Complex graph traversals and pattern matching
UI Framework
Streamlit
Web interface for dynamic visualization and data filtering
Data Libraries
Pandas, Pyvis, Neo4j Python Driver
Data manipulation and interactive network rendering

Prerequisites
Before running the application, ensure you have the following installed and configured:

Python: Version 3.10 or higher
Neo4j Database: A running instance of Neo4j Desktop, Docker container, or Neo4j AuraDB instance (v5.x+)
Package Manager: pip or conda
Installation Instructions
1. Clone the Repository
git clone https://github.com/your-org/ecommerce-analytics-engine.git

cd ecommerce-analytics-engine
2. Create and Activate a Virtual Environment
h
macOS / Linux
python3 -m venv venv
source venv/bin/activate
Windows
python -m venv venv
.\venv\Scripts\activate

### 3. Install Dependencies

```bash

pip install --upgrade pip

pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory of the project and supply your Neo4j database connection credentials:v
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_secure_password
APP_PORT=8501

### 5. Seed the Database (Optional)

If starting with an empty Neo4j instance, run the included database initialization script to generate constraints, indexes, and sample ecommerce dataset:

```bash

python scripts/seed_database.py
Usage
Launching the Dashboard
Execute the following command from the root directory to launch the Streamlit application:streamlit run app.py

Once running, navigate to http://localhost:8501 in your web browser.
Key Workflows
Exploring Product Networks: Navigate to the Product Graph tab to filter by category and visualize products frequently bought together.
Generating Recommendations: Open the Customer Insights page, select a target CustomerID, and adjust recommendation parameters (e.g., minimum path similarity, depth).
Running Graph Algorithms: Access the Algorithms section to trigger community detection (Louvain algorithm) or node centrality calculations directly on your active database.
Project Structure
ecommerce-analytics-engine/

├── assets/                  # Documentation images and static assets

├── config/                  # Database connections and app settings

│   └── database.py

├── queries/                 # Cypher query templates and scripts

│   ├── analytics.cypher

│   └── recommendations.cypher

├── scripts/                 # Ingestion and database seeding utility scripts

│   └── seed_database.py

├── src/                     # Core application modules

│   ├── components/          # Reusable Streamlit UI widgets

│   ├── graph_service.py     # Neo4j driver interface and graph execution

│   └── visualizer.py        # Pyvis and Plotly chart wrappers

├── app.py                   # Main Streamlit application entry point

├── .env.example             # Environment variable template

├── requirements.txt         # Python package dependencies

└── README.md                # Project documentation
Contributing
Contributions are welcome. Please adhere to the following workflow:

Fork the repository.
Create a feature branch (git checkout -b feature/analytics-enhancement).
Commit your changes (git commit -m 'Add custom graph projection support').
Push to the branch (git push origin feature/analytics-enhancement).
Open a Pull Request for review.
License
This project is licensed under the MIT License. See the LICENSE file for details.
