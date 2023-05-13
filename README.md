# CodeFlares-Backend

# Backend Repository

This repository contains the backend code for ingesting data using Kafka, loading it into a data lake, performing validation, transformation, and stamping using Spark, and storing the processed data in a normalized database (PostgreSQL).

## Technologies Used

- Kafka: Distributed messaging system for data ingestion.
- HDFS: Distributed file system for storing raw data in the data lake.
- Spark: Distributed data processing framework for validation, transformation, and stamping.
- PostgreSQL: Relational database for storing processed data in a normalized format.

## Flow of Process

1. User Upload:
   - Users upload data to the system, initiating the data processing pipeline.

2. Ingestion using Kafka:
   - Kafka acts as a distributed messaging system for data ingestion.
   - User-uploaded data is sent to Kafka topics.

3. Load Data Lake:
   - The data from Kafka topics is loaded into the data lake, which is implemented using HDFS.
   - Raw data is stored in its original format in the data lake for further processing.

4. Validation, Transformation, and Stamping using Spark:
   - Spark processes the data stored in the data lake.
   - The data goes through validation to ensure its quality and integrity.
   - Transformation tasks are performed to shape the data according to business requirements.
   - Stamping involves adding metadata or markers to the processed data for traceability.

5. Postgres SQL - Normalized Database:
   - The processed data is stored in a normalized database, specifically PostgreSQL.
   - The normalized database provides efficient storage and querying capabilities for structured data.

## Getting Started

To get started with the backend repository, follow these steps:

1. Clone the repository:
git clone https://github.com/your/repository.git


2. Install the required dependencies:
npm install


3. Configure Kafka:
- Set up Kafka and create the necessary topics for data ingestion.

4. Configure Spark:
- Set up Spark and configure the necessary Spark properties.

5. Configure PostgreSQL:
- Set up PostgreSQL and create the required database and tables.

6. Run the backend application:
npm start

Make sure to configure the necessary environment variables, connection strings, and other configurations as per your specific setup.

## Contributing

Contributions are welcome! If you have any improvements, bug fixes, or new features to propose, please feel free to submit a pull request.

This README file provides an overview of the backend repository, describes the technologies used, outlines the flow of the data processing process, and provides instructions for getting started and contributing to the project.
