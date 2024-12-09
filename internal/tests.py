import requests
import json

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "accept": "application/json",
}


def make_post_request(data: str) -> requests.Response:
    r = requests.post(
        "http://127.0.0.1:8000/get_form",
        data=data,
        headers=headers,
        timeout=2,
    )
    return r


r = make_post_request(data="req_str=user1_email%3Duser1%40gmail.com")
assert r.json() == "User form 1"


r = make_post_request(
    data="req_str=user3_email%3Duser3%40gmail.com%26user3_date_of_birth%3D2024-05-02",
)
assert r.json() == "User form 3"

r = make_post_request(
    data="req_str=user_phone_number%3D%2B7%20924%2055542%20303",
)
assert r.status_code == 422

r = make_post_request(
    data="user_phone_number=+8 924 555 42 30",
)
assert r.status_code == 422

r = make_post_request(
    data="req_str=user_email%3Duser%40gmailcom%26user_phone_number%3D%2B7%20924%20555%2042%203",
)
assert r.status_code == 422


r = make_post_request(
    data="req_str=user_email%3Dusermail.com%26user_phone_number%3D%2B7%20924%20555%2042%203",
)
assert r.status_code == 422

# #######################################################

r = make_post_request(
    data="req_str=user1_email%3Daa%40gmail.com",
)
assert json.loads(r.content) == "User form 1"

r = make_post_request(
    data="req_str=user2_date_of_birth%3D2021-05-21",
)
assert json.loads(r.content) == "User form 2"


r = make_post_request(
    data="req_str=user2_date_of_birth%3D21.05.2021",
)
assert json.loads(r.content) == "User form 2"


r = make_post_request(
    data="req_str=user2_date_of_birth%3D2105.2021",
)
assert r.status_code == 422

r = make_post_request(
    data="req_str=user2_date_of_birth%3D2021-0521",
)
assert r.status_code == 422

r = make_post_request(
    data="req_str=user2_date_of_birth%3D05-2021-21",
)
assert r.status_code == 422

r = make_post_request(
    data="req_str=random_name%3Dsome_name%26random_phone_number%3D%2B7%20924%20052%2034%2002%26random_email%3Drandom%40gmail.com",
)
assert json.loads(r.content) == {
    "random_email": "email",
    "random_phone_number": "phone",
    "random_name": "text",
}

r = make_post_request(
    data="req_str=random_name%3Dsome_name%26random_phone_number%3D%2B7%20924%20052%2034%2002%26random_email%3Drandom%40gmail.com",
)
assert json.loads(r.content) == {
    "random_email": "email",
    "random_phone_number": "phone",
    "random_name": "text",
}

r = make_post_request(
    data="req_str=random_email%3Drandom%40gmail.com%26random_phone_number%3D%2B7%20926%2044%2005%2077",
)
assert r.status_code == 422
