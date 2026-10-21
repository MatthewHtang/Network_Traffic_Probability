#Write your starter code below
import pandas as pd

#Load the raw data 
df = pd.read_csv("data/log2.csv")

# Part 1 Prepare the  data
"""
Edgar
"""

# Part 2 Joint distribution
"""
Edgar
"""

# Part 3 Marginal distributions
"""
Om
"""

# Part 4 Conditional distributions
"""
Om
"""

# Part 5 Interpretation and independence
"""
Akshay
"""

# Part 6 Flow size and average packet size
"""
1. Construct a 3 × 3 frequency table of F versus A, including row and column totals. Convert it to a joint
probability table by dividing each interior count by M. Verify that the nine joint probabilities sum to 1. 
"""
# Keep only the rows where packets it atleast 1
# To calculate average bytes per packet we will divide Bytes by Packets,
# If packets are 0, division is impossible

df = df[df["Packets"] >= 1]

# Compute the bytes per packet for every rows 
# and store it in a new column called "Avg"
df ["Avg"] = df["Bytes"] / df["Packets"]

# Create a function that take Bytes value and return its F bucket
def label_F(bytes_value):
    if bytes_value >= 0 and bytes_value < 1000:
        return "F: Small"

    elif bytes_value >= 1000 and bytes_value < 10000:
        return "F: Medium"

    elif bytes_value >= 10000:
        return "F: Large"

# Create a function that takes one avg value and returns its A bucket
def label_A (avg_value):
    if avg_value >= 0 and avg_value < 200:
        return "A: Small"

    elif avg_value >= 200 and avg_value < 800:
        return "A: Medium"

    elif avg_value >= 800:
        return "A: Large"

# Apply each function to every row
df["F_label"] = df["Bytes"].apply(label_F)
df["A_label"] = df["Avg"].apply(label_A)

#Create a table
table = pd.crosstab(df["F_label"], df["A_label"], margins=True, margins_name="Total")

print("\n---------- 3 × 3 Frequency Table of F versus A ----------\n",table)

# Convert it to a joint probability table by dividing each interior count by M
# Get the conor value
m = table.loc["Total", "Total"]
joint_prob_table = table / m

print("\n\n---------- Joint Probability Table ----------\n", joint_prob_table)
print("\nThe sum of the nine joint probabilities: ", joint_prob_table.loc["Total", "Total"])


"""
2. Calculate both marginal distributions. Report the probabilities of a Large flow and a Large average bytes per
packet. Interpret each result.
"""
# Calculate marginal distribution for F
p_f_small = round(joint_prob_table.loc["F: Small", "Total"], 6)
p_f_medium = round(joint_prob_table.loc["F: Medium", "Total"], 6)
p_f_large = round(joint_prob_table.loc["F: Large", "Total"], 6)

# Calculate marginal distribution for A
p_a_small = round(joint_prob_table.loc["Total", "A: Small"], 6)
p_a_medium = round(joint_prob_table.loc["Total", "A: Medium"], 6)
p_a_large = round(joint_prob_table.loc["Total", "A: Large"], 6)

print(f"\n\n---------- Marginal Distribution for F ----------\n"
      f"P(F:Small) = {p_f_small}\n"
      f"P(F: Medium) = {p_f_medium}\n"
      f"P(F: Large) = {p_f_large}")

print(f"\n\n---------- Marginal Distribution for A ----------\n"
      f"P(A:Small) = {p_a_small}\n"
      f"P(A: Medium) = {p_a_medium}\n"
      f"P(A: Large) = {p_a_large}")

print("\nProbability of a Large Flow: ", round(table.loc["F: Large", "Total"]/m, 6))
print("Probability of a Large Average Bytes per packet: ", round(table.loc["Total", "A: Large"]/m, 6))

"""
3. Calculate P(F = Large, A = Small), P(A = Large | F = Large), and P(F = Large | A = Large). Show the counts and
denominator for each. If a conditioning category is empty, report the conditional probability as undefined. (6
points)

"""