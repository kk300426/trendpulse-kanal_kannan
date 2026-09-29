import pandas as pd
import glob
import os


# ---------------------------------------------------------
# Step 1: Find and load the JSON file created by Task 1
# ---------------------------------------------------------

json_files = glob.glob("data/trends_*.json")

if not json_files:
    print("Error: No trends JSON file found in the data folder.")
    exit()

# Use the first matching Task 1 JSON file
json_file = json_files[0]

# Load the JSON data into a Pandas DataFrame
df = pd.read_json(json_file)

print(f"Loaded {len(df)} stories from {json_file}")


# ---------------------------------------------------------
# Step 2: Remove duplicate stories
# ---------------------------------------------------------

# post_id uniquely identifies a HackerNews story.
# Keep the first occurrence when duplicate IDs are found.
df = df.drop_duplicates(subset="post_id")

print(f"After removing duplicates: {len(df)}")


# ---------------------------------------------------------
# Step 3: Remove rows with required missing values
# ---------------------------------------------------------

# post_id, title and score are required fields.
# Rows missing any of these values cannot be used reliably.
df = df.dropna(subset=["post_id", "title", "score"])

print(f"After removing nulls: {len(df)}")


# ---------------------------------------------------------
# Step 4: Fix data types
# ---------------------------------------------------------

# Convert score and num_comments to numeric values.
# Invalid values are converted to NaN instead of crashing.
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["num_comments"] = pd.to_numeric(
    df["num_comments"],
    errors="coerce"
)

# Remove rows where the conversion created missing values.
df = df.dropna(subset=["score", "num_comments"])

# Convert both columns to integers.
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)


# ---------------------------------------------------------
# Step 5: Remove low-quality stories
# ---------------------------------------------------------

# Keep only stories with at least 5 upvotes.
df = df[df["score"] >= 5]

print(f"After removing low scores: {len(df)}")


# ---------------------------------------------------------
# Step 6: Clean whitespace from titles
# ---------------------------------------------------------

# Remove unnecessary spaces at the beginning/end of titles.
df["title"] = df["title"].str.strip()


# ---------------------------------------------------------
# Step 7: Save the cleaned data as CSV
# ---------------------------------------------------------

output_file = "data/trends_clean.csv"

df.to_csv(output_file, index=False)

print()
print(f"Saved {len(df)} rows to {output_file}")


# ---------------------------------------------------------
# Step 8: Print stories per category
# ---------------------------------------------------------

print()
print("Stories per category:")

category_counts = df["category"].value_counts()

for category, count in category_counts.items():
    print(f"  {category:<15} {count}")
