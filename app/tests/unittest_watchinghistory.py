import unittest

from app import app, db, WatchingHistory, User, initdb


class WatchingHistoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        # Update config
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
        # Create database and table
        db.create_all()
        # Create testing data, 1 user, 1 history
        user = User(name="Test", username="test")
        user.set_password("123")
        history = WatchingHistory(
            title="test watching history",
            season="季",
            value="2",
            episode="4",
            progress="15:03",
        )
        # Add to the database
        db.session.add_all([user, history])
        db.session.commit()

        # Create testing app, equals to a real web browser
        self.client = app.test_client()
        # Create test command interface runner
        self.runner = app.test_cli_runner()

    # After testing
    def tearDown(self):
        # Remove the session
        db.session.remove()
        # Delete the database
        db.drop_all()
        self.app_context.pop()

    # Test the app existance
    def test_app_exist(self):
        self.assertIsNotNone(app)

    # Test the app in testing mode
    def test_app_is_testing(self):
        self.assertTrue(app.config["TESTING"])

    # test 404 page
    def test_404_page(self):
        response = self.client.get("/nothing")  # pass in targeted URL
        data = response.get_data(as_text=True)
        self.assertIn("Not Found", data)
        self.assertIn(
            "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.",
            data,
        )
        self.assertEqual(response.status_code, 404)  # test the response code

    # test index page
    def test_index_page(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertIn("Watching History", data)
        self.assertIn("test watching history", data)
        self.assertEqual(response.status_code, 200)

    # login helper
    def login(self):
        self.client.post(
            "/login", data=dict(username="test", password="123"), follow_redirects=True
        )

    # 测试创建条目
    def test_create_item(self):
        self.login()
        # Testing create a watching history
        response = self.client.post(
            "/",
            data=dict(
                title="New history",
                season="季",
                value="1",
                episode="1",
                progress="13:23",
            ),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("New history", data)
        # Testing create a watching history but title is empty
        response = self.client.post(
            "/",
            data=dict(title="", season="季", value="1", episode="1", progress="13:23"),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("請填寫這個欄位", data)

    # Test Update function
    def test_update_item(self):
        self.login()
        # Test Update page
        response = self.client.get("/update/1")
        data = response.get_data(as_text=True)
        self.assertIn("Updating History", data)
        self.assertIn("test watching history", data)
        self.assertIn("季", data)
        # Test Update operation
        response = self.client.post(
            "/update/1",
            data=dict(
                title="New history updated", value="2", episode="2", progress="20:00"
            ),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("History updated", data)
        # Test Update operation, but title is empty
        response = self.client.post(
            "/update/1",
            data=dict(title="", value="2", episode="2", progress="20:00"),
            follow_redirects=True,
        )
        data = response.get_data(as_text=True)
        self.assertIn("請填寫這個欄位", data)

    # Test delete function
    def test_delete_item(self):
        self.login()
        response = self.client.post("/delete/1", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("History deleted", data)
        self.assertNotIn("test watching history", data)

    # Test login protection
    def test_login_protect(self):
        response = self.client.get("/")
        data = response.get_data(as_text=True)
        self.assertNotIn("Logout", data)
        self.assertNotIn('<form action="/" method="POST">', data)
        self.assertNotIn("新增", data)
        self.assertNotIn("Delete", data)
        self.assertNotIn("Update", data)
        self.assertIn("Please login to see the history", data)

    # Test login
    def test_login(self):
        response = self.client.post(
            "/login", data=dict(username="simon", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertIn("Login success", data)
        self.assertIn("Logout", data)
        self.assertIn("Delete", data)
        self.assertIn("Update", data)
        self.assertIn('<form action="/" method="POST">', data)
        self.assertIn("新增", data)
        # Test with wrong password
        response = self.client.post(
            "/login", data=dict(username="simon", password="456"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login success", data)
        self.assertIn("Invalid username or password", data)
        # Test with wrong username
        response = self.client.post(
            "/login", data=dict(username="wrong", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login success", data)
        self.assertIn("Invalid username or password.", data)
        # Test with empty username
        response = self.client.post(
            "/login", data=dict(username="", password="123"), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login success.", data)
        self.assertIn("請填寫這個欄位", data)
        # Test with empty password
        response = self.client.post(
            "/login", data=dict(username="simon", password=""), follow_redirects=True
        )
        data = response.get_data(as_text=True)
        self.assertNotIn("Login success.", data)
        self.assertIn("請填寫這個欄位", data)

    # Test logout
    def test_logout(self):
        self.login()
        response = self.client.get("/logout", follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn("Logout success", data)
        self.assertNotIn("Logout", data)
        self.assertNotIn("Delete", data)
        self.assertNotIn("Update", data)
        self.assertNotIn('<form action="/" method="POST">', data)

    # Test init. database
    def test_initdb_command(self):
        result = self.runner.invoke(initdb)
        self.assertIn("Initialized database.", result.output)

    # 测试生成管理员账户
    def test_admin_command(self):
        db.drop_all()
        db.create_all()
        result = self.runner.invoke(
            args=["admin", "--username", "grey", "--password", "123"]
        )
        self.assertIn("Creating user...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "grey")
        self.assertTrue(User.query.first().validate_password("123"))

    # Test update the admin account
    def test_admin_command_update(self):
        # Use args to give complete command arguments
        result = self.runner.invoke(
            args=["admin", "--username", "sarah", "--password", "456"]
        )
        self.assertIn("Updating user...", result.output)
        self.assertIn("Done.", result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, "sarah")
        self.assertTrue(User.query.first().validate_password("456"))


if __name__ == "__main__":
    unittest.main()
