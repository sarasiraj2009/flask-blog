import unittest

from flask import abort, url_for
from flask_testing import TestCase

from application import app, db
from application.models import Users, Posts
class TestBase(TestCase):

    def create_app(self):
        config_name = 'testing'
        app.config.update(SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@34.89.26.140/flask_test')
        return app

    def setUp(self):
        """
        Will be called before every test
        """
        # ensure there is no data in the test database when the test starts
        db.session.commit()
        db.drop_all()
        db.create_all()

        # create test admin user
        admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password="admin2016")

        # create test non-admin user
        employee = Users(first_name="test", last_name="user", email="test@user.com", password="test2016")

        # save users to database
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        """
        Will be called after every test
        """

        db.session.remove()
        db.drop_all()

class TestViews(TestBase):

    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
    
    def test_postpage_view(self):

        target_url = url_for('post')
        redirect_url = url_for('login', next=target_url)
       
        response = self.client.get(target_url)
        self.assertRedirects(response, redirect_url)
        self.assertEqual(response.status_code, 302)

class TestRegistration(TestBase):

    def test_registration(self):
        """
        Test that a user can create an account using the registration form
        if all fields are filled out correctly, and that they will be 
        redirected to the login page
        """

        # Click register menu link
        self.driver.find_element_by_xpath("<xpath for Register button in nav bar>").click()
        time.sleep(1)

        # Fill in registration form
        self.driver.find_element_by_xpath('<xpath for registration email>').send_keys(test_admin_email)
        self.driver.find_element_by_xpath('<xpath for registration first name>').send_keys(
            test_admin_first_name)
        self.driver.find_element_by_xpath('<xpath for registration last name>').send_keys(
            test_admin_last_name)
        self.driver.find_element_by_xpath('<xpath for registration password>').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('<xpath for registration check password>').send_keys(
            test_admin_password)
        self.driver.find_element_by_xpath('<xpath for register button>').click()
        time.sleep(1)

        # Assert that browser redirects to login page
        assert url_for('login') in self.driver.current_url

    if __name__ == '__main__':
        unittest.main(port=5000)