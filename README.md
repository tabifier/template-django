# Roller APP template
***

A template for building dockerized Django based API applications that deploy
easily to any Kubernetes environment.


# Setup
You need the following installed on your machine before you can begin using this template:

* [Docker Toolbox](https://www.docker.com/products/docker-toolbox)
* [Git](https://git-scm.com/)

### On Mac & Windows
If you developing on Mac or Windows, you'll need to:

* Create a Docker Engine host if you don't have one already.

  ```bash
  $ docker-machine create --driver virtualbox default
  ```
  **Reference**:
  * https://docs.docker.com/machine/get-started/

* Connect your shell to the new machine.
  ```bash
  eval "$(docker-machine env default)"
  ```

## Configuration
* If you want to use SSL in your local environment, you can copy the files to `cluster/nginx/certs` and uncomment the SSL lines in the **nginx** `conf` files under `cluster/nginx/sites-enabled` after you update the path to the certs.


## Running the service
If you're on Mac or Windows, you'll need to have your docker host started and your shell is connected to it (see above).

Now all that you have to do is start services with the following command:

```
$ docker-compose up
```

Now that the services are running, you can either access the service
on port `80` of the docker host or run the `./dev` command which launches a dev server on port `9000` that you can insert break points in.

```
$ ./dev
```

To get the ip address of the docker host on Mac or Windows (localhost on Linux)
```
$ docker-machine ip default
```

## License
MIT
