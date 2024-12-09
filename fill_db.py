def fill_db(con):
    con.insert({"name": "User form 1", "user1_email": "email"})
    con.insert(
        {
            "name": "User form 2",
            "user2_name": "text",
            "user2_email": "email",
            "user2_date_of_birth": "date",
        }
    )
    con.insert(
        {
            "name": "User form 3",
            "user3_name": "text",
            "user3_email": "email",
            "user3_date_of_birth": "date",
            "user_3_phone_ number": "phone",
        }
    )
