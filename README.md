# MusicReviewApp
Music Review Application Inspired by letterboxd

### Objective

Purpose of this project is to create an application that allows users to create an account and review albums and songs by artists. The application will allow users to create lists of their favorite albums and follow other users, simular to letterboxd. The application will server as a prototype - collecting albums off spotify's api rather than using a pre-existing database.

### Technolgoies Used 

- API Handling (Spotify API)
- Database management
- Frameworks
- Python
- Docker

### Database setup

```
docker run --name=MusicApp --env="MYSQL_ROOT_PASSWORD=root_password" -p 3306:3306 -d mysql:latest
docker exec -it MusicApp mysql -h localhost -P 3306 --protocol=tcp -u root -proot_password
```

### Acknowledgments

The project was inspired by [letterboxd]([https://github.com/oluwatosin17](https://letterboxd.com/)). The project uses spotify's API to collect public data.
