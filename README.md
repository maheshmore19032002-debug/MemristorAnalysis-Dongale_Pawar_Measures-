# Memristor Analysis

A Python-based desktop application for numerical analysis of memristor experimental Voltage–Current data.

## Features

- Excel and CSV dataset loading
- Automatic Voltage–Current pair detection
- Automatic processing of all detected V-I cycles
- Numerical integration methods:
  - Trapezoidal Rule
  - Simpson's 1/3 Rule
  - Simpson's 3/8 Rule
- Cycle-wise memristor measurements
- Mean and variance analysis
- Memristor V-I loop visualization
- Research-oriented Excel report generation
- No manual X/Y variable selection required

## Analysis Outputs

The application generates:

1. Cycles
2. Measure
3. Mean Function
4. Variance Function

The analysis includes metrics such as:

- Vmax
- Vmin
- Imax
- Imin
- Rectangle Area
- Lobe 1 Length
- Lobe 2 Length
- PHL Area
- Loop to Rectangle Ratio
- Lobe 1 Area
- Lobe 2 Area
- Lobe 1 Area per Unit
- Lobe 2 Area per Unit
- Symmetry Index
- Variation
- SD Per Unit Area

## Project Structure

```text
MemristorAnalysis
│
├── src
│   └── memristor_app
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── services
│       │   ├── __init__.py
│       │   ├── data_service.py
│       │   └── integration_service.py
│       │
│       └── ui
│           ├── __init__.py
│           ├── analysis_page.py
│           ├── main_window.py
│           └── memristor_plot.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── main.py