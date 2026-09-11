# Stage 7: MySQL Integration

## Objective

This stage prepares the database layer for prediction persistence and analytics. MySQL is used to store prediction records, which the frontend and dashboard can later query for history and statistics.

## Schema

```sql
CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produce_name VARCHAR(255),
    produce_category VARCHAR(50),
    freshness_status VARCHAR(50),
    confidence DECIMAL(5,4),
    image_path VARCHAR(500),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project structure

- backend/database/db.py — SQLAlchemy connection setup
- backend/models/prediction.py — ORM model for predictions

## Notes

The application is designed so local development does not require AWS credentials. The database is optional for demo usage, but the schema and connection layer are ready for a real MySQL deployment.
