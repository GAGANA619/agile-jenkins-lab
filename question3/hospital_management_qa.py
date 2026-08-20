import hospital_management


passed = 0
failed = 0


def check(name, condition):

    global passed
    global failed

    if condition:
        passed += 1
        print("PASS:", name)

    else:
        failed += 1
        print("FAIL:", name)


print("===== HOSPITAL QA TESTS =====")


# 1. Normal consultation
check(
    "Normal consultation",
    hospital_management.consultation_fee(
        "Normal",
        20
    ) == 500
)


# 2. Emergency consultation
check(
    "Emergency fee higher",
    hospital_management.consultation_fee(
        "Emergency",
        20
    ) > 500
)


# 3. Long consultation
check(
    "Long consultation fee",
    hospital_management.consultation_fee(
        "Normal",
        45
    ) > 500
)


# 4. Follow-up discount
check(
    "Follow-up discount",
    hospital_management.consultation_fee(
        "Follow-up",
        20
    ) < 500
)


# 5. Lab charges
check(
    "Lab total",
    hospital_management.lab_charges(
        [100, 200]
    ) == 300
)


# 6. Medicine charges
check(
    "Medicine total",
    hospital_management.medicine_charges(
        [100, 50]
    ) == 150
)


# 7. Insurance reduces payable
insured = hospital_management.patient_payable(
    "Normal",
    20,
    1000,
    500,
    True
)

uninsured = hospital_management.patient_payable(
    "Normal",
    20,
    1000,
    500,
    False
)

check(
    "Insurance reduces payable",
    insured < uninsured
)


# 8. Invalid duration
try:

    hospital_management.consultation_fee(
        "Normal",
        0
    )

    check(
        "Invalid duration rejected",
        False
    )

except ValueError:

    check(
        "Invalid duration rejected",
        True
    )


print("\n==============================")

if failed > 0:

    print("QA TESTS FAILED")

    print("Passed:", passed)

    print("Failed:", failed)

    raise SystemExit(1)


print("ALL QA TESTS PASSED")

print("Total Passed:", passed)
