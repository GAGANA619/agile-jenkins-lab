def consultation_fee(consultation_type, minutes):
    if minutes <= 0:
        raise ValueError("Invalid duration")

    if consultation_type.lower() == "emergency":
        fee = 1000
    else:
        fee = 500

    if minutes > 30:
        fee += 300

    if consultation_type.lower() == "follow-up":
        fee *= 0.5

    return fee


def lab_charges(tests):
    total = 0

    if tests is None:
        return 0

    for test in tests:
        if test < 0:
            raise ValueError("Invalid lab charge")

        total += test

    return total


def medicine_charges(medicines):
    total = 0

    if medicines is None:
        return 0

    for medicine in medicines:
        if medicine < 0:
            raise ValueError("Invalid medicine charge")

        total += medicine

    return total


def insurance_coverage(total, insured):
    if total < 0:
        raise ValueError("Invalid total")

    if insured:
        return total * 0.70

    return 0


def patient_payable(
    consultation_type,
    minutes,
    lab,
    medicine,
    insured
):
    consultation = consultation_fee(
        consultation_type,
        minutes
    )

    total = (
        consultation
        + lab
        + medicine
    )

    coverage = insurance_coverage(
        total,
        insured
    )

    return total - coverage


def main():

    print("===== HOSPITAL APPOINTMENT & BILLING =====")

    consultation_type = input(
        "Consultation Type: "
    )

    minutes = float(
        input("Consultation Minutes: ")
    )

    lab = float(
        input("Lab Charges: ")
    )

    medicine = float(
        input("Medicine Charges: ")
    )

    insured_input = input(
        "Insurance (yes/no): "
    )

    insured = (
        insured_input.lower() == "yes"
    )

    payable = patient_payable(
        consultation_type,
        minutes,
        lab,
        medicine,
        insured
    )

    print("\n===== BILL =====")

    print(
        "Patient Payable:",
        round(payable, 2)
    )


if __name__ == "__main__":
    main()
