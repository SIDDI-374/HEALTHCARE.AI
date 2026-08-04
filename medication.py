from database import add_medication, get_medications

# ---------------- ADD MEDICATION ---------------- #

def add_new_medication(name, time):
    """
    Add a new medication to the database.
    """

    if name.strip() == "":
        return False

    add_medication(name.strip(), time)

    return True


# ---------------- LIST MEDICATIONS ---------------- #

def list_medications():
    """
    Return all medications.
    """

    meds = get_medications()

    return meds


# ---------------- DRUG INTERACTIONS ---------------- #

interaction_pairs = {

    ("Aspirin", "Ibuprofen"):
        "⚠ Taking Aspirin with Ibuprofen may increase the risk of stomach bleeding.",

    ("Paracetamol", "Alcohol"):
        "⚠ Alcohol may increase the risk of liver damage when combined with Paracetamol.",

    ("Warfarin", "Aspirin"):
        "⚠ Increased risk of serious bleeding.",

    ("Metformin", "Alcohol"):
        "⚠ May increase the risk of lactic acidosis.",

    ("Amoxicillin", "Methotrexate"):
        "⚠ Amoxicillin may increase Methotrexate toxicity.",

    ("Atorvastatin", "Grapefruit"):
        "⚠ Grapefruit may increase the side effects of Atorvastatin."

}


def check_interaction(med1, med2):

    med1 = med1.strip().title()
    med2 = med2.strip().title()

    if (med1, med2) in interaction_pairs:
        return interaction_pairs[(med1, med2)]

    elif (med2, med1) in interaction_pairs:
        return interaction_pairs[(med2, med1)]

    else:
        return "✅ No major interaction found in the local database. Please consult your doctor or pharmacist before combining medications."


# ---------------- REMINDER MESSAGE ---------------- #

def medication_reminder(name, time):

    return f"💊 Reminder: Take {name} at {time}."


# ---------------- MEDICINE SUMMARY ---------------- #

def medicine_summary(name):

    return f"""
Medicine: {name}

✔ Follow the prescribed dosage.

✔ Take the medicine at the recommended time.

✔ Do not stop the medication without consulting your doctor.

✔ Store medicines in a cool, dry place.

✔ Keep medicines out of the reach of children.
"""
