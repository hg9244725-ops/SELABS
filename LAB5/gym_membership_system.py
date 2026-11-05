
"""Fitness gym membership registration and renewal module."""

import hashlib
import os
import secrets


members = {
    "M01": {
        "name": "Alex",
        "plan": "Gold",
        "months_left": 6,
        "fee": 600.0,
    },
    "M02": {
        "name": "Brooke",
        "plan": "Silver",
        "months_left": 1,
        "fee": 350.0,
    },
    "M03": {
        "name": "Chris",
        "plan": "Platinum",
        "months_left": 12,
        "fee": 1000.0,
    },
}


def register_member(member_id, name, plan, months, member_log=None):
    """Register a new gym member."""
    if member_log is None:
        member_log = []

    if member_id in members or months <= 0:
        return False

    members[member_id] = {
        "name": name,
        "plan": plan,
        "months_left": months,
        "fee": 50.0 * months,
    }
    member_log.append(f"Registered {member_id} for {months} months")
    return True


def cancel_membership(member_id):
    """Cancel an existing gym membership."""
    try:
        del members[member_id]
        return True
    except KeyError:
        return False


def check_membership_status(member_id):
    """Check whether a member has an active membership."""
    if members.get(member_id) is None:
        return False

    return members[member_id]["months_left"] > 0


def calculate_renewal_rate(member_id, discount_rate):
    """Calculate the renewal fee after applying a discount."""
    if member_id not in members:
        raise ValueError("Member ID does not exist.")

    if not 0 <= discount_rate <= 1:
        raise ValueError("Discount rate must be between 0 and 1.")

    base_fee = members[member_id]["fee"]
    final_rate = base_fee * (1 - discount_rate)
    return final_rate


def generate_member_hash(member_id):
    """Generate a SHA-256 hash for a member ID."""
    return hashlib.sha256(member_id.encode("utf-8")).hexdigest()


def generate_locker_pin():
    """Generate a secure four-digit locker PIN."""
    return secrets.randbelow(9000) + 1000


def export_member_roster(filename="gym_roster.txt"):
    """Export the gym member roster to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(members))

    print(f"Roster exported to: {filename}")


def get_active_summary(member_records):
    """Return the number of members with active memberships."""
    count = 0

    for details in member_records.values():
        if details["months_left"] > 0:
            count += 1

    return count


def main():
    """Run the gym membership management demonstration."""
    gym_api_secret = os.getenv("GYM_CLOUD_PORTAL_SECRET")

    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")

    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", 0.15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())

    export_member_roster()
    print("Active count:", get_active_summary(members))
    print("Portal secret configured:", bool(gym_api_secret))


if __name__ == "__main__":
    main()
