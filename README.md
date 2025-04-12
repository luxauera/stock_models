
# Financial Models

A collection of financial models and utilities for analyzing and forecasting financial data. This repository includes models for time series forecasting, volatility modeling, chaotic system analysis, and more.

## Features

- **Database Management**: [`PostgresModel`](assets/PostgresManager.py) provides utilities for managing PostgreSQL connections and schemas.
- **Time Series Models**:
  - [`GarchModel`](assets/GARCHModel.py): Implements GARCH for volatility modeling.
  - [`ARIMAModel`](assets/SARIMAModel.py): Implements SARIMA for time series forecasting.
  - [`LyapunovModel`](assets/LYAPONOVModel.py): Uses Lyapunov exponents for chaotic system analysis.
- **Statistical Analysis**: [`Stock_Stats`](assets/Statics.py) computes key statistics like mean, variance, and returns.
- **Query Management**: [`QueryModel`](assets/QueryManager.py) simplifies database queries and schema exploration.

## Setup

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd Financial_Models
   ```

2. Set up the environment variables:
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_PORT`
   - `DB_HOST`
   - `RUN_PERIOD`

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Application

### Usage

The application runs various financial models periodically based on the `RUN_PERIOD` environment variable. The following processes are included:

- **GARCH Process**: Executes the GARCH model for all tables in the database.
- **Stats Process**: Computes statistical metrics for financial data.
- **SARIMA Process**: Forecasts future values using SARIMA.
- **Lyapunov Process**: Analyzes chaotic behavior using Lyapunov exponents.

### Testing

Use the `test.ipynb` notebook for experimentation and testing individual components.

## Docker Support

Build and run the application in a Docker container:

```sh
docker build -t financial-models .
docker run -e DB_NAME=<your-db-name> -e DB_USER=<your-db-user> -e DB_PASSWORD=<your-db-password> -e DB_PORT=<your-db-port> -e DB_HOST=<your-db-host> financial-models
```

## Dependencies

All dependencies are listed in `requirements.txt`. Key libraries include:

- `pandas`, `numpy`: Data manipulation and analysis
- `statsmodels`, `arch`: Statistical modeling
- `tensorflow`, `keras`: Deep learning frameworks
- `SQLAlchemy`, `psycopg2`: Database interaction

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
