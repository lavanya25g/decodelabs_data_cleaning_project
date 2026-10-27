import pandas as pd

# Load the original data and keep an untouched backup
df = pd.read_excel("Dataset_for_Data_Analytics.xlsx")
df_raw = df.copy()

print("Shape (rows, columns):", df.shape)
print()
df.info()
print()
print("Empty cells per column:")
print(df.isna().sum())
print()
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate OrderIDs:", df["OrderID"].duplicated().sum())
# CR001: fill blank CouponCode with "No Coupon"
blank_before = df["CouponCode"].isna().sum()
df["CouponCode"] = df["CouponCode"].fillna("No Coupon")
blank_after = df["CouponCode"].isna().sum()

print()
print("CR001 - blank CouponCode before:", blank_before)
print("CR001 - blank CouponCode after:", blank_after)
print(df["CouponCode"].value_counts())
# CR002: check and remove duplicate OrderIDs
rows_before = len(df)
df = df.drop_duplicates(subset="OrderID", keep="first")
rows_after = len(df)

print()
print("CR002 - rows before:", rows_before)
print("CR002 - rows after:", rows_after)
print("CR002 - duplicates removed:", rows_before - rows_after)
# CR003: trim spaces in text columns
text_cols = ["Product", "ShippingAddress", "PaymentMethod",
             "OrderStatus", "ReferralSource", "CouponCode"]
trimmed = 0
for col in text_cols:
    cleaned = df[col].str.strip()
    trimmed += (cleaned != df[col]).sum()
    df[col] = cleaned
print()
print("CR003 - values changed by trimming:", trimmed)

# Case check: same value written in different cases?
for col in ["Product", "PaymentMethod", "OrderStatus", "ReferralSource"]:
    print(col, "| distinct:", df[col].nunique(),
          "| distinct ignoring case:", df[col].str.lower().nunique())

# CR004: round prices to 2 decimals
for col in ["UnitPrice", "TotalPrice"]:
    rounded = df[col].round(2)
    print("CR004 -", col, "values changed by rounding:", (rounded != df[col]).sum())
    df[col] = rounded

# CR005: dates must be real dates
bad_dates = pd.to_datetime(df["Date"], errors="coerce").isna().sum()
print("CR005 - dates that are not valid:", bad_dates)
print("Date type:", df["Date"].dtype)
print("Date range:", df["Date"].min().date(), "to", df["Date"].max().date())
# CR006: final verification on the cleaned data
dup_ids = df["OrderID"].duplicated().sum()
bad_dates = pd.to_datetime(df["Date"], errors="coerce").isna().sum()
empty_cells = df.isna().sum().sum()

print()
print("FINAL CHECK (in memory)")
print("Duplicate OrderIDs:", dup_ids)
print("Invalid dates:", bad_dates)
print("Empty cells:", empty_cells)
print("Rows, columns:", df.shape)

# Save the cleaned data (dates shown as yyyy-mm-dd)
with pd.ExcelWriter("Dataset_Cleaned_Python.xlsx", engine="openpyxl",
                    date_format="yyyy-mm-dd",
                    datetime_format="yyyy-mm-dd") as writer:
    df.to_excel(writer, index=False, sheet_name="Cleaned_Data")

df.to_csv("Dataset_Cleaned_Python.csv", index=False, date_format="%Y-%m-%d")

# Read the saved file back and prove it again
saved = pd.read_excel("Dataset_Cleaned_Python.xlsx")
dates = pd.to_datetime(saved["Date"], errors="coerce")
bad_format = (~dates.dt.strftime("%Y-%m-%d").str.fullmatch(r"\d{4}-\d{2}-\d{2}", na=False)).sum()

print()
print("FINAL CHECK (read back from saved file)")
print("Rows, columns:", saved.shape)
print("Duplicate OrderIDs:", saved["OrderID"].duplicated().sum())
print("Invalid or wrongly formatted dates:", bad_format)
print("Empty cells:", saved.isna().sum().sum())

assert saved["OrderID"].duplicated().sum() == 0
assert bad_format == 0
assert saved.isna().sum().sum() == 0
print("ALL CHECKS PASSED")
