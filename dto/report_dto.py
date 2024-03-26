from typing_extensions import Self
from pydantic import BaseModel, field_validator, Field, model_validator, ConfigDict

from utils.date_utils import get_last_day_of_month
from .entry_lines import EntryLine


class BaseHeader(BaseModel):

    # Config
    model_config = ConfigDict(populate_by_name=True)

    period: str = Field(exclude=True)
    reference_date: str = Field(default="", serialization_alias="ReferenceDate")
    company_code: str | int = Field(exclude=True)
    memo: str = Field(default="", serialization_alias="Memo")
    transaction_code: str = Field(serialization_alias="TransactionCode")
    tax_date: str = Field(default="", serialization_alias="TaxDate")
    use_auto_storno: str = Field(serialization_alias="UseAutoStorno")
    stamp_tax: str = Field(default="tNO", serialization_alias="StmapTax")
    due_date: str = Field(default="", serialization_alias="DueDate")
    journal_entry_lines: list[EntryLine] = Field(
        default=[], serialization_alias="JournalEntryLines"
    )

    @field_validator("use_auto_storno")
    @classmethod
    def change_auto_storno(cls, v: str) -> str:
        if v == "00":
            return "tNO"
        return "tYES"


class TrialBalance(BaseHeader):

    @model_validator(mode="after")
    def build_model(self) -> Self:
        # Get date for fields
        date = self.period.split("-")
        date = get_last_day_of_month(int(date[0]), int(date[1]))

        self.memo = f"Balance de Comprobación {self.period} Cia {self.company_code}"

        # Build Model
        self.reference_date = date
        self.due_date = self.reference_date
        self.tax_date = self.reference_date
        return self
