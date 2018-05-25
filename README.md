# UCF-Announcements
Django application for managing and displaying UCF-Announcements.

## Installation and Setup

1. Install virtual environment: `pip install virtualenv`
2. Create virtual environment for your project: `virtualenv projectfolder` and move to the directory `cd projectfolder/`
3. Clone repository into src directory: `git clone git@github.com:UCF/unify-events.git src` and move to the directory `cd src/`
4. Activate virtual environment: `source ../bin/activate`
5. Install requirements: `pip install -r requirements.txt`
6. Install the required npm packages: `npm install`
7. Make sure the default artifacts are created: `gulp default`
8. Run the deployment steps: `python manage.py deploy`. This command is the equivelent of running the following individual commands:
    a. `python manage.py migrate`
    b. `python manage.py loaddata audience`
    c. `python manage.py collectstatic -l`
9. Run the local server to debug and test: `python manage.py runserver`

## Changelog

### v1.0.3
Bug Fixes:
* Updated default main site header/footer URLs
* Suppressed exception when `data['items']` is not set when fetching/assigning menu data
* Fixed incorrect item values for menu link URLs; header/footer links should now link to their correct locations
* Added explicit mimetype declaration to robots.txt view to prevent it from being served as text/html

### v1.0.2
Bug Fixes:
* Updated keywords field to not be required.

### v1.0.1
Bug Fixes:
* Fixes [#10](https://github.com/UCF/UCF-Announcements-Django/issues/10) by implementing Main-Site-Theme v3.0.0 styles for navigation.
* Fixes [#11](https://github.com/UCF/UCF-Announcements-Django/issues/11) by updating col widths at various breakpoints and adding the `h-100` class to the columns.

Enhancements:
* Readded datetime pickers fixing [#12](https://github.com/UCF/UCF-Announcements-Django/issues/12)
* Added a slug and permalink field to the Announcements api
* Added basic filtering to the announcements endpoint.
* Added favicon
* Added support for a sitemap
* Added robots.txt
* Added snippets necessary for adding Google Tag Manager
* Updated automatic titles and meta descriptions
* Added delete view
* Added delete buttons to manager list

### v1.0.0
* Initial Release

