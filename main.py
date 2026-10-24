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

# X = Destination Port Category
# Y = Firewall Action (Allowed / Not Allowed)

port_order = ["Port 53", "Port 80", "Port 443", "Other"]
outcome_order = ["Allowed", "Not Allowed"]

# Create the frequency table
counts = pd.crosstab(df_cleaned["X"], df_cleaned["Y"])

# Ensure all categories appear in the correct order
counts = counts.reindex(
    index=port_order,
    columns=outcome_order,
    fill_value=0
)

# Calculate total records
N = len(df_cleaned)

# Calculate joint probabilities
joint_prob = counts / N

# Calculate marginal probabilities
p_port = counts.sum(axis=1) / N
p_outcome = counts.sum(axis=0) / N

"""
1. If X and Y were independent, they would satisfy the relationship below. Compare the observed joint
probability with the product of the marginal probabilities for two cells in your table. Show the calculations.
𝑃(𝑋 = 𝑥, 𝑌 = 𝑦) = 𝑃(𝑋 = 𝑥)𝑃(𝑌 = 𝑦)

"""
print("\n" + "=" * 60)
print("PART 5 - QUESTION 1: TEST OF INDEPENDENCE")
print("=" * 60)

print("\nJoint Frequency Table:")
print(counts)

print("\nJoint Probability Table:")
print(joint_prob.round(6))

cells_to_test = [
    ("Port 443", "Allowed"),
    ("Port 53", "Not Allowed")
]

for port, outcome in cells_to_test:

    observed_probability = joint_prob.loc[port, outcome]

    expected_probability = (
        p_port.loc[port] * p_outcome.loc[outcome]
    )

    difference = abs(
        observed_probability - expected_probability
    )

    print(f"\nCell: {port} and {outcome}")
    print(f"P(X={port}, Y={outcome}) = "
          f"{observed_probability:.6f}")

    print(f"P(X={port}) * P(Y={outcome}) = "
          f"{expected_probability:.6f}")

    print(f"Absolute Difference = {difference:.6f}")

    if difference < 0.000001:
        print("Interpretation: These probabilities are "
              "approximately equal for this cell.")
    else:
        print("Interpretation: These probabilities differ "
              "for this cell, so this cell does not satisfy "
              "the independence equation exactly.")

print(
    "\nWritten Interpretation for Question 1:\n"
    "For Port 443 and Allowed, the joint probability is "
    "0.178188, while the product of the marginal probabilities "
    "is 0.102408. For Port 53 and Not Allowed, the joint "
    "probability is 0.000443, while the product of the marginal "
    "probabilities is 0.100112. Since these values are different, "
    "the independence equation does not hold for these selected "
    "cells. This suggests that destination port category and "
    "firewall action are associated in this dataset. However, "
    "checking two cells alone is not a complete test of "
    "independence for the entire table."
)

"""

2. Compare the overall allowance probability with the allowance probability within each port category. Does the
dataset suggest an association between port category and firewall outcome? Support your answer with
numbers. A formal hypothesis test is not required.

"""

print("\n" + "=" * 60)
print("PART 5 - QUESTION 2: ALLOWANCE PROBABILITIES")
print("=" * 60)

# Overall probability that a connection is allowed
overall_allowed = counts["Allowed"].sum() / N

print(f"\nOverall Allowance Probability: "
      f"{overall_allowed:.6f}")

results = []

for port in port_order:

    total_records = counts.loc[port].sum()
    allowed_records = counts.loc[port, "Allowed"]

    if total_records > 0:
        conditional_probability = (
            allowed_records / total_records
        )
    else:
        conditional_probability = float("nan")

    difference = conditional_probability - overall_allowed

    results.append({
        "Port Category": port,
        "Total Records": total_records,
        "Allowed Records": allowed_records,
        "P(Allowed | Port)": conditional_probability,
        "Difference from Overall": difference
    })

allowance_table = pd.DataFrame(results)

print("\nConditional Allowance Probability Table:")
print(allowance_table.to_string(
    index=False,
    formatters={
        "P(Allowed | Port)": lambda x: f"{x:.6f}",
        "Difference from Overall": lambda x: f"{x:.6f}"
    }
))

print(
    "\nWritten Interpretation for Question 2:\n"
    f"The overall allowance probability is {overall_allowed:.6f} "
    f"({overall_allowed * 100:.2f}%). "
    "The conditional allowance probabilities are approximately "
    "99.81% for Port 53, 99.83% for Port 80, "
    "99.94% for Port 443, and 19.04% for Other. "
    "This shows that almost all traffic in the three specified "
    "port categories was allowed, while only about 19.04% of "
    "traffic in the Other category was allowed. These differences "
    "suggest an association between destination port category "
    "and firewall action in this dataset. However, association "
    "does not prove causation, and traffic in the Other category "
    "is not necessarily malicious."
)

"""
3. Explain why “not allowed” does not automatically mean malicious traffic.

"""
print("\n" + "=" * 60)
print("PART 5 - QUESTION 3: FIREWALL INTERPRETATION")
print("=" * 60)

print(
    "\nWritten Answer:\n"
    "A connection marked as 'Not Allowed' does not necessarily "
    "mean that it is malicious. A firewall may block legitimate "
    "traffic because of security policies, restricted ports, "
    "network configurations, or access-control rules. For "
    "example, a legitimate application might attempt to use "
    "a port that the firewall does not permit. Therefore, the "
    "firewall action tells us whether traffic was permitted, "
    "not whether it was definitely safe or dangerous. Additional "
    "information, such as source addresses, destinations, "
    "traffic patterns, and security alerts, would be needed "
    "to determine whether a connection is suspicious."
)

"""
4. Write a 100–150-word conclusion summarizing your findings and explaining why results from this firewall may
not represent all networks.

"""
print("\n" + "=" * 60)
print("PART 5 - QUESTION 4: CONCLUSION AND LIMITATIONS")
print("=" * 60)

conclusion = (
    "This analysis examined the relationship between destination "
    "port categories and firewall actions using joint, marginal, "
    "and conditional probabilities. The independence calculations "
    "compared observed joint probabilities with the products of "
    "marginal probabilities for selected combinations. The "
    "conditional allowance probabilities for Ports 53, 80, 443, "
    "and Other were compared with the overall allowance "
    "probability to investigate whether firewall decisions varied "
    "across port categories. The calculated results should be "
    "used to describe the strength of any observed association. "
    "However, a connection marked as 'Not Allowed' is not "
    "necessarily malicious because firewalls can block legitimate "
    "traffic for security or configuration reasons. One limitation "
    "is that this dataset represents a particular network "
    "environment and may not represent all networks. Furthermore, "
    "probability comparisons identify associations, not causation, "
    "and cannot independently determine whether traffic is "
    "malicious."
)

print("\nConclusion:")
print(conclusion)

print("\nWord Count:", len(conclusion.split()))

print("\n" + "=" * 60)
print("END OF PART 5")
print("=" * 60)


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