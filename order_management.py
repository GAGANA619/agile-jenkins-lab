def subtotal(quantity, unit_price):
    if quantity < 0 or unit_price < 0:
        raise ValueError("Invalid quantity/price")

    return quantity * unit_price


def category_discount(category, amount):
    if amount < 0:
        raise ValueError("Invalid amount")

    if category.lower() == "electronics":
        return amount * 0.10

    if category.lower() == "clothing":
        return amount * 0.15

    if category.lower() == "books":
        return amount * 0.05

    return 0


def coupon_discount(coupon, amount):
    if amount < 0:
        raise ValueError("Invalid amount")

    if coupon is None or coupon.strip() == "":
        return 0

    if coupon.upper() == "SAVE20":
        return min(amount * 0.20, 2000)

    if coupon.upper() == "SAVE10":
        return min(amount * 0.10, 1000)

    raise ValueError("Invalid coupon code")


def gst(taxable):
    return taxable * 0.18


def shipping(amount):
    if amount >= 2000:
        return 0

    return 100


def final_amount(category, quantity, unit_price, coupon):

    sub = subtotal(
        quantity,
        unit_price
    )

    category_discount_amount = category_discount(
        category,
        sub
    )

    after_category = (
        sub - category_discount_amount
    )

    coupon_discount_amount = coupon_discount(
        coupon,
        after_category
    )

    after_coupon = (
        after_category - coupon_discount_amount
    )

    return (
        after_coupon
        + gst(after_coupon)
        + shipping(after_coupon)
    )


def main():

    print("===== E-COMMERCE ORDER PROCESSING =====")

    category = input("Category: ")

    quantity = int(
        input("Quantity: ")
    )

    unit_price = float(
        input("Unit Price: ")
    )

    coupon = input(
        "Coupon Code: "
    )

    amount = final_amount(
        category,
        quantity,
        unit_price,
        coupon
    )

    print("\n===== ORDER RESULT =====")

    print(
        "Final Order Amount:",
        round(amount, 2)
    )


if __name__ == "__main__":
    main()