import os

import pandas as pd
from pymysql.cursors import DictCursor

from dto.entry_lines import EntryLine
from dto.report_dto import TrialBalance
from config.db_config import get_connection

file_path: str = "./03 00 122 Balance Definitivo 06-2023.xlsx"


def get_header(file_path: str) -> dict[str, str]:
    file_name = os.path.basename(file_path)
    file_name = file_name.replace(".xlsx", "")
    file_name = file_name.split(" ")

    return {
        "report_type": file_name[0],
        "period": file_name[5],
        "company_code": file_name[2],
        "use_auto_storno": file_name[1],
    }


def get_entry_lines(path: str) -> list[EntryLine]:
    data = pd.read_excel(path, dtype=str).to_numpy()
    entry_lines: list[EntryLine] = []

    for entry in data:
        entry_line = EntryLine(
            dimensions=entry[0],
            min_account_code=entry[0],
            debit=float(entry[3]) * 10,
            credit=float(entry[4]) * 10,
            fc_debit=entry[3],
            fc_credit=entry[4],
            fc_currency=entry[5],
        )

        entry_lines.append(entry_line)

    return entry_lines


def get_sap_account_code(min_account: str, max_account: str, cursor: DictCursor) -> str:
    sql = """SELECT 
                        `CTAORIGEN`, REPLACE(`CTASAP`, '.', '') AS CTASAP
                    FROM `cd0133` 
                    WHERE 
                        REPLACE(`CTAORIGEN`, '.', '') 
                        BETWEEN 
                            %s AND %s ORDER BY `CTAORIGEN` ASC"""

    cursor.execute(sql, (min_account, max_account))
    result = cursor.fetchone()
    return result["CTASAP"]


def map_account_codes(entry_lines: list[EntryLine]) -> None:
    connection = get_connection()
    cur = connection.cursor()
    # Map AccountCode v4 to AccountCode SAP
    for entry in entry_lines:
        entry.account_code = get_sap_account_code(
            entry.min_account_code, entry.max_account_code, cur
        )
        entry.close_entry_line()
    cur.close()
    connection.close()


data_header = get_header(file_path)
data_entry_lines = get_entry_lines(file_path)
map_account_codes(entry_lines=data_entry_lines)

trial_balance = TrialBalance(
    period=data_header["period"],
    transaction_code=data_header["report_type"],
    company_code=data_header["company_code"],
    use_auto_storno=data_header["use_auto_storno"],
    journal_entry_lines=data_entry_lines,
)


# Print JSON
print(trial_balance.model_dump_json(indent=4, by_alias=True))
