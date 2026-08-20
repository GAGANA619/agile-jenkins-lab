def calculate_dti(monthly_salary, existing_loan):
    if monthly_salary <= 0:
        raise ValueError("Salary must be greater than zero")

    return existing_loan / monthly_salary


def calculate_eligible_loan(salary, credit_score, existing_loan):

    if salary <= 0:
        raise ValueError("Invalid salary")

    if existing_loan < 0:
        raise ValueError("Invalid existing loan")

    if credit_score < 600:
        return 0

    if credit_score >= 750:
        multiplier = 4
    elif credit_score >= 650:
        multiplier = 3
    else:
        multiplier = 2

    return max(
        0,
        salary * 12 * multiplier - existing_loan
    )


def calculate_interest_rate(credit_score, employment_type):

    if credit_score < 300 or credit_score > 900:
        raise ValueError("Invalid credit score")

    if credit_score >= 750:
        rate = 7.0
    elif credit_score >= 650:
        rate = 8.5
    else:
        rate = 10.0

    if employment_type.lower() == "self-employed":
        rate += 0.5

    if employment_type.lower() == "unemployed":
        rate += 2.0

    return rate


def calculate_emi(principal, annual_rate, months):

    if principal <= 0 or annual_rate < 0 or months <= 0:
        raise ValueError("Invalid EMI input")

    monthly_rate = annual_rate / 1200

    if monthly_rate == 0:
        return principal / months

    emi = (
        principal
        * monthly_rate
        * (1 + monthly_rate) ** months
        / ((1 + monthly_rate) ** months - 1)
    )

    return emi


def approve_loan(
    age,
    salary,
    existing_loan,
    credit_score,
    employment_type,
    requested_loan
):

    if age < 18 or age > 70:
        return False

    if salary <= 0:
        return False

    if existing_loan < 0:
        return False

    if requested_loan <= 0:
        return False

    dti = calculate_dti(
        salary,
        existing_loan
    )

    eligible = calculate_eligible_loan(
        salary,
        credit_score,
        existing_loan
    )

    return (
        credit_score >= 650
        and employment_type.lower() != "unemployed"
        and dti <= 0.5
        and requested_loan <= eligible
    )


def main():

    print("===== BANKING LOAN APPROVAL SYSTEM =====")

    customer_id = input("Customer ID: ")

    age = int(input("Age: "))

    salary = float(
        input("Monthly Salary: ")
    )

    existing_loan = float(
        input("Existing Loan Amount: ")
    )

    credit_score = int(
        input("Credit Score: ")
    )

    employment = input(
        "Employment Type: "
    )

    requested_loan = float(
        input("Requested Loan Amount: ")
    )

    tenure = int(
        input("Loan Tenure (months): ")
    )

    dti = calculate_dti(
        salary,
        existing_loan
    )

    eligible = calculate_eligible_loan(
        salary,
        credit_score,
        existing_loan
    )

    rate = calculate_interest_rate(
        credit_score,
        employment
    )

    print("\n===== LOAN RESULT =====")

    print(
        "Customer ID:",
        customer_id
    )

    print(
        "Debt-to-Income Ratio:",
        round(dti, 2)
    )

    print(
        "Eligible Loan Amount:",
        round(eligible, 2)
    )

    print(
        "Interest Rate:",
        rate,
        "%"
    )

    if requested_loan <= eligible:

        emi = calculate_emi(
            requested_loan,
            rate,
            tenure
        )

        print(
            "EMI:",
            round(emi, 2)
        )

    approved = approve_loan(
        age,
        salary,
        existing_loan,
        credit_score,
        employment,
        requested_loan
    )

    if approved:
        print("Loan Status: APPROVED")
    else:
        print("Loan Status: REJECTED")


if __name__ == "__main__":
    main()