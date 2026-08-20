import loan_processing


passed = 0
failed = 0


def test(test_name, condition):

    global passed
    global failed

    if condition:
        passed += 1
        print("PASS:", test_name)
    else:
        failed += 1
        print("FAIL:", test_name)


print("===== BANKING LOAN QA TESTS =====")


# 1. Minimum age
test(
    "Minimum age",
    loan_processing.approve_loan(
        18,
        50000,
        5000,
        700,
        "Salaried",
        100000
    )
)


# 2. Maximum age
test(
    "Maximum age",
    loan_processing.approve_loan(
        70,
        50000,
        5000,
        700,
        "Salaried",
        100000
    )
)


# 3. Invalid age
test(
    "Invalid age rejected",
    not loan_processing.approve_loan(
        17,
        50000,
        5000,
        700,
        "Salaried",
        100000
    )
)


# 4. Invalid salary
try:

    loan_processing.calculate_dti(
        0,
        5000
    )

    test(
        "Invalid salary exception",
        False
    )

except ValueError:

    test(
        "Invalid salary exception",
        True
    )


# 5. Poor credit score
test(
    "Poor credit score rejected",
    not loan_processing.approve_loan(
        30,
        50000,
        5000,
        500,
        "Salaried",
        100000
    )
)


# 6. High DTI
test(
    "High DTI rejected",
    not loan_processing.approve_loan(
        30,
        50000,
        30000,
        700,
        "Salaried",
        100000
    )
)


# 7. Unemployed
test(
    "Unemployed rejected",
    not loan_processing.approve_loan(
        30,
        50000,
        5000,
        700,
        "Unemployed",
        100000
    )
)


# 8. Self-employed interest
test(
    "Self-employed interest rate",
    loan_processing.calculate_interest_rate(
        700,
        "Self-Employed"
    ) == 9.0
)


# 9. EMI calculation
test(
    "EMI calculation",
    loan_processing.calculate_emi(
        100000,
        8.5,
        60
    ) > 0
)


# 10. Credit score boundary
test(
    "Credit score 650",
    loan_processing.calculate_interest_rate(
        650,
        "Salaried"
    ) == 8.5
)


# 11. Invalid credit score
try:

    loan_processing.calculate_interest_rate(
        1000,
        "Salaried"
    )

    test(
        "Invalid credit score",
        False
    )

except ValueError:

    test(
        "Invalid credit score",
        True
    )


# Final result

print("\n==============================")

if failed > 0:

    print("QA FAILED")

    print(
        "Passed:",
        passed
    )

    print(
        "Failed:",
        failed
    )

    raise SystemExit(1)


print("ALL QA TESTS PASSED")

print(
    "Total Passed:",
    passed
)