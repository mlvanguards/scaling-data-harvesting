# Scaling Data Harvesting

Creating a High-Performance Web Crawling Infrastructure with Genezio

## Overview

This project is a web crawling infrastructure that analyzes LinkedIn posts to identify technology trends. It consists of a Next.js frontend for user interaction and a Python backend for web crawling and data analysis.

## Prerequisites

- Node.js (v19.0.0 or higher)
- Python (v3.11 or higher)
- Poetry (Python package manager)
- Genezio CLI
- MongoDB database
- RapidAPI key for LinkedIn data access
- OpenAI API key for trend analysis



## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/scaling-data-harvesting.git
cd scaling-data-harvesting
```

2. Install frontenddependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd backend
poetry install --no-root
poetry shell
```

4. Create a `.env` file in the `backend` directory with the following variables:
```.dotenv
# Database
DATABASE_URI=your_mongodb_connection_string  
DATABASE_NAME=your_database_name 

# Rapid API 
RAPID_API_KEY=your_rapidapi_key  
RAPID_API_ENDPOINT=your_rapidapi_endpoint  

# Open API
OPENAI_API_KEY=your_openai_api_key  
OPENAI_MODEL=gpt-4-turbo-preview
 
# You get this value after running `make local`in the Functions Deployed -> function-crawler, 
# or when calling `make deploy` from genezio dashboard, this will require you to change the value in genezio environment variables
CRAWLER_URL=your_crawler_endpoint
```

## Running the Project Locally

1. Start the development environment using Genezio:

```bash
make local
```

This command will:
- Start the local Genezio server
- Load environment variables from `./backend/.env`
- Start both frontend and backend services  


2. Open your browser and navigate to: 
```bash
http://localhost:3000
```

This will display the Next.js frontend.


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request