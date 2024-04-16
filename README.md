# UCF-Announcements
Django application for managing and displaying UCF-Announcements.


## Container Instructions

1. Install prerequisite packages:

Podman/Docker is necessary. For installation instructions please refer to their relevant documentation.

2. Ensure the podman machine is initialized

Use the command:

`podman machine init`

3. Ensure the podman machine has started

Use the command:

`podman machine start`

4. Edit the .env.templ file to uncomment the ALLOWED_HOSTS and STATIC_ROOT options 

5. Build the container image

`podman build -t announcements .`

6. Run the container

`podman run -ti -p 8000:8000 announcements`

7. Make changes to the repository and repeat steps 5-7 as necessary


## Installation on machine without a container

### Prerequisites

The `python-ldap` module requires a number of prerequisites to be installed before it can be installed via `pip` in step 5 below.

### Mac OSX

1. [Xcode needs to be installed](https://developer.apple.com/xcode/).
2. The xcode command line tools need to be installed: `xcode-select --install`.
3. Openldap can be installed via homebrew: `brew install openldap`.
4. If running OSX 10.14.0 (Mojave) or above, the following arguments may need to be added to the `pip` command:

```
pip install -r requirements.txt \
--global-option=build_ext \
--global-option="-I$(xcrun --show-sdk-path)/usr/include/sasl"
```

### Debian (Ubuntu)

1. Install prerequisite packages:

```
apt-get install build-essential python3-dev python2.7-dev \
    libldap2-dev libsasl2-dev slapd ldap-utils python-tox \
    lcov valgrind
```
2. Run pip install normally after following steps 1-4 below: `pip install -r requirements.txt`.

### Centos

1. Install prerequisites via `yum`:

```
yum groupinstall "Development tools"
yum install openldap-devel python-devel
```
2. Run pip install normally after following steps 1-4 below: `pip install -r requirements.txt`.

## Local Installation and Setup

1. Install virtual environment: `pip install virtualenv`
2. Create virtual environment for your project: `virtualenv projectfolder` and move to the directory `cd projectfolder/`
3. Clone repository into src directory: `git clone git@github.com:UCF/unify-events.git src` and move to the directory `cd src/`
4. Activate virtual environment: `source ../bin/activate`
5. Copy the `.env.templ` file to `.env` and uncomment and update all configuration items necessary.
6. Install requirements: `pip install -r requirements.txt`
7. Install the required npm packages: `npm install`
8. Make sure the default artifacts are created: `gulp default`
9. Run the deployment steps: `python manage.py deploy`. This command is the equivelent of running the following individual commands:
    a. `python manage.py migrate`
    b. `python manage.py loaddata audience`
    c. `python manage.py collectstatic -l`
10. Run the local server to debug and test: `python manage.py runserver`

## Changelog

### 1.0.14
Enhancements:
* Added expiration period to old announcements. Any past the expiration will be redirected to the home page.
### 1.0.13
Accessibility:
* Added skip to content link at the top of the base template.
### v1.0.12
* Updated default character set and collation for database tables.
### v1.0.11
* Ensure taggit tags (used for announcement keywords) as case sensitive but are pulled via the typeahead control case insensitively.
### v1.0.10
Bug Fixes:
* Fixed a bug where remote menus were not loading properly.

### v1.0.9
Bug Fixes:
* Made changes to the local settings template related to logging.

### v1.0.8
Bug Fixes:
* Corrected problem with date fields in the admin area.

### v1.0.7
Bug Fixes:
* Corrected malformed subquery when excluding ongoing announcements. Fixes #33

### v1.0.6
Enhancements:
* Added ability to filter by field or fieldset on the Announcement serializer. This allows for specific fields, or a predefined set of fields. Currently there is only the `options` fieldset defined for announcements.

### v1.0.5
Enhancements:
* Added detail view for announcements
* Updated Django
* Updated documentation with more detailed installation instructions

Bug Fixes:
* Updated home template to fix audience links bug
* Removed hard coded URL in the javascript for the announcements create/edit form.

### v1.0.4
Bug Fixes:
* Fixed issue with announcement descriptions in cards being truncated without accounting for inner HTML

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

