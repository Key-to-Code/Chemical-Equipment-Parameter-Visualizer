# Chemical Equipment Visualizer - Desktop Application

This is the PyQt5 desktop application for the Chemical Equipment Parameter Visualizer.

## Installation

1. Install Python 3.11 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Make sure the Django backend is running on `http://localhost:8000`

2. Run the desktop application:
```bash
python main.py
```

## Features

- Upload CSV files with equipment data
- View summary statistics
- Display data in table format
- Visualize data with Matplotlib charts (bar charts and pie charts)
- Download PDF reports
- Browse last 5 uploaded datasets

## Usage

1. Click "Upload CSV File" to upload a new dataset
2. Select a dataset from the dropdown to view its details
3. Switch between tabs to see Summary, Data Table, and Charts
4. Click "Download PDF Report" to save a PDF report of the current dataset
