import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------------------------------------------------
# Step 1: Load the analysed data from Task 3
# ---------------------------------------------------------

input_file = "data/trends_analysed.csv"

df = pd.read_csv(input_file)

print(f"Loaded {len(df)} stories from {input_file}")


# Create the outputs folder if it doesn't already exist.
os.makedirs("outputs", exist_ok=True)


# ---------------------------------------------------------
# Chart 1: Top 10 Stories by Score
# ---------------------------------------------------------

# Sort stories by score and select the top 10.
top_stories = df.sort_values(
    by="score",
    ascending=False
).head(10).copy()


# Shorten titles that are longer than 50 characters.
# This keeps the chart readable.
top_stories["short_title"] = top_stories["title"].apply(
    lambda title: title[:50] + "..."
    if len(title) > 50
    else title
)


plt.figure(figsize=(10, 7))

plt.barh(
    top_stories["short_title"],
    top_stories["score"]
)

# Reverse the y-axis so the highest score appears at the top.
plt.gca().invert_yaxis()

plt.title("Top 10 HackerNews Stories by Score")
plt.xlabel("Score")
plt.ylabel("Story Title")

plt.tight_layout()

# Save BEFORE showing the chart.
plt.savefig(
    "outputs/chart1_top_stories.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# Close the figure before creating the next chart.
plt.close()


# ---------------------------------------------------------
# Chart 2: Stories per Category
# ---------------------------------------------------------

# Count the number of stories in each category.
category_counts = df["category"].value_counts()


plt.figure(figsize=(9, 6))

# Passing one value per category gives each bar a different
# default Matplotlib colour.
plt.bar(
    category_counts.index,
    category_counts.values
)

plt.title("Number of Stories per Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")

plt.xticks(rotation=20)

plt.tight_layout()

# Save BEFORE showing the chart.
plt.savefig(
    "outputs/chart2_categories.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ---------------------------------------------------------
# Chart 3: Score vs Comments
# ---------------------------------------------------------

plt.figure(figsize=(10, 7))


# Separate popular and non-popular stories.
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]


# Plot non-popular stories.
plt.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)


# Plot popular stories separately so they have a different
# colour and can be identified using the legend.
plt.scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)


plt.title("Story Score vs Number of Comments")
plt.xlabel("Score")
plt.ylabel("Number of Comments")

plt.legend()

plt.tight_layout()

# Save BEFORE showing the chart.
plt.savefig(
    "outputs/chart3_scatter.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ---------------------------------------------------------
# Bonus: TrendPulse Dashboard
# ---------------------------------------------------------

# Create a 2x2 dashboard.
fig, axes = plt.subplots(
    2,
    2,
    figsize=(16, 11)
)

fig.suptitle(
    "TrendPulse Dashboard",
    fontsize=18
)


# ---------------------------------------------------------
# Dashboard Chart 1
# ---------------------------------------------------------

axes[0, 0].barh(
    top_stories["short_title"],
    top_stories["score"]
)

axes[0, 0].invert_yaxis()

axes[0, 0].set_title("Top 10 Stories by Score")
axes[0, 0].set_xlabel("Score")
axes[0, 0].set_ylabel("Story Title")


# ---------------------------------------------------------
# Dashboard Chart 2
# ---------------------------------------------------------

axes[0, 1].bar(
    category_counts.index,
    category_counts.values
)

axes[0, 1].set_title("Stories per Category")
axes[0, 1].set_xlabel("Category")
axes[0, 1].set_ylabel("Number of Stories")

axes[0, 1].tick_params(
    axis="x",
    rotation=20
)


# ---------------------------------------------------------
# Dashboard Chart 3
# ---------------------------------------------------------

axes[1, 0].scatter(
    not_popular["score"],
    not_popular["num_comments"],
    label="Not Popular",
    alpha=0.7
)

axes[1, 0].scatter(
    popular["score"],
    popular["num_comments"],
    label="Popular",
    alpha=0.7
)

axes[1, 0].set_title("Score vs Comments")
axes[1, 0].set_xlabel("Score")
axes[1, 0].set_ylabel("Number of Comments")

axes[1, 0].legend()


# ---------------------------------------------------------
# Dashboard fourth panel
# ---------------------------------------------------------

# The assignment only requires three charts, so the fourth
# panel is used to display a simple summary.
axes[1, 1].axis("off")

summary_text = (
    f"Total Stories: {len(df)}\n\n"
    f"Average Score: {df['score'].mean():.2f}\n\n"
    f"Average Comments: {df['num_comments'].mean():.2f}\n\n"
    f"Most Common Category:\n"
    f"{category_counts.idxmax()}"
)

axes[1, 1].text(
    0.5,
    0.5,
    summary_text,
    ha="center",
    va="center",
    fontsize=14
)


# Adjust spacing between dashboard elements.
plt.tight_layout(rect=[0, 0, 1, 0.95])


# Save the complete dashboard BEFORE showing it.
plt.savefig(
    "outputs/dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

plt.close()


# ---------------------------------------------------------
# Final confirmation
# ---------------------------------------------------------

print("\nVisualization complete!")

print("Created files:")
print("  outputs/chart1_top_stories.png")
print("  outputs/chart2_categories.png")
print("  outputs/chart3_scatter.png")
print("  outputs/dashboard.png")
