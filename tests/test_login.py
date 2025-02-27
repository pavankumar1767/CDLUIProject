import pytest
from pages.login_page import LoginPage
from utilities.config import Config


@pytest.mark.usefixtures("setup")
class TestLogin:
    def test_valid_login(self, setup):
        page = setup
        login_page = LoginPage(page)


        login_page.navigate(Config.BASE_URL)
        login_page.enter_username("admin@yourstore.com")
        login_page.enter_password("admin")
        login_page.click_login()
        assert login_page.get_text("#welcomeMessage") == "Welcome, testuser!"


    # def test_invalid_login(self, setup):
    #     page = setup
    #     login_page = LoginPage(page)
    #
    #
    #     login_page.navigate("https://example.com/login")
    #     login_page.enter_username("wronguser")
    #     login_page.enter_password("wrongpass")
    #     login_page.click_login()
    #     assert login_page.get_text("#errorMessage") == "Invalid credentials"