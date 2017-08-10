# Version System

Version System is an application for publishing changes and files in new versions of dedicated software for external clients. It uses Python 2.7.x with Django framework.

Frameworks used in the project:
- [Django] (1.11)
- [jQuery] (1.12.4)
- [Bootstrap 3] (3.3.7)

Other Python/Django libraries used in the project:
- [django-bootstrap-pagination] (1.6.2)

Other external jQuery libraries used in the project:
- [jQuery UI] (1.12.1) (datepicker)

***

## Installation
<p>To run Version System locally, first setup and activate virtual environment for it and then:</p>
<br />

__1. Install requirements using pip:__
```shell
pip install -r requirements.txt
```
<br />

__2. Make migrations:__
```shell
python manage.py makemigrations
```

__3. Create the tables in the database by__ `migrate` __command:__
```shell
python manage.py migrate
```
<br />

__4.  Create a user who can login to the admin site:__
```shell
python manage.py createsuperuser
```
<br />

__5. To handle password reset and contact actions you need to edit e-mail configuration in__ `settings.py` (`versionSystem/versionSystem/settings.py`):
```python
EMAIL_HOST = 'smtp.example.com'
EMAIL_HOST_USER = 'example@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEFAULT_FROM_EMAIL = 'example@example.com'

EMAIL_TO = ['example@example.com']
```
<br />

__6. Run the server:__
```shell
python manage.py runserver
```
<br />

__7. Go to__ `"/admin/"` __on your local domain – e.g.,__ `http://127.0.0.1:8000/admin/` __and sign in. Then you need to:__
- Add Clients and moderator Users on behalf of Clients.
- Add Moderators group `"/admin/auth/group/add/"` with `accounts | user | is moderator` permission and Users to this group.
- Publish Versions and Changes.
<br />

__Now the Version System application is ready for use.__

<br />
<p align="center">
<img src="https://lh3.googleusercontent.com/1BZoM_ItaplUDt1wXuxdRKO4oKoOPdoHqLcJt2LbuL7A4xEXIZtGBnNjskGIz9LOj4wgp9mUah6MUzyoUC0YwpT8rjr5DuS9OMVzy1vQywGKFoxA7yk-3brgbldvmM9St2P4hJJ6mdF-9DBuuzwJL1FWdaY6TQdY-so4rvqlKLwDaDw69YOP5hyu9j8WaSRVaBPyBAh6-j03IOaSIc3_CHU3jrQ_0DOzUtfJ5QSQ6C2DJLMh1GmUsieAh0DtCJpbYmTK0pj8CmcdRKwmw9cX1CFoY4E3bshZskwDOEllwIsvHTmMDISB0_FiweQt-KoEEHeCt8lmRBIZhDZDLW1445bz5PuJfa31lMXmeEmnuE6BHfUrTKHW2aSonEBkAYT6ERfjCUASgWeJ-0WLndMSC37hLjGMxv2b77oN7eQWqt5X1w0A_yhJIV2JP3ifHfg50VZ9y4j7ONwMcqGxT1jsEB8NNu7KyKKNAv9WDoEkWiJIzzlWMZad2hGU9v6S-841at2wiLvJ_CprwyNFyZZb0W5f0OPsxzNqU1X0t_6-Ho6MoUfeLW4cTXcwU54ExfC48efMEQpLydoXfy7qK8uZeRpv6grKQMZ5q4Mny1Tm9f0HrrhZfSHWxLh_hXETkOKITpZF7MuSwJBKCUQN6kYc6Xqo-l8GvEfM8_BICwidctEi6Q=w1277-h672-no" alt="Version System - Changes">
</p>

<br />
<p align="center">
<img src="https://lh3.googleusercontent.com/tv0nc2JuO1vjcSmwDGzdjpdeFkTAaK2NXoMCzQlSE9Aw6Va11WvyS5ix5RLmRU8u1cBkL9rkGgp7exoE89iGKs9paJJxVVjY8rF41WHGukHkFBRxJFpx9J1lrrtuNxssmjwNGz0eTklvepL5-1x1VqQZYQwUO-SA9jU4PyMPqSNUDyPeI4rY6t-fd4I3bLIWhVmkAOFQCzsEkru1uyfeVLW-bAMLhAJ0N1FIAub-35j2MEmLS6oFS9hxVtLxJijhoMOW2v1rai0fxqqvkK6RYVagAu7RPbtJCbgUo7YahJcvqtgAIHbq3Vxt_7c5_WLjScgdlqVvM-kFoEv4Yvf8NuSrC_eSS3FGkVQWEu-oyqJN-rGA2NjFcH-YkvzzgeRuNR91PcPdLbZYPDhRrPqYg7gY9vza-5rsF6qHqnXI8zpdTLaluOSE6icizve-6uMETxvtH3D_ml0fBKtDogNjE_u1M6eIXfsW0zMURwOU4gwIq1qlYZYjKfpUndFAFOWKPdHWUb-fAgM-fuVmXQz-iI-7V8u3KdzobUNWodh8Al8KAzfbjTc5UCk1z3zYvIf5dhf_7fW8eQqZylqHyJ3tMpjyT6yCJeivi8oEhPDg98aiqU_fWqXhHwegcZfRrekIO_iUjf72TmXFfY7wLmKRJaZEgrUuwU5kpRBcbXZEB_Fhcg=w1277-h672-no" alt="Version System - Versions">
</p>

[Django]: <https://www.djangoproject.com/>
[jQuery]: <https://jquery.com/>
[Bootstrap 3]: <http://getbootstrap.com/>

[django-bootstrap-pagination]: <https://github.com/jmcclell/django-bootstrap-pagination>

[jQuery UI]: <https://jqueryui.com/>