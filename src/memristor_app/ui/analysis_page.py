from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class AnalysisPage(QWidget):
    """Automatic memristor analysis configuration page."""

    run_analysis_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.dataframe = None
        self.detected_pairs = []

        self.setup_ui()

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------

        title = QLabel("Numerical Analysis")
        title.setObjectName("page_title")

        description = QLabel(
            "Automatically analyze all Voltage–Current cycles "
            "from the loaded memristor dataset."
        )
        description.setObjectName("description_label")
        description.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # ---------------------------------------------------------
        # Configuration Card
        # ---------------------------------------------------------

        config_card = QFrame()
        config_card.setObjectName("info_card")

        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(25, 25, 25, 25)
        config_layout.setSpacing(18)

        config_title = QLabel("Analysis Configuration")
        config_title.setObjectName("card_title")

        config_layout.addWidget(config_title)

        # ---------------------------------------------------------
        # Information Grid
        # ---------------------------------------------------------

        info_grid = QGridLayout()
        info_grid.setHorizontalSpacing(30)
        info_grid.setVerticalSpacing(8)

        # Give the value row enough vertical space.
        info_grid.setRowMinimumHeight(1, 42)

        # ---------------------------------------------------------
        # Detected V-I Pairs
        # ---------------------------------------------------------

        cycles_title = QLabel("Detected V-I Pairs")
        cycles_title.setObjectName("card_title")

        self.cycles_value = QLabel("0")
        self.cycles_value.setObjectName("card_value")

        self.cycles_value.setMinimumHeight(42)
        self.cycles_value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        # ---------------------------------------------------------
        # Data Points
        # ---------------------------------------------------------

        points_title = QLabel("Data Points")
        points_title.setObjectName("card_title")

        self.points_value = QLabel("0")
        self.points_value.setObjectName("card_value")

        self.points_value.setMinimumHeight(42)
        self.points_value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        # ---------------------------------------------------------
        # Dataset Columns
        # ---------------------------------------------------------

        columns_title = QLabel("Dataset Columns")
        columns_title.setObjectName("card_title")

        self.columns_value = QLabel("0")
        self.columns_value.setObjectName("card_value")

        self.columns_value.setMinimumHeight(42)
        self.columns_value.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        # ---------------------------------------------------------
        # Add widgets to grid
        # ---------------------------------------------------------

        info_grid.addWidget(cycles_title, 0, 0)
        info_grid.addWidget(self.cycles_value, 1, 0)

        info_grid.addWidget(points_title, 0, 1)
        info_grid.addWidget(self.points_value, 1, 1)

        info_grid.addWidget(columns_title, 0, 2)
        info_grid.addWidget(self.columns_value, 1, 2)

        # Make all three columns share available width.
        info_grid.setColumnStretch(0, 1)
        info_grid.setColumnStretch(1, 1)
        info_grid.setColumnStretch(2, 1)

        config_layout.addLayout(info_grid)

        # ---------------------------------------------------------
        # Integration Method
        # ---------------------------------------------------------

        method_layout = QHBoxLayout()
        method_layout.setSpacing(12)

        method_label = QLabel("Integration Method:")
        method_label.setObjectName("card_title")

        self.method_combo = QComboBox()
        self.method_combo.setMinimumHeight(40)

        self.method_combo.addItems(
            [
                "Trapezoidal Rule",
                "Simpson's 1/3 Rule",
                "Simpson's 3/8 Rule",
            ]
        )

        method_layout.addWidget(method_label)
        method_layout.addWidget(self.method_combo, 1)

        config_layout.addLayout(method_layout)

        # ---------------------------------------------------------
        # Run Button
        # ---------------------------------------------------------

        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.run_button = QPushButton("Run Analysis")
        self.run_button.setObjectName("primary_button")
        self.run_button.setMinimumWidth(160)
        self.run_button.setMinimumHeight(44)

        self.run_button.clicked.connect(
            self._run_analysis
        )

        button_layout.addWidget(self.run_button)

        config_layout.addLayout(button_layout)

        main_layout.addWidget(config_card)

        # ---------------------------------------------------------
        # Status Card
        # ---------------------------------------------------------

        status_card = QFrame()
        status_card.setObjectName("info_card")

        status_layout = QVBoxLayout(status_card)
        status_layout.setContentsMargins(25, 20, 25, 20)
        status_layout.setSpacing(8)

        status_title = QLabel("Analysis Status")
        status_title.setObjectName("card_title")

        self.status_label = QLabel(
            "Load a dataset to begin analysis."
        )
        self.status_label.setObjectName("placeholder_label")
        self.status_label.setWordWrap(True)

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(status_card)

        # ---------------------------------------------------------
        # Required Outputs
        # ---------------------------------------------------------

        output_card = QFrame()
        output_card.setObjectName("info_card")

        output_layout = QVBoxLayout(output_card)
        output_layout.setContentsMargins(25, 20, 25, 20)
        output_layout.setSpacing(10)

        output_title = QLabel("Required Outputs")
        output_title.setObjectName("card_title")

        output_layout.addWidget(output_title)

        outputs = [
            "1. Cycles — individual cycle-wise measurements",
            "2. Measure — mean of all cycle measurements",
            "3. Mean Function — mean Voltage and Mean Loop",
            "4. Variance Function — Sample Variance and Sample Standard Deviation",
        ]

        for text in outputs:
            label = QLabel(text)
            label.setObjectName("placeholder_label")
            label.setWordWrap(True)
            output_layout.addWidget(label)

        main_layout.addWidget(output_card)

        main_layout.addStretch()

    # =============================================================
    # DATASET
    # =============================================================

    def set_dataframe(self, dataframe) -> None:
        """Receive the loaded dataset and detect V-I pairs."""

        self.dataframe = dataframe

        if dataframe is None or dataframe.empty:
            self.clear_dataset()
            return

        self.columns_value.setText(
            str(len(dataframe.columns))
        )

        self.points_value.setText(
            str(len(dataframe))
        )

        self.detected_pairs = (
            self.detect_voltage_current_pairs(dataframe)
        )

        self.cycles_value.setText(
            str(len(self.detected_pairs))
        )

        if self.detected_pairs:
            self.status_label.setText(
                f"Dataset loaded successfully.\n\n"
                f"Detected {len(self.detected_pairs)} "
                f"Voltage–Current pair(s).\n\n"
                "All detected pairs will be analyzed automatically."
            )

            self.run_button.setEnabled(True)

        else:
            self.status_label.setText(
                "Dataset loaded, but no valid Voltage–Current "
                "column pairs were detected."
            )

            self.run_button.setEnabled(False)

    def clear_dataset(self) -> None:
        """Reset analysis information."""

        self.dataframe = None
        self.detected_pairs = []

        self.cycles_value.setText("0")
        self.points_value.setText("0")
        self.columns_value.setText("0")

        self.status_label.setText(
            "Load a dataset to begin analysis."
        )

        self.run_button.setEnabled(False)

    # =============================================================
    # V-I PAIR DETECTION
    # =============================================================

    @staticmethod
    def detect_voltage_current_pairs(dataframe):
        """
        Detect Voltage–Current pairs dynamically.

        Expected general structure:

            V1, I1, V2, I2, ...

        The actual number of pairs is never hard-coded.
        """

        columns = list(dataframe.columns)

        pairs = []

        # ---------------------------------------------------------
        # First attempt:
        # detect adjacent V-I columns by names such as:
        #
        # V1 / I1
        # Voltage1 / Current1
        # V_1 / I_1
        # ---------------------------------------------------------

        for index in range(len(columns) - 1):

            voltage_column = columns[index]
            current_column = columns[index + 1]

            voltage_text = (
                str(voltage_column)
                .strip()
                .lower()
            )

            current_text = (
                str(current_column)
                .strip()
                .lower()
            )

            voltage_is_valid = (
                voltage_text.startswith("v")
                or voltage_text.startswith("voltage")
            )

            current_is_valid = (
                current_text.startswith("i")
                or current_text.startswith("current")
            )

            if voltage_is_valid and current_is_valid:
                pairs.append(
                    (
                        voltage_column,
                        current_column,
                    )
                )

        # ---------------------------------------------------------
        # Fallback:
        # strict alternating-column structure
        #
        # V1, I1, V2, I2, ...
        # ---------------------------------------------------------

        if not pairs and len(columns) >= 2:

            if len(columns) % 2 == 0:

                for index in range(
                    0,
                    len(columns),
                    2,
                ):

                    pairs.append(
                        (
                            columns[index],
                            columns[index + 1],
                        )
                    )

        return pairs

    # =============================================================
    # RUN ANALYSIS
    # =============================================================

    def _run_analysis(self) -> None:

        if self.dataframe is None:
            self.status_label.setText(
                "Please load a dataset first."
            )
            return

        if not self.detected_pairs:
            self.status_label.setText(
                "No Voltage–Current pairs were detected."
            )
            return

        method = self.method_combo.currentText()

        self.status_label.setText(
            f"Analysis requested.\n\n"
            f"Detected cycles: {len(self.detected_pairs)}\n"
            f"Method: {method}\n\n"
            "Processing all Voltage–Current pairs..."
        )

        self.run_analysis_requested.emit(method)

    # =============================================================
    # STATUS
    # =============================================================

    def set_status(self, message: str) -> None:
        self.status_label.setText(message)