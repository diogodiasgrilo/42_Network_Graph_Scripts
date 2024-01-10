import json

#Read the data from the links.js file
with open('./student_evaluations/links.js', 'r') as file:
    data = file.read().replace('var links = ', '')[:-1]

# Parse the data as JSON
links = json.loads(data)

# Create sets to store the pairs and identify the flipped pairs
pairs_set = set()
flipped_pairs = set()

# Loop through the links and identify unique and flipped pairs
for link in links:
    pair = frozenset([link["source"], link["target"]])
    if pair in pairs_set:
        flipped_pairs.add(pair)
    pairs_set.add(pair)

# Print the results
if flipped_pairs:
    print("Flipped pairs found:")
    for pair in flipped_pairs:
        print(list(pair))
else:
    print("No flipped pairs found.")
