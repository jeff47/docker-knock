# docker-knock
Dockerized version of knock, for downloading and converting Adobe Digital Editions ACSM to EPUB or PDF

https://hub.docker.com/repository/docker/jeffrice/docker-knock


##  Knock
[Knock](https://github.com/BentonEdmondson/knock) is a useful tool for downloading and converting eBooks from Adobe Editions.  Adobe Editions itself is not needed.  This is a dockerized version of knock, so you don't need to enable user namespaces which some may consider a security risk.

## Installation
1.)  You will need an acsm file (Adobe Digital Editions) file.  
2.)  You will need to run the container as interactive to enter your ADE credentials.

```docker run -it -v $(pwd):/home/knock --rm jeffrice/docker-knock File.acsm```

## To-Do

I am working on a better way for authentication, so that your credentials will be saved.  Personally, I do this myself by copying the xml files into the container at build time.  Naturally, that can't be distributed so I'm working on a self-contained alternative.
This is accomplished by placing my auth files in a subdirectory (acsm/) of my build directory, and adding this line to the Dockerfile:

```COPY acsm/ /root/.config/knock/acsm```
