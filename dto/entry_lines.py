from typing_extensions import Self
from pydantic import BaseModel, field_validator, Field, model_validator


class EntryLine(BaseModel):
    account_code: str = Field(default="", serialization_alias="AccountCode")
    dimensions: str = Field(exclude=True)
    min_account_code: str = Field(exclude=True)
    max_account_code: str = Field(default="", exclude=True)
    debit: float = Field(serialization_alias="Debit")
    credit: float = Field(serialization_alias="Credit")
    fc_debit: float = Field(serialization_alias="FCDebit")
    fc_credit: float = Field(serialization_alias="FCCredit")
    fc_currency: str = Field(serialization_alias="FCCurrency")

    @field_validator("min_account_code")
    @classmethod
    def account_code_format(cls, v: str) -> str:
        if len(v) < 6:
            raise AttributeError(f"Valor inválido: {v}")
        return f"{v[0:6]}000"

    @field_validator("dimensions")
    @classmethod
    def save_dimensions(cls, v: str) -> str:
        if len(v) < 9:
            raise AttributeError(f"Valor inválido: {v}")
        return f"{v[9:]}"

    @field_validator("fc_currency")
    @classmethod
    def change_fc_currency(cls, v: str):
        v = "Bs"
        return v

    @model_validator(mode="after")
    def round_to_six_decimals(self) -> Self:
        self.debit = round(self.debit, 6)
        self.credit = round(self.credit, 6)
        self.fc_debit = round(self.fc_debit, 6)
        self.fc_credit = round(self.fc_credit, 6)

        return self

    @model_validator(mode="after")
    def set_max_account_code(self) -> Self:
        self.max_account_code = int(self.min_account_code) + 999
        return self

    def close_entry_line(self) -> None:
        self.account_code = f"{self.account_code}{self.dimensions}"
