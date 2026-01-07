#!/usr/bin/env python3
"""Convert subjects.txt to CSV format with parsed assignment names and users."""

import csv
import re

ASSIGNMENT_PATTERN = r"(day\s*\d{1,2}|final\s+project\s+proposal)"


def parse_assignment_name(subject: str) -> str:
    assignment_match = re.search(ASSIGNMENT_PATTERN, subject, re.IGNORECASE)
    assignment_name = assignment_match.group(1).strip() if assignment_match else ""

    assignment_name = re.sub(r"\s+", " ", assignment_name)

    if not assignment_name:
        return ""

    normalized = assignment_name.lower().replace(" ", "")

    day_match = re.search(r"day(\d{1,2})", normalized)
    if day_match:
        day_num = int(day_match.group(1))
        return f"Day{day_num:02d}" if day_num >= 1 else ""

    if "finalprojectproposal" in normalized:
        return "Proposal"

    return ""


def parse_user(subject: str) -> str:
    subject = re.sub(ASSIGNMENT_PATTERN, "", subject, count=1)
    user_match = re.search(r"\bby\s+(.+?)(?:\s*$)", subject, re.IGNORECASE)
    if user_match:
        user = user_match.group(1).strip()
        return " ".join(word.capitalize() for word in user.split())
    return " ".join(re.findall(r"\b[A-Z][a-z]*\b", subject))


def convert_subjects_to_csv(input_file: str, output_file: str) -> None:
    rows = []
    errors = []

    with open(input_file, "r") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 4:
                issue_number = parts[0]
                subject = parts[2]
                date = parts[3]

                assignment_name = parse_assignment_name(subject)
                user = parse_user(subject)

                # Report parsing errors
                if not assignment_name or not user:
                    errors.append(
                        {"original": line.strip(), "issue_number": issue_number}
                    )

                rows.append(
                    {
                        "issue_number": issue_number,
                        "assignment_name": assignment_name,
                        "user": user,
                        "date": date,
                    }
                )

    # Write to CSV
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["issue_number", "assignment_name", "user", "date"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully converted {len(rows)} entries to {output_file}")

    # Print parsing errors
    if errors:
        print(f"\n⚠️  {len(errors)} lines with parsing issues:\n")
        for error in errors:
            print(f"Issue #{error['issue_number']}: {error['original']}")


if __name__ == "__main__":
    convert_subjects_to_csv("issues.txt", "subjects.csv")
