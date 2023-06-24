# Basics

## Workflow

1. Define dockerfile: You can start the dockerfile from a base container created and
uploaded to docker hub. Then, you can add more stuff from it like copying local files
to it.
2. Build the image with `docker build`.
3. Run the container
4. Manage containers: You can see available ones with `docker ps` or stop running ones
with `docker stop`.
5. Push the image to a registry with `docker push`.

## Volumes

In case you want to change the content of the container, you would need to compile
every time. To avoid this, you can run the container specifying files that will be
transferred automatically. This can be done with flag `-v` in command `docker run`.
