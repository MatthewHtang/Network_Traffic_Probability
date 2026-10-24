#Write your starter code below
import pandas as pd
import matplotlib.pyplot  as plt

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

# Create destination-port categories
df_cleaned["Port_Category"] = df_cleaned["Destination Port"].apply(
    lambda port: (
        "Port 53" if port == 53 else
        "Port 80" if port == 80 else
        "Port 443" if port == 443 else
        "Other"
    )
)

# Create firewall outcome categories
df_cleaned["Outcome"] = df_cleaned["Action"].apply(
    lambda action: "Allowed" if action == "allow"
    else "Not allowed"
)

# Construct the frequency table
frequency_table = pd.crosstab(
    df_cleaned["Port_Category"],
    df_cleaned["Outcome"],
    margins=True,
    margins_name="Total"
)

# Display rows and columns in the assignment's order
frequency_table = frequency_table.reindex(
    ["Port 53", "Port 80", "Port 443", "Other", "Total"],
    axis=0
)

frequency_table = frequency_table.reindex(
    ["Allowed", "Not allowed", "Total"],
    axis=1
)

print("Frequency Table\n", frequency_table)


# B. Construct the joint probability table by dividing each interior cell count by N. 𝑃̂
# (𝑋 = 𝑥, 𝑌 = 𝑦) = 𝑛ₓᵧ/𝑁
N = df_cleaned['Y'].value_counts().sum()
port_list = ["Port 53", "Port 80", "Port 443", "Other"]

P_XY = []
for port in port_list:
    for action in ["Allowed", "Not allowed"]:
        p = frequency_table.loc[port,action]
        P_XY.append((p/N))

print(N)
print(P_XY)
print("Joint Probability: " ,sum(P_XY))

#### 3 Find the probability that a record uses port 53 and is not allowed. (What percentage of all records use port 53 and are not allowed?
print("P ( Port 53 and Not Allowed ): ", frequency_table.loc["Port 53", "Not allowed"] / N)

#### 4 Find the probability that a record uses either port 80 or port 443, and is allowed. (What percentage of all records use either port 80 or port 443 and are allowed?)
print("P (Port 80 or Port 443 and Allowed) : ", (frequency_table.loc['Port 80', 'Allowed'] + frequency_table.loc['Port 443', 'Allowed'])/N)
print("Percentage of (Port 80 or Port 443 and Allowed) : ",( (frequency_table.loc['Port 80', 'Allowed'] + frequency_table.loc['Port 443', 'Allowed'])/N)*100)



# Part 3 Marginal distributions
"""
Om


Part 3 Marginal distributions 10 points
Calculate both marginal distributions by summing the joint probabilities. 𝑃̂
(𝑋 = 𝑥) = ∑𝑃̂ (𝑋 = 𝑥, 𝑌 = 𝑦)
𝑦 𝑃̂
(𝑌 = 𝑦) = ∑𝑃̂ (𝑋 = 𝑥, 𝑌 = 𝑦)
𝑥
1. Present a marginal probability table for each variable and verify that each distribution sums to 1.
2. Identify the most common destination-port category.
3. Report the overall probability that a record is allowed.
4. Explain what information is lost when examining only the marginal distribution
"""

port_list = ["Port 53", "Port 80", "Port 443", "Other"]

# Remove the Total row and Total column
counts = frequency_table.loc[
    port_list,
    ["Allowed", "Not allowed"]
]

# Total number of usable records
N = counts.to_numpy().sum()

# Joint probability table
joint_probability = counts / N

print("Joint Probability Table:")
print(joint_probability.round(4))




# Marginal Probability For X
X_list = []
for port in port_list:
    val = frequency_table.loc[port,"Allowed"] + frequency_table.loc[port ,"Not allowed" ]
    X_list.append(val/N)

print("Marginal distribution of Port \"X\" Category :\n ", port_list)
print( X_list)

# Marginal Probability For Y
Y_list = []
Y_total_value = 0
for action in ["Allowed" , "Not allowed"]:
    val = 0
    for port in port_list:
        val += frequency_table.loc[port, action]

    Y_list.append(val/N)
    Y_total_value = val

print("Marginal distribution of Y (Outcome)\n",["Allowed","Not allowed"])
print("\n",Y_list)

# Verify that each distribution sums to 1
print("Sum of marginal probability of X: " , sum(X_list))
print("Sum of marginal probability of Y: " , sum(Y_list))





print(" Q2. Identify the most common destination-port category.")
print("--> The most common destination-port category is other with probability of  0.52. After that, most common category is Port 53 with probability of 0.235.")



print(" Q3. Report the overall probability that a record is allowed")
print("Overall probability a record is allowed : ", Y_total_value / N)

print("4. Explain what information is lost when examining only the marginal distributions.\n\n--> Marginal distributions show the overall probabilities of destination-port categories and firewall outcomes separately. However, they do not show how firewall outcomes vary across different destination-port categories. For example, the marginal distribution tells us the overall proportion of allowed records but does not tell us whether records using Port 53, Port 80, or Port 443 are more likely to be allowed. To understand the relationship between destination port and firewall outcome, we need the joint or conditional distributions.")






# Part 4 Conditional distributions
"""
Om

 Part 4 Conditional distributions 20 points
Calculate the following probabilities. For each, show the numerator and denominator, report the probability,
and interpret it in context. 𝑃̂
(𝑌 = 𝐴𝑙𝑙𝑜𝑤𝑒𝑑 | 𝑋 = 𝑃𝑜𝑟𝑡 443), 𝑃̂ (𝑋 = 𝑃𝑜𝑟𝑡 443|𝑌 = 𝐴𝑙𝑙𝑜𝑤𝑒𝑑 ) 𝑃̂
(𝑌 = 𝑁𝑜𝑡 𝑎𝑙𝑙𝑜𝑤𝑒𝑑 | 𝑋 = 𝑃𝑜𝑟𝑡 53),𝑃̂ ( 𝑋 = 𝑃𝑜𝑟𝑡 53 | 𝑌 = 𝑁𝑜𝑡 𝑎𝑙𝑙𝑜𝑤𝑒𝑑)
If the conditioning category has no records, report the probability as undefined and explain why.
1. Construct the conditional distribution of firewall outcome within each destination-port category. Verify that each nonempty row sums to 1.
2. Create a bar chart comparing the probability of being allowed across the four port categories. Provide the
underlying values in a table.
3. Explain why P(Allowed | Port 443) and P(Port 443 | Allowed) answer different questions




What is a conditional probability?
A conditional probability asks: What is the probability of an event when we already know another event has happened?
"""


print("Condtional Probability")

print("P(Y = Allowed | X  = Port 443 ): ", frequency_table.loc["Port 443","Allowed"] / frequency_table.loc["Port 443",'Total'])
print("P(X = Port 443 | Y = Allowed )  ", frequency_table.loc["Port 443","Allowed"] / frequency_table.loc["Total",'Allowed'])
print("P(Y = Not allowed | X = Port 53 ) :  ", frequency_table.loc["Port 53","Not allowed"] / frequency_table.loc["Port 53","Total"])
print("P(X = Port 53 | Y = Not allowed ) :  ", frequency_table.loc["Port 53","Not allowed"] / frequency_table.loc["Total", "Not allowed"])

# 1. Construct the conditional distribution of firewall outcome within each destination-port category. Verify that each nonempty row sums to 1.



# Conditional distribution of firewall outcome within each port
conditional_table = counts.div(counts.sum(axis=1), axis=0)

print("\nConditional distribution:")
print(conditional_table.round(4))

print("\nRow sums:")
print(conditional_table.sum(axis=1).round(4))


# 2. Create a bar chart comparing the probability of being allowed across the four port categories. Provide the
# underlying values in a table.


plt.bar( port_list ,conditional_table["Allowed"])
plt.xlabel("Destination Port Categories")
plt.ylabel("Probability of Being Allowed")
plt.title("Probability of Being Allowed by Destination Port Category")
plt.show()



print("""3. Explain why P(Allowed | Port 443) and P(Port 443 | Allowed) answer different questions.

--> P(Allowed | Port 443) provides the probability of Port 443 and firewall outcome Allowed given all the sum of all the Port 443 destination category.

Meanwhile, P(Port 443 | Allowed) provides the probability of Port 443 and Allowed out of all the Allowed firewall outcome.

Although, the numerator is same for both the denominator is defferent.

P(Allowed | Port 443)  = n(Allowed | Port 443)/ n(Port 443)

P(Port 443 | Allowed)  = n(Port 443 | Allowed )/ n(Allowed)
""")




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