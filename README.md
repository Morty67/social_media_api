# Social media API
The application was created on DRF and this API  allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.


## Installing / Getting started:
```shell
Python 3 must be installed
To get started, you need to clone the repository from GitHub: https://github.com/Morty67/social_media_api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Features:

*  JWT authenticated
*  Admin panel - admin/
*  Documentation is located at api/doc/swagger/
*  User profile creation and updating with profile picture, bio, and other details
*  User profile retrieval and searching for users by username or other criteria
*  Follow/unfollow functionality with the ability to view lists of followed and following users
*  Post creation with text content and optional media attachment
* 