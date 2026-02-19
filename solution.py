import pandas as pd

# List of files
files = [
    "data/daily_sales_data_0.csv",
    "data/daily_sales_data_1.csv",
    "data/daily_sales_data_2.csv"
]

# Read and combine all CSV files
df_list = []

for file in files:
    df = pd.read_csv(file)
    df_list.append(df)

# Combine into one dataframe
combined_df = pd.concat(df_list, ignore_index=True)

# -----------------------------
# Data Cleaning & Transformation
# -----------------------------

# Keep only Pink Morsels
filtered_df = combined_df[combined_df["product"] == "pink morsel"]

# Remove dollar sign and convert price to float
filtered_df["price"] = filtered_df["price"].replace('[\$,]', '', regex=True).astype(float)

# Calculate sales
filtered_df["Sales"] = filtered_df["price"] * filtered_df["quantity"]

# Select required columns
final_df = filtered_df[["Sales", "date", "region"]]

# Rename columns
final_df.columns = ["Sales", "Date", "Region"]

# Save output file
final_df.to_csv("formatted_sales_output.csv", index=False)

print("✅ Output file created: formatted_sales_output.csv")
 