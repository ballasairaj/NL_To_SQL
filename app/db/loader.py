import pandas as pd
from app.db.database import engine

INSTALLMENT_DATES = {
    1: "2025-07-30",
    2: "2026-03-30"
}

def normalize(col: str) -> str:
    return col.strip().lower().replace(" ", "_")

def is_paid(value):
    if pd.isna(value):
        return 0
    return 1 if str(value).strip().lower() in ["paid", "yes", "done"] else 0

def normalize_category(value):
    if pd.isna(value):
        return None
    v = str(value).strip().lower()
    if "day" in v:
        return "day_scholar"
    if "hostel" in v:
        return "hostel"
    return v

def load_excel_to_db(excel_file):
    xls = pd.ExcelFile(excel_file)

    # =============================
    # SHEET 1 : STUDENTS + PAYMENTS
    # =============================
    df = pd.read_excel(xls, sheet_name=0)
    df.columns = [normalize(c) for c in df.columns]

    df = df[
        df["student_name"].notna() &
        df["roll_no"].notna() &
        df["total_fee"].notna()
    ]

    students_rows = []
    payments_rows = []

    for _, row in df.iterrows():
        student_id = f"STU{int(row['roll_no']):03d}"

        students_rows.append({
            "student_id": student_id,
            "student_name": row["student_name"],
            "roll_no": int(row["roll_no"]),
            "class": row["class"],
            "section": row["section"],
            "email": row["email"],
            "phone_number": row["phone_number"],
            "category": normalize_category(row["category"]),
            "total_fee": int(row["total_fee"]),
            "due_amount": int(row["due"])
        })

        payments_rows.append({
            "student_id": student_id,
            "installment_no": 1,
            "installment_amount": row["1st_installment"],
            "due_date": INSTALLMENT_DATES[1],
            "paid": is_paid(row["status_1"]),
            "payment_date": row["date_1"]
        })

        payments_rows.append({
            "student_id": student_id,
            "installment_no": 2,
            "installment_amount": row["2nd_installment"],
            "due_date": INSTALLMENT_DATES[2],
            "paid": is_paid(row["status_2"]),
            "payment_date": row["date_2"]
        })

    pd.DataFrame(students_rows).to_sql("students", engine, if_exists="replace", index=False)
    pd.DataFrame(payments_rows).to_sql("payments", engine, if_exists="replace", index=False)

    # =============================
    # SHEET 2 : PAYROLL
    # =============================
    payroll_df = pd.read_excel(xls, sheet_name=1)
    payroll_df.columns = [normalize(c) for c in payroll_df.columns]
    payroll_df = payroll_df[payroll_df["employee_id"].notna()]

    payroll_df.to_sql("payroll", engine, if_exists="replace", index=False)
