from pathlib import Path

import numpy as np
import pandas as pd

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
    QTabWidget,
    QAbstractItemView,
)

from memristor_app.services.data_service import DataService
from memristor_app.services.integration_service import IntegrationService
from memristor_app.ui.analysis_page import AnalysisPage
from memristor_app.ui.memristor_plot import MemristorPlotWidget


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Memristor Analysis")
        self.resize(1200, 800)

        # ---------------------------------------------------------
        # Application data
        # ---------------------------------------------------------

        self.selected_file: str | None = None
        self.dataframe = None

        self.df1 = None
        self.stats_df1 = None
        self.mean = None
        self.var = None

        self.current_method = None

        self.data_service = DataService()

        self.setup_ui()

    # =============================================================
    # MAIN UI
    # =============================================================

    def setup_ui(self) -> None:

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f5f7fa;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 14px;
            }

            QFrame#sidebar {
                background-color: #172033;
                border: none;
            }

            QLabel#app_title {
                color: white;
                font-size: 24px;
                font-weight: 700;
            }

            QLabel#app_subtitle {
                color: #9ca8bb;
                font-size: 12px;
            }

            QListWidget#navigation {
                background-color: transparent;
                border: none;
                outline: none;
            }

            QListWidget#navigation::item {
                color: #cbd5e1;
                padding: 14px 16px;
                margin: 3px 0;
                border-radius: 8px;
            }

            QListWidget#navigation::item:selected {
                background-color: #2d3b55;
                color: white;
            }

            QListWidget#navigation::item:hover {
                background-color: #25324a;
            }

            QFrame#content_area {
                background-color: #f5f7fa;
            }

            QLabel#page_title {
                color: #172033;
                font-size: 28px;
                font-weight: 700;
            }

            QLabel#welcome_label {
                color: #172033;
                font-size: 30px;
                font-weight: 700;
            }

            QLabel#description_label {
                color: #64748b;
                font-size: 14px;
            }

            QFrame#info_card {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }

            QLabel#card_title {
                color: #172033;
                font-size: 16px;
                font-weight: 600;
            }

            QLabel#card_value {
                color: #172033;
                font-size: 22px;
                font-weight: 700;
            }

            QLabel#result_card_title {
                color: #64748b;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#result_card_value {
                color: #172033;
                font-size: 19px;
                font-weight: 700;
            }

            QLabel#placeholder_label {
                color: #64748b;
                font-size: 14px;
            }

            QLabel#version_label {
                color: #64748b;
                font-size: 12px;
            }

            QLabel#results_hint {
                color: #64748b;
                font-size: 13px;
            }

            QPushButton#primary_button {
                background-color: #2563eb;
                color: white;
                border: none;
                border-radius: 7px;
                padding: 10px 18px;
                font-weight: 600;
            }

            QPushButton#primary_button:hover {
                background-color: #1d4ed8;
            }

            QPushButton#primary_button:pressed {
                background-color: #1e40af;
            }

            QPushButton#secondary_button {
                background-color: white;
                color: #2563eb;
                border: 1px solid #2563eb;
                border-radius: 7px;
                padding: 10px 18px;
                font-weight: 600;
            }

            QPushButton#secondary_button:hover {
                background-color: #eff6ff;
            }

            QTableWidget#preview_table {
                background-color: white;
                border: 1px solid #e2e8f0;
                gridline-color: #e2e8f0;
                selection-background-color: #dbeafe;
                selection-color: #172033;
            }

            QTableWidget#result_table {
                background-color: white;
                border: 1px solid #e2e8f0;
                gridline-color: #e2e8f0;
                selection-background-color: #dbeafe;
                selection-color: #172033;
                alternate-background-color: #f8fafc;
            }

            QTabWidget::pane {
                background-color: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }

            QTabBar::tab {
                background-color: #e2e8f0;
                color: #334155;
                padding: 10px 18px;
                margin-right: 2px;
            }

            QTabBar::tab:selected {
                background-color: #2563eb;
                color: white;
            }

            QHeaderView::section {
                background-color: #f1f5f9;
                color: #334155;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e2e8f0;
                font-weight: 600;
            }
            """
        )

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QHBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # =========================================================
        # SIDEBAR
        # =========================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(235)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(
            18,
            25,
            18,
            20,
        )
        sidebar_layout.setSpacing(8)

        title = QLabel("Memristor")
        title.setObjectName("app_title")

        subtitle = QLabel("Analysis Platform")
        subtitle.setObjectName("app_subtitle")

        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)

        sidebar_layout.addSpacing(25)

        self.navigation = QListWidget()
        self.navigation.setObjectName("navigation")

        navigation_items = [
            "Dashboard",
            "Data",
            "Analysis",
            "Results",
            "Reports",
            "Settings",
        ]

        for item_text in navigation_items:

            self.navigation.addItem(
                QListWidgetItem(item_text)
            )

        self.navigation.setCurrentRow(0)

        self.navigation.currentRowChanged.connect(
            self.change_page
        )

        sidebar_layout.addWidget(
            self.navigation
        )

        sidebar_layout.addStretch()

        version = QLabel("Version 1.0.0")
        version.setObjectName("version_label")

        sidebar_layout.addWidget(version)

        # =========================================================
        # CONTENT
        # =========================================================

        content_area = QFrame()
        content_area.setObjectName("content_area")

        content_layout = QVBoxLayout(
            content_area
        )
        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.pages = QStackedWidget()

        # Pages
        self.dashboard_page = (
            self.create_dashboard_page()
        )

        self.data_page = (
            self.create_data_page()
        )

        self.analysis_page = AnalysisPage()

        self.analysis_page.run_analysis_requested.connect(
            self.handle_analysis_request
        )

        self.results_page = (
            self.create_results_page()
        )

        self.reports_page = (
            self.create_reports_page()
        )

        self.settings_page = (
            self.create_placeholder_page(
                "Settings",
                "Application settings will be available here.",
            )
        )

        self.pages.addWidget(
            self.dashboard_page
        )

        self.pages.addWidget(
            self.data_page
        )

        self.pages.addWidget(
            self.analysis_page
        )

        self.pages.addWidget(
            self.results_page
        )

        self.pages.addWidget(
            self.reports_page
        )

        self.pages.addWidget(
            self.settings_page
        )

        content_layout.addWidget(
            self.pages
        )

        root_layout.addWidget(sidebar)
        root_layout.addWidget(content_area)

    # =============================================================
    # DASHBOARD
    # =============================================================

    def create_dashboard_page(self) -> QWidget:

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )
        layout.setSpacing(20)

        welcome = QLabel(
            "Welcome to Memristor Analysis"
        )

        welcome.setObjectName(
            "welcome_label"
        )

        description = QLabel(
            "Load your dataset, perform automatic "
            "Voltage–Current cycle analysis, "
            "and generate research-ready results."
        )

        description.setObjectName(
            "description_label"
        )

        description.setWordWrap(True)

        layout.addWidget(welcome)
        layout.addWidget(description)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        self.dataset_card = (
            self.create_info_card(
                "Dataset",
                "No file loaded",
            )
        )

        self.analysis_status_card = (
            self.create_info_card(
                "Analysis",
                "Not started",
            )
        )

        self.method_status_card = (
            self.create_info_card(
                "Method",
                "Not selected",
            )
        )

        cards_layout.addWidget(
            self.dataset_card
        )

        cards_layout.addWidget(
            self.analysis_status_card
        )

        cards_layout.addWidget(
            self.method_status_card
        )

        layout.addLayout(
            cards_layout
        )

        layout.addStretch()

        return page

    # =============================================================
    # DATA PAGE
    # =============================================================

    def create_data_page(self) -> QWidget:

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        layout.setSpacing(20)

        title = QLabel("Dataset")
        title.setObjectName(
            "page_title"
        )

        description = QLabel(
            "Load an Excel or CSV dataset for analysis."
        )

        description.setObjectName(
            "description_label"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        # ---------------------------------------------------------
        # File card
        # ---------------------------------------------------------

        file_card = QFrame()
        file_card.setObjectName(
            "info_card"
        )

        file_layout = QVBoxLayout(
            file_card
        )

        file_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        file_layout.setSpacing(12)

        file_title = QLabel(
            "Dataset File"
        )

        file_title.setObjectName(
            "card_title"
        )

        self.file_label = QLabel(
            "No file selected"
        )

        self.file_label.setObjectName(
            "placeholder_label"
        )

        browse_button = QPushButton(
            "Browse File"
        )

        browse_button.setObjectName(
            "primary_button"
        )

        browse_button.clicked.connect(
            self.select_data_file
        )

        file_layout.addWidget(
            file_title
        )

        file_layout.addWidget(
            self.file_label
        )

        file_layout.addWidget(
            browse_button
        )

        layout.addWidget(
            file_card
        )

        # ---------------------------------------------------------
        # Information cards
        # ---------------------------------------------------------

        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)

        self.rows_card = (
            self.create_info_card(
                "Rows",
                "0",
            )
        )

        self.columns_card = (
            self.create_info_card(
                "Columns",
                "0",
            )
        )

        self.status_card = (
            self.create_info_card(
                "Status",
                "Not loaded",
            )
        )

        info_layout.addWidget(
            self.rows_card
        )

        info_layout.addWidget(
            self.columns_card
        )

        info_layout.addWidget(
            self.status_card
        )

        layout.addLayout(
            info_layout
        )

        # ---------------------------------------------------------
        # Preview
        # ---------------------------------------------------------

        preview_title = QLabel(
            "Data Preview"
        )

        preview_title.setObjectName(
            "card_title"
        )

        layout.addWidget(
            preview_title
        )

        self.preview_table = QTableWidget()

        self.preview_table.setObjectName(
            "preview_table"
        )

        self.preview_table.setAlternatingRowColors(
            True
        )

        self.preview_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.preview_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )

        self.preview_table.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self.preview_table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        self.preview_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        layout.addWidget(
            self.preview_table
        )

        return page

    # =============================================================
    # RESULTS PAGE
    # =============================================================

    def create_results_page(self) -> QWidget:

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            30,
            25,
            30,
            25,
        )

        layout.setSpacing(12)

        title = QLabel(
            "Analysis Results"
        )

        title.setObjectName(
            "page_title"
        )

        description = QLabel(
            "Complete results generated from all "
            "Voltage–Current cycles."
        )

        description.setObjectName(
            "description_label"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        # =========================================================
        # SUMMARY CARDS
        # =========================================================

        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(12)

        self.result_cycles_card = (
            self.create_result_summary_card(
                "Cycles Processed",
                "—",
            )
        )

        self.result_method_card = (
            self.create_result_summary_card(
                "Integration Method",
                "—",
            )
        )

        self.result_phl_card = (
            self.create_result_summary_card(
                "Mean PHL Area",
                "—",
            )
        )

        self.result_ratio_card = (
            self.create_result_summary_card(
                "Mean Loop / Rectangle",
                "—",
            )
        )

        summary_layout.addWidget(
            self.result_cycles_card
        )

        summary_layout.addWidget(
            self.result_method_card
        )

        summary_layout.addWidget(
            self.result_phl_card
        )

        summary_layout.addWidget(
            self.result_ratio_card
        )

        layout.addLayout(
            summary_layout
        )

        hint = QLabel(
            "Use the tabs below to inspect cycle-wise "
            "measurements, summary measures, mean functions, "
            "variance functions, and V–I loop plots."
        )

        hint.setObjectName(
            "results_hint"
        )

        layout.addWidget(
            hint
        )

        # =========================================================
        # RESULT TABS
        # =========================================================

        self.result_tabs = QTabWidget()

        # ---------------------------------------------------------
        # Cycles
        # ---------------------------------------------------------

        self.cycles_table = QTableWidget()

        self.cycles_table.setObjectName(
            "result_table"
        )

        self.setup_result_table(
            self.cycles_table
        )

        self.result_tabs.addTab(
            self.cycles_table,
            "Cycles",
        )

        # ---------------------------------------------------------
        # Measure
        # ---------------------------------------------------------

        self.measure_table = QTableWidget()

        self.measure_table.setObjectName(
            "result_table"
        )

        self.setup_result_table(
            self.measure_table
        )

        self.result_tabs.addTab(
            self.measure_table,
            "Measure",
        )

        # ---------------------------------------------------------
        # Mean Function
        # ---------------------------------------------------------

        self.mean_table = QTableWidget()

        self.mean_table.setObjectName(
            "result_table"
        )

        self.setup_result_table(
            self.mean_table
        )

        self.result_tabs.addTab(
            self.mean_table,
            "Mean Function",
        )

        # ---------------------------------------------------------
        # Variance Function
        # ---------------------------------------------------------

        self.variance_table = QTableWidget()

        self.variance_table.setObjectName(
            "result_table"
        )

        self.setup_result_table(
            self.variance_table
        )

        self.result_tabs.addTab(
            self.variance_table,
            "Variance Function",
        )

        # ---------------------------------------------------------
        # V-I Loop Plot
        # ---------------------------------------------------------

        self.loop_plot = (
            MemristorPlotWidget()
        )

        self.result_tabs.addTab(
            self.loop_plot,
            "V–I Loops",
        )

        layout.addWidget(
            self.result_tabs,
            1,
        )

        # =========================================================
        # BOTTOM STATUS + EXPORT
        # =========================================================

        button_layout = QHBoxLayout()

        self.results_status = QLabel(
            "No analysis results available."
        )

        self.results_status.setObjectName(
            "placeholder_label"
        )

        button_layout.addWidget(
            self.results_status
        )

        button_layout.addStretch()

        self.export_button = QPushButton(
            "Export Excel Report"
        )

        self.export_button.setObjectName(
            "primary_button"
        )

        self.export_button.clicked.connect(
            self.export_results
        )

        self.export_button.setEnabled(
            False
        )

        button_layout.addWidget(
            self.export_button
        )

        layout.addLayout(
            button_layout
        )

        return page

    # =============================================================
    # RESULT SUMMARY CARD
    # =============================================================

    def create_result_summary_card(
        self,
        title_text: str,
        value_text: str,
    ) -> QFrame:

        card = QFrame()

        card.setObjectName(
            "info_card"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            16,
            13,
            16,
            13,
        )

        layout.setSpacing(4)

        title = QLabel(
            title_text
        )

        title.setObjectName(
            "result_card_title"
        )

        value = QLabel(
            value_text
        )

        value.setObjectName(
            "result_card_value"
        )

        value.setWordWrap(True)

        layout.addWidget(
            title
        )

        layout.addWidget(
            value
        )

        card.setProperty(
            "result_card_value_label",
            value,
        )

        return card

    def set_result_card_value(
        self,
        card: QFrame,
        value: str,
    ) -> None:

        label = card.property(
            "result_card_value_label"
        )

        if label:
            label.setText(
                value
            )

    # =============================================================
    # REPORT PAGE
    # =============================================================

    def create_reports_page(self) -> QWidget:

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        layout.setSpacing(20)

        title = QLabel(
            "Reports"
        )

        title.setObjectName(
            "page_title"
        )

        description = QLabel(
            "Export the complete memristor analysis "
            "as an Excel workbook."
        )

        description.setObjectName(
            "description_label"
        )

        layout.addWidget(title)
        layout.addWidget(description)

        card = QFrame()

        card.setObjectName(
            "info_card"
        )

        card_layout = QVBoxLayout(
            card
        )

        card_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        card_layout.setSpacing(15)

        card_title = QLabel(
            "Excel Report"
        )

        card_title.setObjectName(
            "card_title"
        )

        card_text = QLabel(
            "The report contains four worksheets:\n\n"
            "• Cycles — cycle-wise measurements\n"
            "• Measure — mean measurements\n"
            "• mean Function — mean Voltage and Mean loop\n"
            "• Variance function — sample variance and "
            "sample standard deviation"
        )

        card_text.setObjectName(
            "placeholder_label"
        )

        card_text.setWordWrap(True)

        report_button = QPushButton(
            "Download Excel Report"
        )

        report_button.setObjectName(
            "primary_button"
        )

        report_button.clicked.connect(
            self.export_results
        )

        self.report_button = (
            report_button
        )

        self.report_button.setEnabled(
            False
        )

        card_layout.addWidget(
            card_title
        )

        card_layout.addWidget(
            card_text
        )

        card_layout.addWidget(
            report_button
        )

        layout.addWidget(card)
        layout.addStretch()

        return page

    # =============================================================
    # RESULT TABLE SETUP
    # =============================================================

    def setup_result_table(
        self,
        table: QTableWidget,
    ) -> None:

        table.setAlternatingRowColors(
            True
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectItems
        )

        table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        table.setSortingEnabled(
            True
        )

        table.setWordWrap(
            False
        )

        table.setHorizontalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        table.setVerticalScrollMode(
            QAbstractItemView.ScrollMode.ScrollPerPixel
        )

        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        table.horizontalHeader().setStretchLastSection(
            False
        )

        table.verticalHeader().setDefaultSectionSize(
            30
        )

        table.verticalHeader().setVisible(
            False
        )

    # =============================================================
    # PLACEHOLDER PAGE
    # =============================================================

    def create_placeholder_page(
        self,
        title_text: str,
        description_text: str,
    ) -> QWidget:

        page = QWidget()

        layout = QVBoxLayout(page)

        layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        layout.setSpacing(15)

        title = QLabel(
            title_text
        )

        title.setObjectName(
            "page_title"
        )

        description = QLabel(
            description_text
        )

        description.setObjectName(
            "description_label"
        )

        description.setWordWrap(True)

        layout.addWidget(title)
        layout.addWidget(description)

        placeholder = QLabel(
            "This section is under development."
        )

        placeholder.setObjectName(
            "placeholder_label"
        )

        layout.addWidget(
            placeholder
        )

        layout.addStretch()

        return page

    # =============================================================
    # INFORMATION CARD
    # =============================================================

    def create_info_card(
        self,
        title_text: str,
        value_text: str,
    ) -> QFrame:

        card = QFrame()

        card.setObjectName(
            "info_card"
        )

        layout = QVBoxLayout(card)

        layout.setContentsMargins(
            20,
            18,
            20,
            18,
        )

        layout.setSpacing(6)

        title = QLabel(
            title_text
        )

        title.setObjectName(
            "card_title"
        )

        value = QLabel(
            value_text
        )

        value.setObjectName(
            "card_value"
        )

        value.setWordWrap(True)

        layout.addWidget(
            title
        )

        layout.addWidget(
            value
        )

        card.setProperty(
            "card_value_label",
            value,
        )

        return card

    def set_card_value(
        self,
        card: QFrame,
        value: str,
    ) -> None:

        label = card.property(
            "card_value_label"
        )

        if label:
            label.setText(
                value
            )

    # =============================================================
    # FILE LOADING
    # =============================================================

    def select_data_file(self) -> None:

        file_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Select Dataset",
                "",
                (
                    "Data Files (*.xlsx *.xls *.csv);;"
                    "Excel Files (*.xlsx *.xls);;"
                    "CSV Files (*.csv)"
                ),
            )
        )

        if not file_path:
            return

        try:

            dataframe = (
                self.data_service.load_file(
                    file_path
                )
            )

            info = (
                self.data_service
                .get_dataset_info(
                    dataframe
                )
            )

            self.selected_file = (
                file_path
            )

            self.dataframe = (
                dataframe
            )

            # -----------------------------------------------------
            # Clear previous analysis
            # -----------------------------------------------------

            self.df1 = None
            self.stats_df1 = None
            self.mean = None
            self.var = None
            self.current_method = None

            # -----------------------------------------------------
            # File information
            # -----------------------------------------------------

            file_name = Path(
                file_path
            ).name

            self.file_label.setText(
                file_name
            )

            self.set_card_value(
                self.rows_card,
                str(info["rows"]),
            )

            self.set_card_value(
                self.columns_card,
                str(info["columns"]),
            )

            self.set_card_value(
                self.status_card,
                "Loaded",
            )

            self.set_card_value(
                self.dataset_card,
                file_name,
            )

            self.set_card_value(
                self.analysis_status_card,
                "Not started",
            )

            self.set_card_value(
                self.method_status_card,
                "Not selected",
            )

            # -----------------------------------------------------
            # Reset result summary
            # -----------------------------------------------------

            self.reset_result_summary()

            # -----------------------------------------------------
            # Give dataset to Analysis page
            # -----------------------------------------------------

            self.analysis_page.set_dataframe(
                dataframe
            )

            # -----------------------------------------------------
            # Prepare plot
            # -----------------------------------------------------

            self.loop_plot.set_dataframe(
                dataframe
            )

            # -----------------------------------------------------
            # Preview
            # -----------------------------------------------------

            self.show_data_preview(
                dataframe
            )

            # -----------------------------------------------------
            # Reset result status
            # -----------------------------------------------------

            self.results_status.setText(
                "No analysis results available."
            )

            self.export_button.setEnabled(
                False
            )

            self.report_button.setEnabled(
                False
            )

        except Exception as error:

            self.set_card_value(
                self.status_card,
                "Error",
            )

            QMessageBox.critical(
                self,
                "Dataset Error",
                (
                    "The dataset could not be loaded."
                    "\n\n"
                    f"Reason:\n{error}"
                ),
            )

    # =============================================================
    # RESET RESULT SUMMARY
    # =============================================================

    def reset_result_summary(self) -> None:

        self.set_result_card_value(
            self.result_cycles_card,
            "—",
        )

        self.set_result_card_value(
            self.result_method_card,
            "—",
        )

        self.set_result_card_value(
            self.result_phl_card,
            "—",
        )

        self.set_result_card_value(
            self.result_ratio_card,
            "—",
        )

        self.cycles_table.clear()
        self.cycles_table.setRowCount(0)
        self.cycles_table.setColumnCount(0)

        self.measure_table.clear()
        self.measure_table.setRowCount(0)
        self.measure_table.setColumnCount(0)

        self.mean_table.clear()
        self.mean_table.setRowCount(0)
        self.mean_table.setColumnCount(0)

        self.variance_table.clear()
        self.variance_table.setRowCount(0)
        self.variance_table.setColumnCount(0)

        self.result_tabs.setCurrentIndex(
            0
        )

    # =============================================================
    # DATA PREVIEW
    # =============================================================

    def show_data_preview(
        self,
        dataframe,
    ) -> None:

        preview_rows = min(
            10,
            len(dataframe),
        )

        preview_columns = len(
            dataframe.columns
        )

        self.preview_table.clear()

        self.preview_table.setRowCount(
            preview_rows
        )

        self.preview_table.setColumnCount(
            preview_columns
        )

        self.preview_table.setHorizontalHeaderLabels(
            [
                str(column)
                for column in dataframe.columns
            ]
        )

        for row_index in range(
            preview_rows
        ):

            for column_index in range(
                preview_columns
            ):

                value = dataframe.iloc[
                    row_index,
                    column_index,
                ]

                if value is None:

                    text = ""

                else:

                    try:

                        if pd.isna(value):

                            text = ""

                        else:

                            text = str(value)

                    except Exception:

                        text = str(value)

                item = QTableWidgetItem(
                    text
                )

                self.preview_table.setItem(
                    row_index,
                    column_index,
                    item,
                )

        if preview_rows > 0:

            self.preview_table.scrollToTop()

    # =============================================================
    # NAVIGATION
    # =============================================================

    def change_page(
        self,
        index: int,
    ) -> None:

        self.pages.setCurrentIndex(
            index
        )

    # =============================================================
    # ANALYSIS
    # =============================================================

    def handle_analysis_request(
        self,
        method: str,
    ) -> None:
        """
        Run the complete automatic memristor analysis.

        No X/Y variable selection is required.
        All detected Voltage-Current pairs are processed.
        """

        if self.dataframe is None:

            QMessageBox.warning(
                self,
                "No Dataset",
                (
                    "Please load a dataset "
                    "before running the analysis."
                ),
            )

            return

        try:

            # -----------------------------------------------------
            # Run calculation engine
            # -----------------------------------------------------

            (
                self.df1,
                self.stats_df1,
                self.mean,
                self.var,
            ) = IntegrationService.process_data(
                self.dataframe,
                method,
            )

            self.current_method = method

            # -----------------------------------------------------
            # Update dashboard
            # -----------------------------------------------------

            self.set_card_value(
                self.analysis_status_card,
                "Completed",
            )

            self.set_card_value(
                self.method_status_card,
                method,
            )

            # -----------------------------------------------------
            # Populate results
            # -----------------------------------------------------

            self.populate_results()

            # -----------------------------------------------------
            # Update analysis status
            # -----------------------------------------------------

            self.analysis_page.set_status(
                (
                    "Analysis completed successfully.\n\n"
                    f"Cycles processed: "
                    f"{len(self.df1)}\n"
                    f"Integration method: {method}\n\n"
                    "Results are available in the "
                    "Results section."
                )
            )

            self.results_status.setText(
                (
                    f"Analysis completed — "
                    f"{len(self.df1)} cycles processed "
                    f"using {method}."
                )
            )

            self.export_button.setEnabled(
                True
            )

            self.report_button.setEnabled(
                True
            )

            # Automatically open Results
            self.navigation.setCurrentRow(
                3
            )

            QMessageBox.information(
                self,
                "Analysis Complete",
                (
                    "Memristor analysis completed "
                    "successfully.\n\n"
                    f"Cycles processed: "
                    f"{len(self.df1)}\n"
                    f"Method: {method}"
                ),
            )

        except Exception as error:

            self.analysis_page.set_status(
                (
                    "Analysis failed.\n\n"
                    f"Reason:\n{error}"
                )
            )

            QMessageBox.critical(
                self,
                "Analysis Error",
                (
                    "The analysis could not be completed."
                    "\n\n"
                    f"Reason:\n{error}"
                ),
            )

    # =============================================================
    # POPULATE RESULTS
    # =============================================================

    def populate_results(self) -> None:

        self.populate_cycles_table()

        self.populate_measure_table()

        self.populate_table(
            self.mean_table,
            self.mean,
            index=False,
        )

        self.populate_table(
            self.variance_table,
            self.var,
            index=True,
        )

        self.update_result_summary()

        # Make sure the latest dataset is displayed
        self.loop_plot.set_dataframe(
            self.dataframe
        )

        # Start on the Cycles tab
        self.result_tabs.setCurrentIndex(
            0
        )

    # =============================================================
    # CYCLES TABLE
    # =============================================================

    def populate_cycles_table(self) -> None:

        table = self.cycles_table

        table.setSortingEnabled(False)
        table.clear()

        if self.df1 is None:

            table.setRowCount(0)
            table.setColumnCount(0)

            return

        dataframe = self.df1.copy()

        table.setRowCount(
            len(dataframe)
        )

        table.setColumnCount(
            len(dataframe.columns) + 1
        )

        headers = [
            "Cycle"
        ]

        headers.extend(
            [
                str(column)
                for column in dataframe.columns
            ]
        )

        table.setHorizontalHeaderLabels(
            headers
        )

        for row_index in range(
            len(dataframe)
        ):

            # Cycle number
            cycle_item = QTableWidgetItem(
                str(row_index + 1)
            )

            table.setItem(
                row_index,
                0,
                cycle_item,
            )

            for column_index in range(
                len(dataframe.columns)
            ):

                value = dataframe.iloc[
                    row_index,
                    column_index,
                ]

                text = self.format_table_value(
                    value
                )

                item = QTableWidgetItem(
                    text
                )

                table.setItem(
                    row_index,
                    column_index + 1,
                    item,
                )

        table.resizeColumnsToContents()

        # Keep cycle column compact
        table.setColumnWidth(
            0,
            75,
        )

        table.setSortingEnabled(True)

    # =============================================================
    # MEASURE TABLE
    # =============================================================

    def populate_measure_table(self) -> None:

        table = self.measure_table

        table.setSortingEnabled(False)
        table.clear()

        if self.stats_df1 is None:

            table.setRowCount(0)
            table.setColumnCount(0)

            return

        # ---------------------------------------------------------
        # Convert the original wide Measure result into a
        # readable Metric / Mean table for the UI.
        #
        # The original dataframe is NOT changed.
        # Excel export remains exactly as before.
        # ---------------------------------------------------------

        metric_columns = list(
            self.stats_df1.columns
        )

        table.setRowCount(
            len(metric_columns)
        )

        table.setColumnCount(2)

        table.setHorizontalHeaderLabels(
            [
                "Metric",
                "Mean",
            ]
        )

        for row_index, metric in enumerate(
            metric_columns
        ):

            metric_item = QTableWidgetItem(
                str(metric)
            )

            table.setItem(
                row_index,
                0,
                metric_item,
            )

            try:

                value = self.stats_df1.loc[
                    "Mean",
                    metric,
                ]

            except Exception:

                value = np.nan

            value_item = QTableWidgetItem(
                self.format_table_value(
                    value
                )
            )

            table.setItem(
                row_index,
                1,
                value_item,
            )

        table.resizeColumnsToContents()

        table.setColumnWidth(
            0,
            300,
        )

        table.setColumnWidth(
            1,
            180,
        )

        table.setSortingEnabled(True)

    # =============================================================
    # DATAFRAME → QTABLEWIDGET
    # =============================================================

    def populate_table(
        self,
        table: QTableWidget,
        dataframe,
        index: bool = True,
    ) -> None:

        table.setSortingEnabled(False)
        table.clear()

        if dataframe is None:

            table.setRowCount(0)
            table.setColumnCount(0)

            return

        display_df = dataframe.copy()

        if index:

            display_df = (
                display_df.reset_index()
            )

        table.setRowCount(
            len(display_df)
        )

        table.setColumnCount(
            len(display_df.columns)
        )

        table.setHorizontalHeaderLabels(
            [
                str(column)
                for column in display_df.columns
            ]
        )

        for row_index in range(
            len(display_df)
        ):

            for column_index in range(
                len(display_df.columns)
            ):

                value = display_df.iloc[
                    row_index,
                    column_index,
                ]

                text = self.format_table_value(
                    value
                )

                table.setItem(
                    row_index,
                    column_index,
                    QTableWidgetItem(text),
                )

        table.resizeColumnsToContents()

        table.setSortingEnabled(
            True
        )

    # =============================================================
    # TABLE VALUE FORMAT
    # =============================================================

    @staticmethod
    def format_table_value(
        value,
    ) -> str:

        if value is None:

            return ""

        try:

            if pd.isna(value):

                return ""

        except Exception:

            pass

        if isinstance(
            value,
            (
                float,
                np.floating,
            ),
        ):

            return f"{float(value):.8f}"

        if isinstance(
            value,
            (
                int,
                np.integer,
            ),
        ):

            return str(
                int(value)
            )

        return str(value)

    # =============================================================
    # RESULT SUMMARY
    # =============================================================

    def update_result_summary(
        self,
    ) -> None:

        # ---------------------------------------------------------
        # Cycles
        # ---------------------------------------------------------

        cycle_count = (
            len(self.df1)
            if self.df1 is not None
            else 0
        )

        self.set_result_card_value(
            self.result_cycles_card,
            str(cycle_count),
        )

        # ---------------------------------------------------------
        # Method
        # ---------------------------------------------------------

        self.set_result_card_value(
            self.result_method_card,
            self.current_method
            or "—",
        )

        # ---------------------------------------------------------
        # Mean PHL Area
        # ---------------------------------------------------------

        phl_value = self.get_measure_value(
            "PHL Area"
        )

        self.set_result_card_value(
            self.result_phl_card,
            self.format_summary_value(
                phl_value
            ),
        )

        # ---------------------------------------------------------
        # Mean Loop / Rectangle Ratio
        # ---------------------------------------------------------

        ratio_value = (
            self.get_measure_value(
                "Loop to Rectangle ratio"
            )
        )

        self.set_result_card_value(
            self.result_ratio_card,
            self.format_summary_value(
                ratio_value
            ),
        )

    # =============================================================
    # GET MEASURE VALUE
    # =============================================================

    def get_measure_value(
        self,
        metric_name: str,
    ):

        if self.stats_df1 is None:

            return np.nan

        try:

            return self.stats_df1.loc[
                "Mean",
                metric_name,
            ]

        except Exception:

            return np.nan

    # =============================================================
    # SUMMARY NUMBER FORMAT
    # =============================================================

    @staticmethod
    def format_summary_value(
        value,
    ) -> str:

        if value is None:

            return "—"

        try:

            if pd.isna(value):

                return "—"

            return f"{float(value):.8g}"

        except Exception:

            return str(value)

    # =============================================================
    # EXPORT EXCEL REPORT
    # =============================================================

    def export_results(self) -> None:

        if (
            self.df1 is None
            or self.stats_df1 is None
            or self.mean is None
            or self.var is None
        ):

            QMessageBox.warning(
                self,
                "No Results",
                (
                    "Please run the analysis "
                    "before exporting the report."
                ),
            )

            return

        default_name = (
            "Memristor_Analysis_Report.xlsx"
        )

        save_path, _ = (
            QFileDialog.getSaveFileName(
                self,
                "Save Analysis Report",
                default_name,
                "Excel Files (*.xlsx)",
            )
        )

        if not save_path:

            return

        try:

            with pd.ExcelWriter(
                save_path,
                engine="openpyxl",
            ) as writer:

                # -------------------------------------------------
                # Preserve original report structure
                # -------------------------------------------------

                self.df1.to_excel(
                    writer,
                    sheet_name="Cycles",
                    index=True,
                )

                self.stats_df1.to_excel(
                    writer,
                    sheet_name="Measure",
                    index=True,
                )

                self.mean.to_excel(
                    writer,
                    sheet_name="mean Function",
                    index=False,
                )

                self.var.to_excel(
                    writer,
                    sheet_name="Variance function",
                    index=True,
                )

            QMessageBox.information(
                self,
                "Report Saved",
                (
                    "Excel report created successfully."
                    "\n\n"
                    f"Saved to:\n{save_path}"
                ),
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                (
                    "The report could not be saved."
                    "\n\n"
                    f"Reason:\n{error}"
                ),
            )