"""Simple growth-rate baseline for initial course enrollments."""

import math

import pandas as pd


REQUIRED_COLUMNS = (
    "Course",
    "Initial enrollment",
    "Growth rate per semester (%)",
)


def build_forecast(enrollment_data: pd.DataFrame, semesters_ahead: int) -> pd.DataFrame:
    """Project course enrollments using a per-semester percentage growth rate."""
    if not isinstance(semesters_ahead, int) or isinstance(semesters_ahead, bool):
        raise ValueError("The number of semesters must be a whole number.")
    if semesters_ahead < 1:
        raise ValueError("Forecast at least one semester ahead.")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in enrollment_data]
    if missing_columns:
        raise ValueError(f"Enrollment data is missing required columns: {', '.join(missing_columns)}.")

    records = []
    seen_courses = set()
    for row_number, row in enumerate(enrollment_data.loc[:, REQUIRED_COLUMNS].itertuples(index=False), 1):
        course, initial_enrollment, growth_rate = row
        if all(_is_blank(value) for value in row):
            continue

        if not isinstance(course, str) or not course.strip():
            raise ValueError(f"Row {row_number}: enter a course name.")
        course = course.strip()
        if course.casefold() in seen_courses:
            raise ValueError(f"Row {row_number}: course '{course}' is listed more than once.")
        seen_courses.add(course.casefold())

        try:
            enrollment = float(initial_enrollment)
        except (TypeError, ValueError):
            raise ValueError(f"Row {row_number}: initial enrollment must be a non-negative whole number.") from None
        if not math.isfinite(enrollment) or enrollment < 0 or not enrollment.is_integer():
            raise ValueError(f"Row {row_number}: initial enrollment must be a non-negative whole number.")

        try:
            rate = float(growth_rate)
        except (TypeError, ValueError):
            raise ValueError(f"Row {row_number}: enter a growth rate of at least -100%.") from None
        if not math.isfinite(rate) or rate < -100:
            raise ValueError(f"Row {row_number}: enter a finite growth rate of at least -100%.")

        for semester in range(1, semesters_ahead + 1):
            projected = enrollment * (1 + rate / 100) ** semester
            if not math.isfinite(projected):
                raise ValueError(f"Row {row_number}: the growth rate produces an unrepresentable forecast.")
            records.append(
                {
                    "Course": course,
                    "Semester": semester,
                    "Projected enrollment": math.floor(projected + 0.5),
                }
            )

    if not records:
        raise ValueError("Add at least one course with enrollment and growth-rate values.")
    return pd.DataFrame.from_records(records, columns=("Course", "Semester", "Projected enrollment"))


def _is_blank(value: object) -> bool:
    if value is None or pd.isna(value):
        return True
    return isinstance(value, str) and not value.strip()
