import math

import numpy as np
import pandas as pd


class IntegrationService:
    """
    Numerical integration and memristor analysis service.

    The calculation logic is based on the original memristor
    analysis code.

    Supported methods:
        - Trapezoidal Rule
        - Simpson's 1/3 Rule
        - Simpson's 3/8 Rule
    """

    # =============================================================
    # NUMERICAL INTEGRATION
    # =============================================================

    @staticmethod
    def trapezoidal(x, y):
        """
        Trapezoidal numerical integration.

        Formula:
            Integral ≈ Σ [(x[i+1] - x[i]) *
                          (y[i] + y[i+1]) / 2]
        """

        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if len(x) != len(y):
            raise ValueError(
                "X and Y must contain the same number of points."
            )

        if len(x) < 2:
            raise ValueError(
                "At least two data points are required."
            )

        return float(
            np.sum(
                (x[1:] - x[:-1])
                * (y[1:] + y[:-1])
                / 2.0
            )
        )

    @staticmethod
    def simpsons_one_third(x, y):
        """
        Simpson's 1/3 numerical integration.

        Based on the original implementation.

        If the number of intervals is odd, the final interval
        is excluded, matching the original program behavior.
        """

        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if len(x) != len(y):
            raise ValueError(
                "X and Y must contain the same number of points."
            )

        if len(x) < 3:
            raise ValueError(
                "Simpson's 1/3 Rule requires at least 3 points."
            )

        n = len(x) - 1

        # Preserve the behavior of the original code.
        if n % 2 != 0:
            n -= 1

        if n <= 0:
            raise ValueError(
                "Insufficient points for Simpson's 1/3 Rule."
            )

        h = abs(x[n] - x[0]) / n

        area = y[0] + y[n]

        area += 4 * np.sum(y[1:n:2])

        area += 2 * np.sum(y[2:n:2])

        area *= h / 3.0

        return float(area)

    @staticmethod
    def simpsons_three_eighth(x, y):
        """
        Simpson's 3/8 numerical integration.

        Composite Simpson's 3/8 Rule:

            Integral ≈ 3h/8 [
                y0 + yn
                + 3(sum of non-multiple-of-3 interior points)
                + 2(sum of multiple-of-3 interior points)
            ]

        If the number of intervals is not divisible by 3,
        the largest valid number of intervals is used.
        """

        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if len(x) != len(y):
            raise ValueError(
                "X and Y must contain the same number of points."
            )

        if len(x) < 4:
            raise ValueError(
                "Simpson's 3/8 Rule requires at least 4 points."
            )

        n = len(x) - 1

        # Use the largest number of intervals divisible by 3.
        n = n - (n % 3)

        if n <= 0:
            raise ValueError(
                "Insufficient points for Simpson's 3/8 Rule."
            )

        h = abs(x[n] - x[0]) / n

        area = y[0] + y[n]

        # Interior points
        for i in range(1, n):
            if i % 3 == 0:
                area += 2 * y[i]
            else:
                area += 3 * y[i]

        area *= 3 * h / 8.0

        return float(area)

    # =============================================================
    # METHOD SELECTOR
    # =============================================================

    @classmethod
    def integrate(cls, x, y, method):
        """
        Select the requested numerical integration method.
        """

        if method == "Trapezoidal Rule":
            return cls.trapezoidal(x, y)

        if method == "Simpson's 1/3 Rule":
            return cls.simpsons_one_third(x, y)

        if method == "Simpson's 3/8 Rule":
            return cls.simpsons_three_eighth(x, y)

        raise ValueError(
            f"Unsupported integration method: {method}"
        )

    # =============================================================
    # VARIATION
    # =============================================================

    @staticmethod
    def compute_total_variation(list1, list2):
        """
        Compute total squared variation:

            Σ (x1 - x2)^2
        """

        array1 = np.asarray(list1, dtype=float)
        array2 = np.asarray(list2, dtype=float)

        if len(array1) != len(array2):
            raise ValueError(
                "Both arrays must have the same length."
            )

        squared_variation = (
            array1 - array2
        ) ** 2

        total_variation = np.sum(
            squared_variation
        )

        return float(total_variation)

    @staticmethod
    def compute_total_sd(list1, list2):
        """
        Compute:

            sqrt(Σ (x1 - x2)^2)
        """

        total_variation = (
            IntegrationService.compute_total_variation(
                list1,
                list2,
            )
        )

        return float(
            math.sqrt(total_variation)
        )

    # =============================================================
    # FARTHEST DISTANCES
    # =============================================================

    @staticmethod
    def find_farthest_distances(data):
        """
        Calculate the maximum distance from origin
        for the first and second halves of a V-I cycle.
        """

        voltage = pd.to_numeric(
            data.iloc[:, 0],
            errors="coerce",
        )

        current = pd.to_numeric(
            data.iloc[:, 1],
            errors="coerce",
        )

        mid_index = len(voltage) // 2

        distances_part1 = np.sqrt(
            voltage.iloc[:mid_index].to_numpy() ** 2
            + current.iloc[:mid_index].to_numpy() ** 2
        )

        distances_part2 = np.sqrt(
            voltage.iloc[mid_index:].to_numpy() ** 2
            + current.iloc[mid_index:].to_numpy() ** 2
        )

        return (
            float(np.max(distances_part1)),
            float(np.max(distances_part2)),
        )

    # =============================================================
    # MAIN MEMRISTOR PROCESSING
    # =============================================================

    @classmethod
    def process_data(
        cls,
        data: pd.DataFrame,
        method: str = "Simpson's 1/3 Rule",
    ):
        """
        Process all Voltage-Current cycles.

        Expected dataset structure:

            V1 | I1 | V2 | I2 | V3 | I3 | ...

        No cycle count is hard-coded.

        Returns:
            df1
            stats_df1
            mean
            var
        """

        if data is None or data.empty:
            raise ValueError(
                "The dataset is empty."
            )

        num_columns = data.shape[1]

        if num_columns < 2:
            raise ValueError(
                "The dataset must contain at least "
                "one Voltage-Current pair."
            )

        if num_columns % 2 != 0:
            raise ValueError(
                "The dataset must contain an even number "
                "of columns arranged as Voltage-Current pairs."
            )

        cycles = num_columns // 2

        # ---------------------------------------------------------
        # Storage
        # ---------------------------------------------------------

        imax = []
        imin = []
        vmax = []
        vmin = []

        rect_area = []
        loop_area = []

        lobe_1_area = []
        lobe_2_area = []

        symmetry_index = []
        loop_to_rectangle_ratio = []

        l1 = []
        l2 = []

        lobe_1_area_per_unit = []
        lobe_2_area_per_unit = []

        sd_per_unit_area = []
        variation = []

        # ---------------------------------------------------------
        # Mean Voltage and Mean Current
        # ---------------------------------------------------------

        selected_columns_voltage = data.iloc[:, ::2].apply(
            pd.to_numeric,
            errors="coerce",
        )

        mean_selected_cols_volt = (
            selected_columns_voltage.mean(axis=1)
        )

        selected_columns = data.iloc[:, 1::2].apply(
            pd.to_numeric,
            errors="coerce",
        )

        mean_selected_cols = (
            selected_columns.mean(axis=1)
        )

        # ---------------------------------------------------------
        # Process every cycle
        # ---------------------------------------------------------

        for i in range(cycles):

            voltage = pd.to_numeric(
                data.iloc[:, 2 * i],
                errors="coerce",
            )

            current = pd.to_numeric(
                data.iloc[:, 2 * i + 1],
                errors="coerce",
            )

            # Check numeric values
            if voltage.isna().any():
                raise ValueError(
                    f"Non-numeric or missing values found "
                    f"in Voltage column {i + 1}."
                )

            if current.isna().any():
                raise ValueError(
                    f"Non-numeric or missing values found "
                    f"in Current column {i + 1}."
                )

            # -----------------------------------------------------
            # Basic maximum/minimum values
            # -----------------------------------------------------

            vmin.append(
                float(voltage.min())
            )

            vmax.append(
                float(voltage.max())
            )

            imax.append(
                float(current.max())
            )

            imin.append(
                float(current.min())
            )

            # -----------------------------------------------------
            # Rectangle area
            # -----------------------------------------------------

            rectangle = (
                abs(vmin[i] - vmax[i])
                * abs(imin[i] - imax[i])
            )

            rect_area.append(
                float(rectangle)
            )

            # -----------------------------------------------------
            # Detect characteristic voltage indexes
            # -----------------------------------------------------

            index1 = 0
            index2 = 0
            index3 = 0

            for j in range(2, len(data)):

                v_j = voltage.iloc[j]
                v_j2 = voltage.iloc[j - 2]
                v_j1 = voltage.iloc[j - 1]

                # Positive-side turning point
                if (
                    v_j >= 0
                    and v_j2 <= v_j1 >= v_j
                ):
                    index1 = j - 1

                # Zero crossing
                if (
                    v_j <= 0
                    and 0 <= v_j1
                ):
                    index2 = j - 1

                # Negative-side turning point
                if (
                    v_j <= 0
                    and v_j2 >= v_j1 <= v_j
                ):
                    index3 = j - 1

            # Same fallback behavior as original code
            if index1 == 0:
                index1 = int(
                    voltage.idxmax()
                )

            if index3 == 0:
                index3 = int(
                    voltage.idxmin()
                )

            # -----------------------------------------------------
            # Extract four integration regions
            # -----------------------------------------------------

            x1 = voltage.iloc[
                : index1 + 1
            ].to_numpy()

            y1 = current.iloc[
                : index1 + 1
            ].to_numpy()

            x2 = voltage.iloc[
                index1 + 1 : index2 + 1
            ].to_numpy()

            y2 = current.iloc[
                index1 + 1 : index2 + 1
            ].to_numpy()

            x3 = -1 * voltage.iloc[
                index2 + 1 : index3 + 1
            ].to_numpy()

            y3 = -1 * current.iloc[
                index2 + 1 : index3 + 1
            ].to_numpy()

            x4 = -1 * voltage.iloc[
                index3 + 1 :
            ].to_numpy()

            y4 = -1 * current.iloc[
                index3 + 1 :
            ].to_numpy()

            # -----------------------------------------------------
            # Numerical integration
            # -----------------------------------------------------

            area1 = cls.integrate(
                x1,
                y1,
                method,
            )

            area2 = cls.integrate(
                x2,
                y2,
                method,
            )

            area3 = cls.integrate(
                x3,
                y3,
                method,
            )

            area4 = cls.integrate(
                x4,
                y4,
                method,
            )

            # -----------------------------------------------------
            # Lobe lengths
            # -----------------------------------------------------

            p, q = cls.find_farthest_distances(
                data.iloc[:, 2 * i : 2 * i + 2]
            )

            l1.append(p)
            l2.append(q)

            # -----------------------------------------------------
            # Loop area
            # -----------------------------------------------------

            lobe1 = abs(
                area1 - area2
            )

            lobe2 = abs(
                area3 - area4
            )

            total_loop_area = (
                lobe1 + lobe2
            )

            loop_area.append(
                float(total_loop_area)
            )

            # -----------------------------------------------------
            # Loop / Rectangle ratio
            # -----------------------------------------------------

            if rectangle == 0:
                lsr = np.nan
            else:
                lsr = (
                    total_loop_area
                    / rectangle
                )

            loop_to_rectangle_ratio.append(
                float(lsr)
                if not np.isnan(lsr)
                else np.nan
            )

            # -----------------------------------------------------
            # Lobe areas
            # -----------------------------------------------------

            lobe_1_area.append(
                float(lobe1)
            )

            lobe_2_area.append(
                float(lobe2)
            )

            # -----------------------------------------------------
            # Lobe area per unit
            # -----------------------------------------------------

            if p == 0:
                lobe1_per_unit = np.nan
            else:
                lobe1_per_unit = abs(
                    lobe1 / p
                )

            if q == 0:
                lobe2_per_unit = np.nan
            else:
                lobe2_per_unit = abs(
                    lobe2 / q
                )

            lobe_1_area_per_unit.append(
                float(lobe1_per_unit)
                if not np.isnan(lobe1_per_unit)
                else np.nan
            )

            lobe_2_area_per_unit.append(
                float(lobe2_per_unit)
                if not np.isnan(lobe2_per_unit)
                else np.nan
            )

            # -----------------------------------------------------
            # Symmetry Index
            # -----------------------------------------------------

            denominator = (
                lobe1 + lobe2
            )

            if denominator == 0:
                si = np.nan
            else:
                si = abs(
                    lobe1 - lobe2
                ) / denominator

            symmetry_index.append(
                float(si)
                if not np.isnan(si)
                else np.nan
            )

            # -----------------------------------------------------
            # Variation
            # -----------------------------------------------------

            v = cls.compute_total_variation(
                current,
                mean_selected_cols,
            )

            variation.append(v)

            # -----------------------------------------------------
            # SD Per Unit Area
            # -----------------------------------------------------

            sd = cls.compute_total_sd(
                current,
                mean_selected_cols,
            )

            if total_loop_area == 0:
                sd_per_unit = np.nan
            else:
                sd_per_unit = (
                    sd
                    / total_loop_area
                )

            sd_per_unit_area.append(
                float(sd_per_unit)
                if not np.isnan(sd_per_unit)
                else np.nan
            )

        # =========================================================
        # CYCLE-WISE RESULT
        # =========================================================

        df1 = pd.DataFrame(
            {
                "Vmax": vmax,
                "Vmin": vmin,
                "Imax": imax,
                "Imin": imin,
                "Rectangle Area": rect_area,
                "Lobe1 Length L1": l1,
                "Lobe1 Length L2": l2,
                "PHL Area": loop_area,
                "Loop to Rectangle ratio":
                    loop_to_rectangle_ratio,
                "Lobe 1 Area": lobe_1_area,
                "Lobe 2 Area": lobe_2_area,
                "Lobe 1 area per unit":
                    lobe_1_area_per_unit,
                "Lobe 2 area per unit":
                    lobe_2_area_per_unit,
                "Symmetry Index": symmetry_index,
                "Variation": variation,
                "SD Per Unit Area":
                    sd_per_unit_area,
            }
        )

        # =========================================================
        # MEAN / MEASURE
        # =========================================================

        stats_df1 = pd.DataFrame(
            {
                "Mean": df1.mean(
                    numeric_only=True
                )
            }
        ).T

        # =========================================================
        # MEAN FUNCTION
        # =========================================================

        mean = pd.DataFrame(
            {
                "Voltage":
                    mean_selected_cols_volt,
                "Mean loop":
                    mean_selected_cols,
            }
        )

        # =========================================================
        # VARIANCE FUNCTION
        # =========================================================

        var = pd.DataFrame(
            {
                "Sample Variance":
                    selected_columns.var(
                        axis=1,
                        ddof=1,
                    ),
                "Sample Standard Deviation":
                    selected_columns.std(
                        axis=1,
                        ddof=1,
                    ),
            }
        )

        return (
            df1,
            stats_df1,
            mean,
            var,
        )