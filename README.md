do.
# Memristor Analysis

A Python-based analytical application for quantitative analysis of memristor Voltage–Current (V–I) characteristics.

The project provides both:

- 🖥️ A desktop application using PySide6
- 🌐 A web application using Streamlit

The application automatically detects Voltage–Current column pairs and performs numerical analysis across all available cycles without requiring manual X/Y variable selection.

---

## 🚀 Live Web Application

**Memristor Analysis — Live App**

https://maheshmore19032002-debug-memristoranalysis-dongal-webapp-qzkgk2.streamlit.app/

The web application allows users to upload their memristor dataset directly through a browser and perform the analysis without installing the desktop application.

---

## 📌 Project Overview

Memristor devices exhibit nonlinear Voltage–Current characteristics and hysteresis behavior. Quantitative analysis of these characteristics can provide useful measures for evaluating switching behavior, hysteresis, symmetry, variation, and related electrical properties.

This project implements a computational framework for analyzing multiple Voltage–Current cycles using numerical integration and derived quantitative metrics.

The application was developed as part of research work related to quantitative memristor characterization.

---

## ✨ Key Features

### Automatic Dataset Processing

- Supports Excel (`.xlsx`, `.xls`) and CSV (`.csv`) datasets
- Automatically detects Voltage–Current column pairs
- Processes all detected V–I cycles
- No manual X/Y column selection required
- Dynamically adapts to the number of available V–I pairs

### Numerical Integration

The application supports:

- Trapezoidal Rule
- Simpson's 1/3 Rule
- Simpson's 3/8 Rule

### Quantitative Metrics

The analysis includes:

- Vmax
- Vmin
- Imax
- Imin
- Rectangle Area
- Lobe 1 Length (L1)
- Lobe 1 Length (L2)
- PHL Area
- Loop-to-Rectangle Ratio
- Lobe 1 Area
- Lobe 2 Area
- Lobe 1 Area per Unit
- Lobe 2 Area per Unit
- Symmetry Index
- Variation
- SD per Unit Area

### Generated Results

The application produces four main analytical outputs:

1. **Cycles**  
   Cycle-wise measurements for every detected V–I pair.

2. **Measure**  
   Mean values of the cycle-wise measurements.

3. **Mean Function**  
   Row-wise mean Voltage and Mean Loop values.

4. **Variance Function**  
   Row-wise sample variance and sample standard deviation.

### Visualization

The application provides an interactive V–I loop visualization for the detected cycles.

### Excel Export

The analysis results can be exported as an Excel workbook containing:

- `Cycles`
- `Measure`
- `mean Function`
- `Variance function`

---

## 🏗️ Project Architecture

The project follows a modular architecture separating the user interface, data handling, and analytical logic.

```text
MemristorAnalysis/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/
│   └── memristor_app/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   ├── data_service.py
│       │   └── integration_service.py
│       │
│       └── ui/
│           ├── __init__.py
│           ├── analysis_page.py
│           ├── main_window.py
│           └── memristor_plot.py
│
└── web/
    └── app.py

Main Components
data_service.py
Responsible for:
- Dataset loading
- File validation
- Excel/CSV handling
- Dataset information
integration_service.py
Contains the core numerical analysis, including:
- Numerical integration
- Cycle processing
- Memristor metric calculation
- Statistical calculations
- Result generation
analysis_page.py
Provides the desktop analysis configuration interface.
main_window.py
Controls the main desktop application interface, navigation, results, and report export.
memristor_plot.py
Provides V–I loop visualization for the desktop application.
web/app.py
Provides the Streamlit web interface while reusing the same analytical services used by the desktop application.
📊 Input Dataset Structure
The application is designed for datasets containing alternating Voltage and Current columns.
Example:
V1 | I1 | V2 | I2 | V3 | I3 | ...

Where:
- V1, V2, V3, ... represent Voltage measurements
- I1, I2, I3, ... represent corresponding Current measurements
Each Voltage–Current pair is treated as an individual cycle.
The application automatically detects the available pairs rather than requiring the user to manually select them.
🔬 Analysis Workflow
The general workflow is:
Dataset
   │
   ▼
File Loading
   │
   ▼
Automatic V–I Pair Detection
   │
   ▼
Numerical Integration
   │
   ▼
Cycle-wise Metric Calculation
   │
   ▼
Statistical Aggregation
   │
   ├───────────────┐
   ▼               ▼
Cycle Results   Mean Results
   │
   ├───────────────┐
   ▼               ▼
Mean Function   Variance Function
   │
   ▼
V–I Visualization
   │
   ▼
Excel Report

💻 Desktop Application
Requirements
The desktop application requires Python and the project dependencies.
Recommended Python environment:
Python 3.11+

Installation
Clone the repository:
git clone https://github.com/maheshmore19032002-debug/MemristorAnalysis-Dongale_Pawar_Measures-.git

Move into the project directory:
cd MemristorAnalysis-Dongale_Pawar_Measures-

Create a virtual environment:
python -m venv .venv

Activate the environment on Windows:
.venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run Desktop Application
Set the source directory as the Python path:
$env:PYTHONPATH="src"

Then run:
python -m memristor_app.main

🌐 Web Application
The web version is implemented using Streamlit.
Run Locally
From the project root:
streamlit run web/app.py

The application will open in the browser.
Online Version
The deployed application is available at:
https://maheshmore19032002-debug-memristoranalysis-dongal-webapp-qzkgk2.streamlit.app/
📦 Dependencies
The project uses the following main Python packages:
- NumPy
- Pandas
- OpenPyXL
- PySide6
- Streamlit
- Plotly
The complete dependency list is available in:
requirements.txt

📁 Output Structure
The generated Excel report contains four worksheets:
Analysis Report
│
├── Cycles
├── Measure
├── mean Function
└── Variance function

Cycles
Contains individual cycle-wise analytical measurements.
Measure
Contains the mean of the cycle-wise metrics.
Mean Function
Contains row-wise mean Voltage and Mean Loop values.
Variance Function
Contains row-wise sample variance and sample standard deviation.
🔎 Automatic V–I Pair Detection
The application is designed to work dynamically with different numbers of cycles.
For example, datasets such as:
V1 | I1 | V2 | I2

or:
V1 | I1 | V2 | I2 | V3 | I3 | V4 | I4 | V5 | I5

can be processed without changing the analysis code.
The application does not permanently assume a fixed number of cycles.
📈 Visualization
The web application provides an interactive V–I plot using Plotly.
The visualization allows the user to inspect the detected Voltage–Current loops and compare the available cycles visually.
🧪 Research Context
The analytical framework is based on quantitative evaluation of memristor hysteresis and related V–I characteristics.
The project includes measures related to:
- Hysteresis/loop area
- Geometric reference area
- Lobe areas
- Symmetry
- Variation
- Standard deviation
- Normalized measures
Numerical integration is used to estimate relevant areas from the experimental V–I data.
🛠️ Design Principles
The application was developed with the following principles:
- Correctness of numerical calculations
- Modular architecture
- Separation of UI and analytical logic
- Reusable analysis services
- Dynamic dataset handling
- Minimal manual configuration
- Clear analytical outputs
- Reproducible workflow
- Maintainable project structure
🔐 Data and Privacy
The application does not require users to manually modify the source code to analyze a dataset.
For sensitive or unpublished research data, users should consider using the desktop application locally rather than uploading confidential datasets to a public web deployment.
📜 License
This project is currently maintained as a research and academic software project.
License terms can be added when the project is prepared for formal open-source distribution.
👨‍🔬 Research / Development
Project: Memristor Analysis
Application Type: Numerical Analysis and Visualization
Domain: Memristor / Electrical Device Characterization
Technology: Python
Desktop GUI: PySide6
Web Framework: Streamlit
Data Analysis: Pandas, NumPy
Visualization: Plotly
🔗 Project Links
GitHub Repository
https://github.com/maheshmore19032002-debug/MemristorAnalysis-Dongale_Pawar_Measures-
Live Web Application
https://maheshmore19032002-debug-memristoranalysis-dongal-webapp-qzkgk2.streamlit.app/