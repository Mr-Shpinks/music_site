### Description
This is a Django web application - experimental attempt to create [AllMusic](https://www.allmusic.com/) or [Discogs](https://www.discogs.com/) simple analogy. User can browse releases, artists, labels, charts etc.

#### Project structure:
* music_site is the main Django application that runs the project alltogether 
* music_database is the application responsible for most communications with the database
* accounts app is responsibe for user management, but it mostly Django defaults
* templates are HTML files for Django views to render

All other folders not directly related to web-application work.

Web application uses PostgreSQL database. **Most data is autogenerateed randomly** with Python [script](generator/generator.py) in order to load the database. 
Pagination added where needed to make pages load faster. SQL-injection protection is built in in Django.


### Database
#### music_database application database:
![music_database application database](/screenshots/music_database_tables.png)

#### all web-application database:
![all web-application database](/screenshots/all_database_tables.png)

### Screenshots
#### Main page:
![Main page](/screenshots/main_page.png)

#### Release details page:
![Release details page](/screenshots/details.png)

#### All database search:
![All database search](/screenshots/general_search.png)
