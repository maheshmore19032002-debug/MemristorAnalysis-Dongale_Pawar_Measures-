import numpy as np
import pandas as pd

from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QWidget


class MemristorPlotWidget(QWidget):
    """
    Lightweight V-I loop visualization widget.

    The widget automatically detects adjacent Voltage-Current
    column pairs from the supplied dataframe.

    Example:
        V1, I1, V2, I2, V3, I3

    No manual X/Y selection is required.
    """

    COLORS = [
        "#2563eb",
        "#dc2626",
        "#16a34a",
        "#9333ea",
        "#ea580c",
        "#0891b2",
        "#db2777",
        "#65a30d",
        "#7c3aed",
        "#ca8a04",
        "#0f766e",
        "#be123c",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.dataframe = None
        self.pairs = []

        self.setMinimumHeight(420)

        self.setAttribute(
            Qt.WidgetAttribute.WA_OpaquePaintEvent
        )

    # =============================================================
    # DATA
    # =============================================================

    def set_dataframe(self, dataframe) -> None:
        """
        Detect all adjacent V-I pairs and prepare them for plotting.
        """

        self.dataframe = dataframe
        self.pairs = []

        if dataframe is None:
            self.update()
            return

        columns = list(dataframe.columns)

        # ---------------------------------------------------------
        # Primary detection:
        # V / Voltage followed by I / Current
        # ---------------------------------------------------------

        detected_pairs = []

        for index in range(len(columns) - 1):

            first_name = str(columns[index]).strip().lower()
            second_name = str(columns[index + 1]).strip().lower()

            first_is_voltage = (
                first_name.startswith("v")
                or first_name.startswith("voltage")
            )

            second_is_current = (
                second_name.startswith("i")
                or second_name.startswith("current")
            )

            if first_is_voltage and second_is_current:

                detected_pairs.append(
                    (
                        columns[index],
                        columns[index + 1],
                    )
                )

        # ---------------------------------------------------------
        # Fallback:
        # Strict alternating columns
        # ---------------------------------------------------------

        if not detected_pairs and len(columns) >= 2:

            if len(columns) % 2 == 0:

                for index in range(
                    0,
                    len(columns),
                    2,
                ):

                    detected_pairs.append(
                        (
                            columns[index],
                            columns[index + 1],
                        )
                    )

        # ---------------------------------------------------------
        # Prepare numeric data
        # ---------------------------------------------------------

        for pair_number, (
            voltage_column,
            current_column,
        ) in enumerate(detected_pairs, start=1):

            try:

                voltage = pd.to_numeric(
                    dataframe[voltage_column],
                    errors="coerce",
                ).to_numpy(dtype=float)

                current = pd.to_numeric(
                    dataframe[current_column],
                    errors="coerce",
                ).to_numpy(dtype=float)

            except Exception:
                continue

            if len(voltage) == 0:
                continue

            valid_mask = (
                np.isfinite(voltage)
                & np.isfinite(current)
            )

            voltage = voltage[valid_mask]
            current = current[valid_mask]

            if len(voltage) < 2:
                continue

            self.pairs.append(
                {
                    "number": pair_number,
                    "voltage_name": str(voltage_column),
                    "current_name": str(current_column),
                    "voltage": voltage,
                    "current": current,
                }
            )

        self.update()

    def clear_plot(self) -> None:
        self.dataframe = None
        self.pairs = []
        self.update()

    # =============================================================
    # PAINT
    # =============================================================

    def paintEvent(self, event) -> None:

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        width = self.width()
        height = self.height()

        # ---------------------------------------------------------
        # Background
        # ---------------------------------------------------------

        painter.fillRect(
            0,
            0,
            width,
            height,
            QColor("#ffffff"),
        )

        if not self.pairs:

            self.draw_empty_state(
                painter,
                width,
                height,
            )

            painter.end()
            return

        # ---------------------------------------------------------
        # Plot margins
        # ---------------------------------------------------------

        left_margin = 75
        right_margin = 30
        top_margin = 90
        bottom_margin = 65

        plot_left = left_margin
        plot_top = top_margin

        plot_right = max(
            left_margin + 100,
            width - right_margin,
        )

        plot_bottom = max(
            top_margin + 100,
            height - bottom_margin,
        )

        plot_width = (
            plot_right - plot_left
        )

        plot_height = (
            plot_bottom - plot_top
        )

        # ---------------------------------------------------------
        # Title
        # ---------------------------------------------------------

        title_font = QFont(
            "Segoe UI",
            16,
            QFont.Weight.DemiBold,
        )

        painter.setFont(title_font)
        painter.setPen(
            QColor("#172033")
        )

        painter.drawText(
            30,
            28,
            width - 60,
            30,
            Qt.AlignmentFlag.AlignLeft,
            "Memristor V–I Loops",
        )

        # ---------------------------------------------------------
        # Subtitle
        # ---------------------------------------------------------

        subtitle_font = QFont(
            "Segoe UI",
            10,
        )

        painter.setFont(subtitle_font)
        painter.setPen(
            QColor("#64748b")
        )

        painter.drawText(
            30,
            55,
            width - 60,
            20,
            Qt.AlignmentFlag.AlignLeft,
            (
                f"{len(self.pairs)} Voltage–Current "
                "pairs plotted automatically"
            ),
        )

        # ---------------------------------------------------------
        # Calculate global limits
        # ---------------------------------------------------------

        all_voltage = np.concatenate(
            [
                pair["voltage"]
                for pair in self.pairs
            ]
        )

        all_current = np.concatenate(
            [
                pair["current"]
                for pair in self.pairs
            ]
        )

        x_min = float(
            np.min(all_voltage)
        )

        x_max = float(
            np.max(all_voltage)
        )

        y_min = float(
            np.min(all_current)
        )

        y_max = float(
            np.max(all_current)
        )

        # Prevent zero-size ranges
        if np.isclose(x_min, x_max):

            x_padding = (
                abs(x_min) * 0.05
                if not np.isclose(x_min, 0)
                else 1.0
            )

            x_min -= x_padding
            x_max += x_padding

        else:

            x_padding = (
                x_max - x_min
            ) * 0.05

            x_min -= x_padding
            x_max += x_padding

        if np.isclose(y_min, y_max):

            y_padding = (
                abs(y_min) * 0.05
                if not np.isclose(y_min, 0)
                else 1.0
            )

            y_min -= y_padding
            y_max += y_padding

        else:

            y_padding = (
                y_max - y_min
            ) * 0.05

            y_min -= y_padding
            y_max += y_padding

        # ---------------------------------------------------------
        # Mapping functions
        # ---------------------------------------------------------

        def map_x(value):

            return plot_left + (
                (value - x_min)
                / (x_max - x_min)
            ) * plot_width

        def map_y(value):

            return plot_bottom - (
                (value - y_min)
                / (y_max - y_min)
            ) * plot_height

        # ---------------------------------------------------------
        # Grid
        # ---------------------------------------------------------

        grid_pen = QPen(
            QColor("#e2e8f0")
        )

        grid_pen.setWidth(1)

        painter.setPen(grid_pen)

        grid_count = 5

        for i in range(
            grid_count + 1
        ):

            ratio = i / grid_count

            x = int(
                plot_left
                + ratio * plot_width
            )

            y = int(
                plot_top
                + ratio * plot_height
            )

            painter.drawLine(
                x,
                plot_top,
                x,
                plot_bottom,
            )

            painter.drawLine(
                plot_left,
                y,
                plot_right,
                y,
            )

        # ---------------------------------------------------------
        # Axes
        # ---------------------------------------------------------

        axis_pen = QPen(
            QColor("#64748b")
        )

        axis_pen.setWidth(1)

        painter.setPen(axis_pen)

        painter.drawLine(
            plot_left,
            plot_bottom,
            plot_right,
            plot_bottom,
        )

        painter.drawLine(
            plot_left,
            plot_top,
            plot_left,
            plot_bottom,
        )

        # ---------------------------------------------------------
        # Tick labels
        # ---------------------------------------------------------

        tick_font = QFont(
            "Segoe UI",
            9,
        )

        painter.setFont(tick_font)
        painter.setPen(
            QColor("#64748b")
        )

        for i in range(
            grid_count + 1
        ):

            ratio = i / grid_count

            x_value = (
                x_min
                + ratio * (x_max - x_min)
            )

            y_value = (
                y_min
                + ratio * (y_max - y_min)
            )

            x = int(
                plot_left
                + ratio * plot_width
            )

            y = int(
                plot_bottom
                - ratio * plot_height
            )

            x_label = self.format_axis_value(
                x_value
            )

            y_label = self.format_axis_value(
                y_value
            )

            painter.drawText(
                x - 40,
                plot_bottom + 8,
                80,
                20,
                Qt.AlignmentFlag.AlignHCenter,
                x_label,
            )

            painter.drawText(
                5,
                y - 10,
                60,
                20,
                Qt.AlignmentFlag.AlignRight,
                y_label,
            )

        # ---------------------------------------------------------
        # Axis labels
        # ---------------------------------------------------------

        axis_label_font = QFont(
            "Segoe UI",
            10,
            QFont.Weight.DemiBold,
        )

        painter.setFont(
            axis_label_font
        )

        painter.setPen(
            QColor("#334155")
        )

        painter.drawText(
            plot_left,
            height - 20,
            plot_width,
            25,
            Qt.AlignmentFlag.AlignHCenter,
            "Voltage",
        )

        painter.save()

        painter.translate(
            18,
            plot_top + plot_height / 2,
        )

        painter.rotate(-90)

        painter.drawText(
            -plot_height / 2,
            -10,
            plot_height,
            20,
            Qt.AlignmentFlag.AlignHCenter,
            "Current",
        )

        painter.restore()

        # ---------------------------------------------------------
        # Draw V-I loops
        # ---------------------------------------------------------

        for pair_index, pair in enumerate(
            self.pairs
        ):

            color = QColor(
                self.COLORS[
                    pair_index
                    % len(self.COLORS)
                ]
            )

            pen = QPen(color)
            pen.setWidth(2)

            painter.setPen(pen)

            voltage = pair["voltage"]
            current = pair["current"]

            for point_index in range(
                1,
                len(voltage),
            ):

                x1 = map_x(
                    voltage[
                        point_index - 1
                    ]
                )

                y1 = map_y(
                    current[
                        point_index - 1
                    ]
                )

                x2 = map_x(
                    voltage[
                        point_index
                    ]
                )

                y2 = map_y(
                    current[
                        point_index
                    ]
                )

                painter.drawLine(
                    int(x1),
                    int(y1),
                    int(x2),
                    int(y2),
                )

        # ---------------------------------------------------------
        # Legend
        # ---------------------------------------------------------

        self.draw_legend(
            painter,
            width,
        )

        painter.end()

    # =============================================================
    # EMPTY STATE
    # =============================================================

    def draw_empty_state(
        self,
        painter: QPainter,
        width: int,
        height: int,
    ) -> None:

        title_font = QFont(
            "Segoe UI",
            15,
            QFont.Weight.DemiBold,
        )

        painter.setFont(title_font)
        painter.setPen(
            QColor("#334155")
        )

        painter.drawText(
            30,
            height // 2 - 15,
            width - 60,
            30,
            Qt.AlignmentFlag.AlignCenter,
            "No V–I data available",
        )

        body_font = QFont(
            "Segoe UI",
            10,
        )

        painter.setFont(body_font)
        painter.setPen(
            QColor("#64748b")
        )

        painter.drawText(
            30,
            height // 2 + 20,
            width - 60,
            25,
            Qt.AlignmentFlag.AlignCenter,
            (
                "Load a dataset containing "
                "Voltage–Current pairs."
            ),
        )

    # =============================================================
    # LEGEND
    # =============================================================

    def draw_legend(
        self,
        painter: QPainter,
        width: int,
    ) -> None:

        legend_font = QFont(
            "Segoe UI",
            9,
        )

        painter.setFont(
            legend_font
        )

        max_items_per_row = max(
            1,
            min(
                5,
                len(self.pairs),
            ),
        )

        item_width = max(
            120,
            (width - 60)
            // max_items_per_row,
        )

        start_x = 30
        start_y = 70

        for index, pair in enumerate(
            self.pairs
        ):

            row = (
                index
                // max_items_per_row
            )

            column = (
                index
                % max_items_per_row
            )

            x = (
                start_x
                + column * item_width
            )

            y = (
                start_y
                + row * 18
            )

            color = QColor(
                self.COLORS[
                    index
                    % len(self.COLORS)
                ]
            )

            pen = QPen(color)
            pen.setWidth(3)

            painter.setPen(pen)

            painter.drawLine(
                x,
                y,
                x + 18,
                y,
            )

            painter.setPen(
                QColor("#334155")
            )

            painter.drawText(
                x + 24,
                y - 7,
                item_width - 25,
                18,
                Qt.AlignmentFlag.AlignLeft,
                f"Cycle {pair['number']}",
            )

    # =============================================================
    # FORMAT
    # =============================================================

    @staticmethod
    def format_axis_value(
        value: float,
    ) -> str:

        if np.isclose(value, 0):

            return "0"

        absolute_value = abs(value)

        if (
            absolute_value >= 1000
            or absolute_value < 0.001
        ):

            return f"{value:.2e}"

        return f"{value:.4g}"