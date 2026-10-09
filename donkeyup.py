import random

# -----------------------------
# Step 1: Nominals introduce placeholders
# -----------------------------

def introduce_placeholders(entity_type, count=3):
    """Create placeholder entities."""
    return [
        {"id": f"{entity_type}_{i+1}", "type": entity_type}
        for i in range(count)
    ]


# -----------------------------
# Step 2: Relative clause updates placeholder properties
# -----------------------------

def apply_relative_clause(farmers, donkeys):
    """
    Relative clause 'who owns a donkey' runs FIRST.
    It tags each farmer with ownership property in memory.
    """

    print("=" * 60)
    print("PHASE 1: RELATIVE CLAUSE EXECUTION")
    print("'who owns a donkey' - tagging placeholders with properties")
    print("=" * 60)

    memory = {}

    donkey_pool = donkeys.copy()

    # NEW: randomize which farmers get processed first
    farmer_pool = farmers.copy()
    random.shuffle(farmer_pool)

    print(f"\nInitial farmers: {[f['id'] for f in farmer_pool]}")
    print(f"Available donkeys: {[d['id'] for d in donkey_pool]}\n")

    for farmer in farmer_pool:

        if donkey_pool:

            owned_donkey = random.choice(donkey_pool)
            donkey_pool.remove(owned_donkey)

            memory[farmer['id']] = {
                "farmer": farmer,
                "donkeys": [owned_donkey]
            }

            print(
                f"✓ TAGGED: {farmer['id']} now HAS PROPERTY: owns {owned_donkey['id']}"
            )

        else:

            memory[farmer['id']] = {
                "farmer": farmer,
                "donkeys": []
            }

            print(f"✗ UNTAGGED: {farmer['id']} owns no donkey")

    return memory


# -----------------------------
# Step 3: Determiner filters based on properties
# -----------------------------

def apply_determiner(memory, determiner_type="every"):
    """
    Determiner 'every' quantifies over ONLY those farmers
    who were tagged with donkey-ownership property.
    """

    print("\n" + "=" * 60)
    print("PHASE 2: DETERMINER FILTERING")
    print(f"'{determiner_type} farmer who owns a donkey' - filtering domain")
    print("=" * 60)

    donkey_owners = [
        record
        for record in memory.values()
        if len(record['donkeys']) > 0
    ]

    print(f"\nAll farmers: {list(memory.keys())}")

    print(
        f"Farmers WITH property (donkey-owners): "
        f"{[r['farmer']['id'] for r in donkey_owners]}"
    )

    print(
        f"Farmers WITHOUT property: "
        f"{[r['farmer']['id'] for r in memory.values() if len(r['donkeys']) == 0]}"
    )

    return donkey_owners


# -----------------------------
# Step 4: Matrix predicate runs with tagged placeholders
# -----------------------------

def run_matrix_predicate(donkey_owners, determiner_type="every"):
    """
    Matrix predicate 'beats it' runs using the memory
    of which donkey belongs to which farmer.
    """

    print("\n" + "=" * 60)
    print("PHASE 3: MATRIX PREDICATE EXECUTION")
    print(f"'{determiner_type} farmer who owns a donkey beats it'")
    print("=" * 60)

    if determiner_type == "every":

        print("\nSIMULATING EACH DONKEY-OWNER:\n")

        for record in donkey_owners:

            farmer = record['farmer']
            donkey = record['donkeys'][0]

            print(
                f"▶ {farmer['id']} beats {donkey['id']} "
                f"(retrieved from memory)"
            )

        print(f"\n✓ Simulated {len(donkey_owners)} beating events")

    elif determiner_type == "no":

        print(
            f"\nNo farmer who owns a donkey beats it → "
            f"{len(donkey_owners)} events suppressed"
        )

    elif determiner_type == "two":

        print("\nTwo farmers who own a donkey beat it → (first two only)")


# -----------------------------
# Step 5: Run the complete simulation
# -----------------------------

print("\n" + "★" * 60)
print("SIMULATION: 'Every farmer who owns a donkey beats it'")
print("★" * 60 + "\n")

# Initialize placeholders

farmers = introduce_placeholders("farmer", count=4)
donkeys = introduce_placeholders("donkey", count=3)

# 1. RELATIVE CLAUSE FIRST
ownership_memory = apply_relative_clause(farmers, donkeys)

# 2. DETERMINER SECOND
donkey_owners = apply_determiner(ownership_memory, "every")

# 3. MATRIX PREDICATE LAST
run_matrix_predicate(donkey_owners, "every")

print("\n" + "★" * 60)
print("KEY INSIGHT: Relative clauses MUST run before determiners")
print("because they establish the properties determiners filter by.")
print("★" * 60)