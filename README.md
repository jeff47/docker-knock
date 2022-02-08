# docker-knock
Dockerized version of knock, for downloading and converting Adobe Digital Editions ACSM to EPUB or PDF

https://hub.docker.com/repository/docker/jeffrice/docker-knock


##  Knock
[Knock](https://github.com/BentonEdmondson/knock) is a useful tool for downloading and converting eBooks from Adobe Editions.  Adobe Editions itself is not needed.  This is a dockerized version of knock, so you don't need to enable user namespaces which some may consider a security risk.

## Installation
1.  You will need an acsm file (Adobe Digital Editions) file.
1.  Change to the directory containing the acsm file.
1.  **First run:** You will need to run the container as interactive to enter your ADE credentials.

```docker run -it -v $(pwd):/home/knock -v ~/.config/knock:/root/.config/knock --rm jeffrice/docker-knock File.acsm```

1.  After the first run (and your credentials are saved), you can leave off the ```-it``` part.

