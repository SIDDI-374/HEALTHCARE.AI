def calculate_bmi(weight, height):

    if height == 0:
        return 0

    height_m = height / 100
    bmi = weight / (height_m ** 2)

    return round(bmi, 2)

    data = cursor.fetchall()

    conn.close()

    return data
