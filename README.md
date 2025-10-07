# Recruitment Analytics Dashboard

An interactive dashboard for analyzing recruitment data with comprehensive visualizations and metrics.

## Features

- **Key Metrics**: Overview of total requisitions, closed positions, average TAT, profiles shared, and interviews
- **Interactive Filters**: Filter by Business Unit, Department, and Location
- **Visualizations**:
  - Requisition status distribution
  - Business unit analysis
  - Location-wise breakdown
  - Gender distribution
  - Time series trends
  - Candidate source analysis
  - TAT analysis and distributions
  - Department-wise statistics
- **Data Export**: Download filtered data as CSV
- **Responsive Design**: Full-width layout with interactive Plotly charts

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your Excel file (`datafile.xlsx`) in the project directory

## Usage

Run the dashboard:
```bash
streamlit run dashboard.py
```

or

```bash
python -m streamlit run dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501` or `http://localhost:8502`

## Data Requirements

The dashboard expects an Excel file with recruitment data containing columns such as:
- Requisition dates and status
- Business Unit, Department, Location
- Candidate information (gender, source, etc.)
- TAT metrics
- Interview and profile data

## Technologies

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive visualizations
- **OpenPyXL**: Excel file reading

## License

MIT
