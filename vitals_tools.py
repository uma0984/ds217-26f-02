"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """Return a list of the systolic readings from the encounters."""
    systolic_values = []
    for line in encounters:
        fields = line.split(",")
        systolic_values.append(int(fields[2]))
    return systolic_values


def mean_systolic(readings):
    """Return the mean of a list of systolic readings, or None if the list is empty."""
    if not readings:
        return None
    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of unique patient IDs in the encounters."""
    unique_patients = 0
    patient_ids = []
    for line in encounters:
        fields = line.split(",")
        patient_id = fields[0]
        if patient_id not in patient_ids:
            patient_ids.append(patient_id)
            unique_patients += 1
    return unique_patients


def patients_at_or_above(encounters: list, cutoff:int) -> list:
    """Return a list of patient IDs whose systolic readings are at or above the cutoff."""
    patients = []
    for line in encounters:
        fields = line.split(",")
        patient_id = fields[0]
        systolic_reading = int(fields[2])
        if systolic_reading >= cutoff and patient_id not in patients:
            patients.append(patient_id)
    return patients