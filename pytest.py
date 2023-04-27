============================= test session starts ==============================
platform linux -- Python 3.10.6, pytest-6.2.4, py-1.11.0, pluggy-0.13.1 -- /home/antares/Dev/api_yamdb/venv/bin/python3
django: settings: api_yamdb.settings (from ini)
rootdir: /home/antares/Dev/api_yamdb, configfile: pytest.ini, testpaths: tests/
plugins: django-4.4.0, pythonpath-0.7.3
collecting ... collected 77 items

tests/test_00_user_registration.py::Test00UserRegistration::test_00_nodata_signup PASSED [  1%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_invalid_data_signup PASSED [  2%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_singup_length_and_simbols_validation[data0-messege0] PASSED [  3%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_singup_length_and_simbols_validation[data1-messege1] PASSED [  5%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_singup_length_and_simbols_validation[data2-messege2] PASSED [  6%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_valid_data_user_signup PASSED [  7%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_valid_data_admin_create_user PASSED [  9%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_admin_create_user_length_and_simbols_validation[data0-messege0] PASSED [ 10%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_admin_create_user_length_and_simbols_validation[data1-messege1] PASSED [ 11%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_admin_create_user_length_and_simbols_validation[data2-messege2] PASSED [ 12%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_admin_create_user_length_and_simbols_validation[data3-messege3] PASSED [ 14%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_admin_create_user_length_and_simbols_validation[data4-messege4] PASSED [ 15%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_obtain_jwt_token_invalid_data PASSED [ 16%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_registration_me_username_restricted PASSED [ 18%]
tests/test_00_user_registration.py::Test00UserRegistration::test_00_registration_same_email_restricted PASSED [ 19%]
tests/test_00_user_registration.py::Test00UserRegistration::test_get_new_confirmation_code_for_existing_user PASSED [ 20%]
tests/test_00_user_registration.py::Test00UserRegistration::test_get_confirmation_code_for_user_created_by_admin PASSED [ 22%]
tests/test_01_users.py::Test01UserAPI::test_01_users_not_authenticated PASSED [ 23%]
tests/test_01_users.py::Test01UserAPI::test_02_users_username_not_authenticated PASSED [ 24%]
tests/test_01_users.py::Test01UserAPI::test_03_users_me_not_authenticated PASSED [ 25%]
tests/test_01_users.py::Test01UserAPI::test_04_users_get_admin PASSED    [ 27%]
tests/test_01_users.py::Test01UserAPI::test_04_02_users_get_search PASSED [ 28%]
tests/test_01_users.py::Test01UserAPI::test_04_01_users_get_admin_only PASSED [ 29%]
tests/test_01_users.py::Test01UserAPI::test_05_01_users_post_admin_bad_requests PASSED [ 31%]
tests/test_01_users.py::Test01UserAPI::test_05_02_users_post_admin_user_creation[data0-] PASSED [ 32%]
tests/test_01_users.py::Test01UserAPI::test_05_02_users_post_admin_user_creation[data1-без указания роли нового пользователя ] PASSED [ 33%]
tests/test_01_users.py::Test01UserAPI::test_05_03_users_post_response_has_data PASSED [ 35%]
tests/test_01_users.py::Test01UserAPI::test_05_04_users_post_user_superuser PASSED [ 36%]
tests/test_01_users.py::Test01UserAPI::test_06_users_username_get_admin PASSED [ 37%]
tests/test_01_users.py::Test01UserAPI::test_06_users_username_get_not_admin PASSED [ 38%]
tests/test_01_users.py::Test01UserAPI::test_07_01_users_username_patch_admin PASSED [ 40%]
tests/test_01_users.py::Test01UserAPI::test_07_02_users_username_patch_moderator PASSED [ 41%]
tests/test_01_users.py::Test01UserAPI::test_07_03_users_username_patch_user PASSED [ 42%]
tests/test_01_users.py::Test01UserAPI::test_07_05_users_username_put_not_allowed PASSED [ 44%]
tests/test_01_users.py::Test01UserAPI::test_08_01_users_username_delete_admin PASSED [ 45%]
tests/test_01_users.py::Test01UserAPI::test_08_02_users_username_delete_moderator PASSED [ 46%]
tests/test_01_users.py::Test01UserAPI::test_08_03_users_username_delete_user PASSED [ 48%]
tests/test_01_users.py::Test01UserAPI::test_08_04_users_username_delete_superuser PASSED [ 49%]
tests/test_01_users.py::Test01UserAPI::test_09_users_me_get PASSED       [ 50%]
tests/test_01_users.py::Test01UserAPI::test_09_02_users_me_delete_not_allowed PASSED [ 51%]
tests/test_01_users.py::Test01UserAPI::test_10_01_users_me_patch PASSED  [ 53%]
tests/test_01_users.py::Test01UserAPI::test_10_02_users_me_has_field_validation[data0-messege0] PASSED [ 54%]
tests/test_01_users.py::Test01UserAPI::test_10_02_users_me_has_field_validation[data1-messege1] PASSED [ 55%]
tests/test_01_users.py::Test01UserAPI::test_10_02_users_me_has_field_validation[data2-messege2] PASSED [ 57%]
tests/test_01_users.py::Test01UserAPI::test_10_02_users_me_has_field_validation[data3-messege3] PASSED [ 58%]
tests/test_01_users.py::Test01UserAPI::test_10_02_users_me_has_field_validation[data4-messege4] PASSED [ 59%]
tests/test_01_users.py::Test01UserAPI::test_10_03_users_me_patch_change_role_not_allowed PASSED [ 61%]
tests/test_02_category.py::Test02CategoryAPI::test_01_category_not_auth PASSED [ 62%]
tests/test_02_category.py::Test02CategoryAPI::test_02_category_with_admin_user PASSED [ 63%]
tests/test_02_category.py::Test02CategoryAPI::test_03_category_fields_validation[data0-massage0] PASSED [ 64%]
tests/test_02_category.py::Test02CategoryAPI::test_03_category_fields_validation[data1-massage1] PASSED [ 66%]
tests/test_02_category.py::Test02CategoryAPI::test_03_category_fields_validation[data2-massage2] PASSED [ 67%]
tests/test_02_category.py::Test02CategoryAPI::test_04_category_delete_admin PASSED [ 68%]
tests/test_02_category.py::Test02CategoryAPI::test_05_category_check_permission_admin PASSED [ 70%]
tests/test_03_genre.py::Test03GenreAPI::test_01_genre_not_auth PASSED    [ 71%]
tests/test_03_genre.py::Test03GenreAPI::test_02_genre PASSED             [ 72%]
tests/test_03_genre.py::Test03GenreAPI::test_03_category_fields_validation[data0-massage0] PASSED [ 74%]
tests/test_03_genre.py::Test03GenreAPI::test_03_category_fields_validation[data1-massage1] 

=============================== warnings summary ===============================
venv/lib/python3.10/site-packages/django/utils/version.py:6
  /home/antares/Dev/api_yamdb/venv/lib/python3.10/site-packages/django/utils/version.py:6: DeprecationWarning: The distutils package is deprecated and slated for removal in Python 3.12. Use setuptools or check PEP 632 for potential alternatives
    from distutils.version import LooseVersion

tests/test_00_user_registration.py: 3837 warnings
tests/test_01_users.py: 5420 warnings
tests/test_02_category.py: 1303 warnings
tests/test_03_genre.py: 545 warnings
venv/lib/python3.10/site-packages/django/utils/asyncio.py:19: 170 warnings
  /home/antares/Dev/api_yamdb/venv/lib/python3.10/site-packages/django/utils/asyncio.py:19: DeprecationWarning: There is no current event loop
    event_loop = asyncio.get_event_loop()

-- Docs: https://docs.pytest.org/en/stable/warnings.html
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! KeyboardInterrupt !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
/home/antares/Dev/api_yamdb/venv/lib/python3.10/site-packages/django/utils/crypto.py:87: KeyboardInterrupt
(to show a full traceback on KeyboardInterrupt use --full-trace)
===================== 57 passed, 11276 warnings in 21.11s ======================
