#Write your starter code below
import pandas as pd

#Load the raw data 
df = pd.read_csv("data/log2.csv")

# Part 1 Prepare the  data
"""
Edgar
"""

#Question 1. Report the original number of records and list the distinct Action values.

#Prints the number of records of network traffic according to dataset
print(len(df))

#Prints a list of unique "Action values" by first selecting the column "Action" the dataset
print(df["Action"].unique())



# Question 2. Check the two required columns for missing or invalid values. Exclude affected records and report how many
# were excluded.

#Prints the number of actions that are missing within the dataset
print(df["Action"].isna().sum())

#Prints the number of destination ports that are missing within the dataset
print(df["Destination Port"].isna().sum())

#Checks and prints the dataset Destination Port values to 
#gauge possible invalid values (anything outside of network port range 0-65535)
print(df["Destination Port"].min())
print(df["Destination Port"].max())

#Prints number of values that are invalid/outside our range, all based from values in Destination Port column
print((~df["Destination Port"].between(0,65535)).sum())

#Prints the number of values that are not whole numbers, meaning they're invalid values 
print((df["Destination Port"] % 1 !=0).sum())


#Prints the number of values in the Action column that are not the 4 acceptable action values
print((~df["Action"].isin(["allow", "drop", "deny", "reset-both"])).sum())

#Transfers the cleaned/checked dataset to a copy that group members will use
df_cleaned = df.copy()


#No records excluded after checking, so excluded is simply 0
excluded_records = 0
print("Number of excluded records is: ", excluded_records)

#Prints the final number of usable records, N, which is confirmed to be all original records
N = len(df_cleaned)
print("Final number of usable records, N, is: ", N)

#Defining and implementing "Destination port" and "Firewall outcome" as two categories in dataset
def categorize_port(port):
    if port == 53:
        return "Port 53"
    elif port == 80:
        return "Port 80"
    elif port == 443:
        return "Port 443"
    else:
        return "Other"    


#Creates a new column in dataset and prints the number of each category of Destination Port
df_cleaned["X"] = df_cleaned["Destination Port"].apply(categorize_port)
print(df_cleaned["X"].value_counts())


#
def categorize_action(action):
    if action == "allow":
        return "Allowed"
    else:
        return "Not Allowed"  


#
#Creates a new column in dataset and prints the number of each category of Action
df_cleaned["Y"] = df_cleaned["Action"].apply(categorize_action)
print(df_cleaned["Y"].value_counts())

#ADD QUESTION 3 HEADER COMMENT AND DESCRIPTIONS FOR EMPTY COMMENTS

print("END OF PART 1/n")



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