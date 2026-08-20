import order_management


passed = 0
failed = 0


def test(name, condition):

    global passed
    global failed

    if condition:
        passed += 1
        print("PASS:", name)
    else:
        failed += 1
        print("FAIL:", name)


print("===== E-COMMERCE QA TESTS =====")


# 1. Single product
test(
    "Single product",
    order_management.subtotal(1, 100) == 100
)


# 2. Multiple products
test(
    "Multiple products",
    order_management.subtotal(3, 100) == 300
)


# 3. Zero quantity
test(
    "Zero quantity",
    order_management.subtotal(0, 100) == 0
)


# 4. Negative quantity
try:

    order_management.subtotal(
        -1,
        100
    )

    test(
        "Negative quantity rejected",
        False
    )

except ValueError:

    test(
        "Negative quantity rejected",
        True
    )


# 5. Electronics discount
test(
    "Electronics discount",
    order_management.category_discount(
        "Electronics",
        1000
    ) == 100
)


# 6. Clothing discount
test(
    "Clothing discount",
    order_management.category_discount(
        "Clothing",
        1000
    ) == 150
)


# 7. Books discount
test(
    "Books discount",
    order_management.category_discount(
        "Books",
        1000
    ) == 50
)


# 8. Free shipping
test(
    "Free shipping",
    order_management.shipping(2000) == 0
)


# 9. Shipping below threshold
test(
    "Shipping below threshold",
    order_management.shipping(1999) == 100
)


# 10. SAVE10 coupon
test(
    "SAVE10 coupon",
    order_management.coupon_discount(
        "SAVE10",
        1000
    ) == 100
)


# 11. SAVE20 coupon
test(
    "SAVE20 coupon",
    order_management.coupon_discount(
        "SAVE20",
        1000
    ) == 200
)


# 12. Invalid coupon
try:

    order_management.coupon_discount(
        "BAD",
        1000
    )

    test(
        "Invalid coupon rejected",
        False
    )

except ValueError:

    test(
        "Invalid coupon rejected",
        True
    )


# 13. GST
test(
    "GST calculation",
    order_management.gst(1000) == 180
)


# 14. Final amount
test(
    "Final amount positive",
    order_management.final_amount(
        "Books",
        2,
        500,
        "SAVE10"
    ) > 0
)


print("\n==============================")

if failed > 0:

    print("QA FAILED")

    print("Passed:", passed)

    print("Failed:", failed)

    raise SystemExit(1)


print("ALL QA TESTS PASSED")

print("Total Passed:", passed)