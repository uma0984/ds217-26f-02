#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Usable encounters are those with three fields, a valid integer systolic reading, and a plausible value.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    lines = data_path.read_text().splitlines()[1:]
    encounters = []
    skipped = 0
    for line in lines:
        fields = line.split(",")
        if len(fields) == 3:
            if fields[2].isint():
                if 60 <= int(fields[2]) <= 250:
                    encounters.append(line)
                else:
                    print(f"Skipping row with implausible systolic reading: {line}")
                    skipped += 1
            else:
                print(f"Skipping row with non-integer systolic reading: {line}")
                skipped += 1
        else:
            print(f"Skipping row with incorrect number of fields: {line}")
            skipped += 1
    return encounters, skipped


def main():
    """Main function to orchestrate the clinic report generation."""
    encounters, skipped = read_encounters(DATA_PATH)
    readings = systolic_readings(encounters)
    report_text = (f"Usable encounters: {len(encounters)}\n"
                   f"Skipped rows: {skipped}\n"
                   f"Patients seen: {count_patients(encounters)}\n"
                   f"Mean systolic: {mean_systolic(readings):.1f} mmHg\n"
                   f"Highest systolic: {max(systolic_readings(encounters))} mmHg\n"
                   f"Lowest systolic: {min(systolic_readings(encounters))} mmHg")

    OUTPUT_DIR.mkdir(exist_ok=True)  
    report_path = OUTPUT_DIR / "vitals_report.txt"
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write(report_text)

    with open(report_path, "r", encoding="utf-8") as report_file:
        saved_text = report_file.read()

    print(f"Read back from {report_path}:")
    print(saved_text, end="")
    print(f"Saved report matches: {saved_text == report_text}")
    assert saved_text == report_text, "the saved report does not match the text we built"
    cutoff = 140

    # while True:
        #     cutoff = input("Enter the cutoff for follow-up (between (120,180)): ")
        #     if not cutoff.isdigit() or not (120 <= int(cutoff) <= 180):
        #         print("Invalid input. Please enter a number between 120 and 180.")
        #     else:
        #         break

    
    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_text = (f"Cutoff: {cutoff}\n"
                     f"Reason: Systolic reading at or above cutoff\n")
    followup_text += "\n".join(patients_at_or_above(encounters, cutoff)) + "\n"

    with open(followup_path, "w", encoding="utf-8") as followup_file:
        followup_file.write(followup_text)
    

if __name__ == "__main__":
    main()
