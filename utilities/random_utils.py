from faker import Faker
import random
from datetime import datetime

# Initialize Faker
faker = Faker()

class RandomUtils:

    @staticmethod
    def get_first_name():
        return faker.first_name()

    @staticmethod
    def get_last_name():
        return faker.last_name()

    @staticmethod
    def get_user_name():
        first_name = faker.first_name()
        max_digits = max(0, 11 - len(first_name))
        numeric_part = ''.join(random.choices('0123456789', k=max_digits))
        return first_name + numeric_part

    @staticmethod
    def get_email():
        fname = faker.first_name()
        lname = faker.last_name()
        email_domains = ["@yopmail.com"]
        selected_domain = random.choice(email_domains)
        email = f"{fname}{lname}{random.randint(0, 99999)}{selected_domain}"
        return email

    @staticmethod
    def get_street():
        return faker.street_address()

    @staticmethod
    def get_city():
        return faker.city()

    @staticmethod
    def get_number():
        return faker.numerify("###")

    @staticmethod
    def get_random_string():
        return faker.bothify("?" * 20, letters=True, numbers=True)

    @staticmethod
    def get_commission_rule_name():
        return f"CommissionRule{random.randint(100, 999)}"

    @staticmethod
    def get_mobile_number():
        return faker.numerify("##########")

    @staticmethod
    def get_current_date_termination():
        return datetime.now().strftime("%Y-%m-%d")
