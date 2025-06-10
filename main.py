from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any
import pandas as pd

app = FastAPI()

# Load the Excel file once when the app starts
def read_excel_file():
    # 👇 Put the correct Excel file path here
    file_path = "data.xlsx"  # Change to your actual Excel file name or path
    try:
        xls = pd.ExcelFile(file_path)
        return {sheet_name: xls.parse(sheet_name) for sheet_name in xls.sheet_names}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading Excel file: {str(e)}")

excel_data = read_excel_file()

# 🟢 Endpoint 1: List all tables (sheet names)
@app.get("/list_tables")
def list_tables() -> List[str]:
    return list(excel_data.keys())

# 🟢 Endpoint 2: Get details of a specific table
@app.get("/get_table_details/{table_name}")
def get_table_details(table_name: str) -> Dict[str, Any]:
    if table_name not in excel_data:
        raise HTTPException(status_code=404, detail="Table not found")
    df = excel_data[table_name]
    return {
        "columns": list(df.columns),
        "num_rows": len(df),
        "sample_data": df.head(5).to_dict(orient="records")
    }

# 🟢 Endpoint 3: Get row-wise sum for a table
@app.get("/row_sum/{table_name}")
def row_sum(table_name: str) -> List[float]:
    if table_name not in excel_data:
        raise HTTPException(status_code=404, detail="Table not found")
    df = excel_data[table_name]
    numeric_df = df.select_dtypes(include='number')
    return numeric_df.sum(axis=1).tolist()
