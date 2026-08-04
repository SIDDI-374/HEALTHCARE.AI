def calculate_bmi(weight, height):
    """
    Calculate BMI from weight (kg) and height (cm)
    """

    if height <= 0:
        return 0

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# --------------------------------------------------


def bmi_category(bmi):
    """
    Return BMI category
    """

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal Weight"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"


# --------------------------------------------------


def daily_water_intake(weight):
    """
    Recommended daily water intake in litres.
    Formula: 35 ml per kg.
    """

    water = weight * 35 / 1000

    return round(water, 2)


# --------------------------------------------------


def calorie_estimate(weight, height, age, gender):
    """
    Estimate daily calories using Mifflin-St Jeor equation.
    """

    if gender.lower() == "male":
        calories = (10 * weight) + (6.25 * height) - (5 * age) + 5

    else:
        calories = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(calories)


# --------------------------------------------------


def health_score(bmi):
    """
    Simple health score based on BMI.
    """

    if 18.5 <= bmi <= 24.9:
        return 100

    elif 25 <= bmi <= 29.9:
        return 80

    elif 30 <= bmi <= 34.9:
        return 65

    elif bmi < 18.5:
        return 70

    else:
        return 50
