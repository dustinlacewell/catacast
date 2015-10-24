# catacast

A script for ttycast streaming an ASCII game of Cataclysm: DDA to a Docker host

## Dependencies:

You'll need to install ttyrec to your local machine. You can get the source here:

   https://github.com/mjording/ttyrec

Just run `make` and put both `ttyrec` and `ttyplay` on your `PATH`.


## Installation:

Just download the `catacast` script and put it somewhere on your `PATH`. You can then start streaming to the public server:

    catacast /path/to/cataclysm

This will attempt to stream to the default port `9000`. If someone is already using it, you can specify a custom port:

    PORT=9001 catacast /path/to/cataclysm


## Using your own server

There are four steps to setting up your own server for use with catacast:

  * Install the custom login-shell `ttycast-sh`
  * Install Docker
  * Add the `cdda` login user and set its shell to `ttycast-sh`
  * Add your public key to the `cdda` authorized_keys file


### Installing `ttycast-sh`

To install the ttycast shell, simply copy the script to your server and make it executable. Perhaps, `/usr/local/bin/ttycast-sh`

### Installing Docker

If you're not overly paranoid and understand how https works you can install using the following:

    curl https://get.docker.com/ | sh

You should be able to view Docker daemon info:

    docker info

Go ahead and pull down the ttycast image:

    docker pull dlacewell/ttycast

If you can't bring yourself to install this way, the Docker documentation lists other ways for many operating systems such as Ubuntu:

    https://docs.docker.com/installation/ubuntulinux/

### Adding the `cdda` user

Simply run the following to add the user:

    useradd -m -G docker -s /usr/local/bin/ttycast-sh

### Adding your public key

Simply add your public key to /home/cdda/.ssh/authorized_keys


### Streaming to your server

You should now be able to stream to your server without encountering a password prompt you can't respond to:


    PORT=9002 HOST=$YOURSERVERIP catacast /path/to/cataclysm