# Memristor Analysis

A Python-based desktop application for automated quantitative analysis of memristor Current–Voltage (I–V) characteristics and Pinched Hysteresis Loops (PHL).

The application is designed to automate numerical analysis of multi-cycle memristor I–V data, calculate PHL-based performance measures, visualize Voltage–Current loops, evaluate cycle-to-cycle variability, and generate structured Excel reports.

---

## Overview

Memristors exhibit nonlinear and history-dependent Current–Voltage characteristics. Under periodic excitation, these characteristics commonly form a Pinched Hysteresis Loop (PHL), which provides important information about switching behaviour.

The purpose of this project is to provide a reproducible computational framework for analysing such I–V characteristics using numerical integration and statistical measures.

The research framework uses the complete hysteresis loop rather than relying only on isolated switching points. Numerical integration is used because experimental and simulated I–V characteristics are generally available as discrete observations rather than as a closed-form mathematical function.

The associated research work describes the use of numerical integration, particularly Simpson's 1/3 rule, together with mean and standard-deviation functions to study memristor switching behaviour and cycle-to-cycle variability.

---

## Key Features

- Automated Voltage–Current pair detection
- No manual X/Y variable selection required
- Automatic analysis of all detected V–I cycles
- Pinched Hysteresis Loop visualization
- Multiple numerical integration methods
- Cycle-wise quantitative analysis
- Mean measurement across cycles
- Mean function calculation
- Variance and standard-deviation function calculation
- Cycle-to-cycle variability analysis
- Structured Excel report generation
- Desktop graphical user interface built with PySide6
- Modular service-based application architecture
- CSV and Excel dataset loading
- Research-oriented output structure

---

## Analysis Workflow

The application follows the general workflow:

```text
Input I–V Dataset
       │
       ▼
Dataset Loading
       │
       ▼
Automatic V–I Pair Detection
       │
       ▼
Cycle-wise PHL Analysis
       │
       ├── Vmax / Vmin
       ├── Imax / Imin
       ├── Rectangle Area
       ├── Lobe Areas
       ├── Loop Area
       ├── Symmetry
       └── Variability Measures
       │
       ▼
Mean Function
       │
       ▼
Variance / Standard Deviation Function
       │
       ▼
Results Visualization
       │
       ▼
Excel Report

The research methodology segments the complete PHL into four curves based on the direction of the voltage sweep and calculates the enclosed areas using numerical integration.

Input Dataset

The application is designed for datasets containing alternating Voltage and Current columns.

Example:

V1 | I1 | V2 | I2 | V3 | I3 | ... | Vn | In

where:

V1, V2, ..., Vn represent voltage measurements for individual cycles.
I1, I2, ..., In represent corresponding current measurements.
Each Voltage–Current pair represents one switching cycle.

Example:

V1    I1    V2    I2    V3    I3
------------------------------------
-3.0  ...   -3.0  ...   -3.0  ...
-2.9  ...   -2.9  ...   -2.9  ...
...
 3.0  ...    3.0  ...    3.0  ...

The application automatically detects Voltage–Current pairs and processes all valid pairs.

Manual selection of individual X and Y variables is not required.

Numerical Integration

The application provides three selectable integration methods:

Trapezoidal Rule
Simpson's 1/3 Rule
Simpson's 3/8 Rule

The research methodology uses numerical integration because PHLs generally do not follow a standard geometric form and discrete I–V observations require numerical methods for estimating the enclosed area.

Simpson's 1/3 rule is particularly important in the original research methodology and was used for calculating the areas of the segmented PHL curves.

Calculated Measures

The application calculates a range of quantitative measures for each Voltage–Current cycle.

Basic I–V Measures
Vmax

Maximum voltage observed in the cycle.

Vmin

Minimum voltage observed in the cycle.

Imax

Maximum current observed in the cycle.

Imin

Minimum current observed in the cycle.

Rectangle Area

The rectangular operating area is calculated from the voltage and current ranges:

Rectangle Area =
|Vmax - Vmin| × |Imax - Imin|

This corresponds to the axis-aligned rectangle enclosing the PHL.

PHL Area

The complete pinched hysteresis loop is divided into positive and negative regions and the enclosed areas are obtained from the corresponding curve segments.

The general concept is:

Positive Lobe Area
        +
Negative Lobe Area
        =
Total PHL Area

The research methodology calculates the enclosed area of each quadrant using absolute differences between the corresponding curve areas.

Lobe 1 and Lobe 2

The application separately evaluates the two major lobes of the hysteresis loop:

Lobe 1 Area
Lobe 2 Area

These measures provide information about the positive and negative regions of the PHL.

Lobe Length

The application estimates the geometric length of the two major loop lobes:

Lobe 1 Length
Lobe 2 Length

These lengths are subsequently used for normalized lobe-area measures.

Lobe Area per Unit Length

The application calculates normalized lobe-area measures:

Lobe 1 Area per Unit
Lobe 2 Area per Unit

These measures normalize the corresponding lobe area by its length and can assist with comparisons across different operating ranges.

Loop-to-Rectangle Area Ratio

The Loop-to-Rectangle Area Ratio is calculated as:

Loop Area / Rectangle Area

This provides a normalized measure of how much of the available voltage-current operating window is occupied by the hysteresis loop.

Symmetry Index

The Symmetry Index quantifies the relative difference between the positive and negative loop lobes.

A normalized symmetry measure provides information about the balance between the two sides of the PHL.

Cycle-to-Cycle Variability

A major component of the application is the evaluation of variability between different switching cycles.

For a given voltage point, the current values from multiple cycles are compared with their corresponding mean current.

The application calculates:

Variation
Standard Deviation
Standard Deviation per Unit Area

The methodology considers the current response at corresponding voltage points across cycles.

Mean Function

The Mean Function represents the point-wise average current response across the available switching cycles.

Conceptually:

Mean Current at point t
=
Average of current values at point t across cycles

This produces a representative mean I–V behaviour for the dataset.

Variance and Standard Deviation Function

The application also evaluates point-wise variability across switching cycles.

The Standard Deviation Function indicates how much the current response varies from the mean response at each corresponding point.

This allows localized variability to be examined instead of relying only on one overall variability value.

Application Outputs

The application produces four principal analytical outputs.

1. Cycles

Contains cycle-wise measurements.

Example measures include:

Vmax
Vmin
Imax
Imin
Rectangle Area
Lobe 1 Length
Lobe 2 Length
PHL Area
Loop to Rectangle Ratio
Lobe 1 Area
Lobe 2 Area
Lobe 1 Area per Unit
Lobe 2 Area per Unit
Symmetry Index
Variation
SD Per Unit Area
2. Measure

Contains the mean value of the calculated cycle-wise measurements.

This provides a compact summary of the analytical measures across all processed cycles.

3. Mean Function

Contains the point-wise mean Voltage and mean Current/loop response across cycles.

This output is used to represent the typical behaviour of the switching cycles.

4. Variance Function

Contains point-wise variability information, including sample variance and sample standard deviation.

Excel Report

The application can export the analysis results into an Excel workbook.

The generated workbook contains:

Cycles
Measure
mean Function
Variance function

This structure is intended to preserve the research-oriented organization of the analysis results.

Visualization

The application provides a dedicated V–I Loop visualization.

The visualization allows the user to inspect the detected Voltage–Current cycles together and examine the shape of the corresponding hysteresis loops.

The PHL is a central component of the research methodology because loop shape, area, symmetry and cycle-to-cycle variability are used to characterize memristive behaviour.

Graphical User Interface

The desktop application is developed using:

Python
PySide6
Pandas
NumPy
OpenPyXL

The GUI provides separate sections for:

Dashboard
Data
Analysis
Results
Reports
Settings

The interface is designed to minimize manual configuration and automate the complete analysis workflow.

Project Architecture

The project follows a modular architecture separating user-interface components from data handling and numerical analysis.

MemristorAnalysis/
│
├── .gitignore
├── README.md
├── requirements.txt
│
└── src/
    └── memristor_app/
        │
        ├── __init__.py
        ├── main.py
        │
        ├── services/
        │   ├── __init__.py
        │   ├── data_service.py
        │   └── integration_service.py
        │
        └── ui/
            ├── __init__.py
            ├── analysis_page.py
            ├── main_window.py
            └── memristor_plot.py
Main Components
main.py

Application entry point.

data_service.py

Responsible for dataset loading and basic dataset information.

Supported input formats include:

.xlsx
.xls
.csv
integration_service.py

Contains the numerical integration methods and the core memristor analysis logic.

analysis_page.py

Provides the analysis configuration interface and automatic V–I pair detection.

main_window.py

Controls the main application window, navigation, results display and report export workflow.

memristor_plot.py

Provides V–I loop visualization within the desktop application.

Installation
1. Clone the repository
git clone https://github.com/maheshmore19032002-debug/MemristorAnalysis-Dongale_Pawar_Measures-.git

Move into the project directory:

cd MemristorAnalysis-Dongale_Pawar_Measures-
2. Create a Virtual Environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
Running the Application

The project uses a src layout.

From the project root:

$env:PYTHONPATH="src"
python -m memristor_app.main

The application will start as a desktop GUI.

Dataset Preparation

For automated analysis, organize the I–V data in alternating Voltage–Current pairs.

Recommended structure:

V1 | I1 | V2 | I2 | V3 | I3 | ...

The voltage and current measurements corresponding to each cycle should have the same number of observations.

For example:

Voltage Cycle 1 → V1
Current Cycle 1 → I1

Voltage Cycle 2 → V2
Current Cycle 2 → I2

Voltage Cycle 3 → V3
Current Cycle 3 → I3

The application automatically detects valid pairs and processes them.

Research Context

This software was developed in connection with the research project:

Quantifying Memristor Performance: Novel Metrics for Absolute and Comparative Evaluation

The research project was submitted to the Department of Statistics, Shivaji University, Kolhapur, as partial fulfilment for the Master of Science in Statistics.

The research framework focuses on quantitative evaluation of memristive devices using PHL-derived measures, numerical integration and functional analysis of repeated switching cycles.

Research Dataset

The research report describes an application of the methodology to I–V data from:

10 memristor devices
10 switching cycles per device

The reported framework is intended to be applicable more broadly to multi-cycle memristive I–V datasets.

The application itself does not require the user to hard-code a fixed number of cycles.

Reproducibility

The project aims to provide a reproducible computational workflow by:

Separating data loading from numerical analysis
Providing explicit integration-method selection
Automatically detecting V–I pairs
Processing all detected cycles
Producing structured outputs
Exporting results to Excel
Keeping the numerical analysis logic in a dedicated service module

For research use, users should retain the original dataset and document the selected integration method and analysis settings used for each experiment.

Limitations

The current version is designed primarily for structured multi-cycle I–V datasets.

Users should ensure that:

Voltage and current columns are correctly paired.
Data points within a cycle are ordered consistently.
The dataset represents comparable switching cycles.
Missing or invalid numerical observations are handled before analysis.
Results are interpreted within the physical and experimental context of the corresponding memristive device.

The software provides numerical and statistical measurements; interpretation of device physics should be performed together with the experimental conditions and underlying device characteristics.

Future Development

Potential future development includes:

Browser-based web application
Online deployment
Interactive Plotly-based visualizations
Additional statistical analysis
Batch analysis of multiple datasets
Comparative device analysis
Automated research report generation
Advanced PHL visualization
Configuration and experiment metadata management
Reproducible analysis configuration files
Research-oriented benchmarking workflows
Citation

If this software or the associated methodology is used in academic or research work, please cite the associated research project and acknowledge the software implementation.

Research Project

Quantifying Memristor Performance: Novel Metrics for Absolute and Comparative Evaluation

Department of Statistics, Shivaji University, Kolhapur.

Authors

Mahesh Manohar More

Pallavi Shejwal Ananda

Under the guidance of:

Dr. S. D. Pawar

Department of Statistics
Shivaji University, Kolhapur

References

The associated research report cites foundational and related literature on memristors, memristive systems, hysteresis-loop analysis and resistive switching, including:

Chua, L. O. (1971). Memristor—The missing circuit element. IEEE Transactions on Circuit Theory, 18(5), 507–519.
Strukov, D. B., Snider, G. S., Stewart, D. R., & Williams, R. S. (2008). The missing memristor found. Nature, 453(7191), 80–83.
Chua, L. (2019). Everything you wish to know about memristors but are afraid to ask. Handbook of Memristor Networks.
Zidan, M. A., Strachan, J. P., & Lu, W. D. (2018). The future of electronics based on memristive systems. Nature Electronics, 1(1), 22–29.
Biolek, Z., Biolek, D., & Biolkova, V. (2013). Analytical computation of the area of pinched hysteresis loops of ideal mem-elements. Radioengineering, 22(1), 132–135.
Biolek, D., Biolek, Z., & Biolková, V. (2014). Interpreting area of pinched memristor hysteresis loop. Electronics Letters, 50(2), 74–75.
Thorat, P. S., Kumbhar, D. D., Oval, R. D., Kumar, S., Awale, M., Ramanathan, T. V., ... & Sutar, S. S. (2025). On the time series analysis of resistive switching devices. Microelectronic Engineering, 297, 112306.