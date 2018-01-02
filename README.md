# deeplearn-gl

[![Travis CI](https://travis-ci.org/stackgl/headless-gl.svg?branch=master)](https://travis-ci.org/stackgl/headless-gl)
[![Appveyor](https://ci.appveyor.com/api/projects/status/github/stackgl/headless-gl?svg=true)](https://ci.appveyor.com/project/mikolalysenko/headless-gl)
[![js-standard-style](https://img.shields.io/badge/code%20style-standard-brightgreen.svg)](http://standardjs.com/)

`deeplearn-gl` lets you create a WebGL context in [node.js](https://nodejs.org/en/) without making a window or loading a full browser environment.

This fork provides enough capability to run deeplearn.js using the GPU (with GPU processing asynchronous to the node execution).

## Example

```javascript
var gl = require('deeplearn-gl')
var dl = require('deeplearn');
var math = new dl.NDArrayMath('webgl');
var size = 3000;

var start = Date.now();

var a = dl.Array2D.ones([size, size]);
var b = dl.Array2D.ones([size, size]);

var result = math.matMul(a, b);

var promise = result.data().then(function(data) {
  console.log("done in ", (Date.now()-start)/1000, "seconds with value", data[0]);
}).catch(console.log);
```

## Warning!

This is forked from a module that is not actively developed.

## Install
Installing `deeplearn-gl` currently has only been tested on OSX.  You can install it using [npm](https://www.npmjs.com/) run the command,

```
npm install deeplearn-gl
```

And you are good to go!  If your system is not supported, then please see the [development](#system-dependencies) section on how to configure your build environment.  Patches to improve support are always welcome!

## API

`deeplearn-gl` exposes a global `document.createElement` which supports creating canvas elements
for drawing (using node-canvas) or for GL (using headless-gl and the angleproject)

### Extensions

In addition to all the usual WebGL methods, `headless-gl` exposes some extensions that allow deeplearn-js to function more efficiently.

## System dependencies

On OSX installing `deeplearn-gl` from npm should just work.  However, if you run into problems you might need to adjust your system configuration and make sure all your dependencies are up to date.  For general information on building native modules, see the [`node-gyp`](https://github.com/nodejs/node-gyp) documentation.

#### Mac OS X

* [Python 2.7](https://www.python.org/)
* [XCode](https://developer.apple.com/xcode/)

#### Ubuntu/Debian

* [Python 2.7](https://www.python.org/)
* A GNU C++ environment (available via the `build-essential` package on `apt`)
* [libxi-dev](http://www.x.org/wiki/)
* Working and up to date OpenGL drivers
* [GLEW](http://glew.sourceforge.net/)

```
$ sudo apt-get install -y build-essential libxi-dev libglu1-mesa-dev libglew-dev
```

#### Windows

* [Python 2.7](https://www.python.org/)
* [Microsoft Visual Studio](https://www.microsoft.com/en-us/download/details.aspx?id=5555)
* d3dcompiler_47.dll should be in c:\windows\system32, but if isn't then you can find another copy in the deps/ folder
* (optional) A modern nodejs supporting es6 to run some examples https://iojs.org/en/es6.html

## FAQ

### How can I use headless-gl with a continuous integration service?

`headless-gl` should work out of the box on most CI systems.  Some notes on specific CI systems:

* [CircleCI](https://circleci.com/): `headless-gl` should just work in the default node environment.
* [AppVeyor](http://www.appveyor.com/): Again it should just work
* [TravisCI](https://travis-ci.org/): Works out of the box on the OS X image.  For Linux VMs, you need to install mesa and xvfb.  To do this, create a file in the root of your repo called `.travis.yml` and paste the following into it:

```
language: node_js
os: linux
sudo: required
dist: trusty
addons:
  apt:
    packages:
    - mesa-utils
    - xvfb
    - libgl1-mesa-dri
    - libglapi-mesa
    - libosmesa6
node_js:
  - '6'
before_script:
  - export DISPLAY=:99.0; sh -e /etc/init.d/xvfb start
```

If you know of a service not listed here, open an issue I'll add it to the list.

### How can `headless-gl` be used on a headless Linux machine?

If you are running your own minimal Linux server, such as the one one would want to use on Amazon AWS or equivalent, it will likely not provide an X11 nor an OpenGL environment. To setup such an environment you can use those two packages:

1. [Xvfb](https://en.wikipedia.org/wiki/Xvfb) is a lightweight X11 server which provides a back buffer for displaying X11 application offscreen and reading back the pixels which were drawn offscreen. It is typically used in Continuous Integration systems. It can be installed on CentOS with `yum install -y Xvfb`, and comes preinstalled on Ubuntu.
2. [Mesa](http://www.mesa3d.org/intro.html) is the reference open source software implementation of OpenGL. It can be installed on CentOS with `yum install -y mesa-dri-drivers`, or `apt-get install libgl1-mesa-dev`. Since a cloud Linux instance will typically run on a machine that does not have a GPU, a software implementation of OpenGL will be required.

Interacting with `Xvfb` requires you to start it on the background and to execute your `node` program with the DISPLAY environment variable set to whatever was configured when running Xvfb (the default being :99). If you want to do that reliably you'll have to start Xvfb from an init.d script at boot time, which is extra configuration burden. Fortunately there is a wrapper script shipped with Xvfb known as `xvfb-run` which can start Xvfb on the fly, execute your node program and finally shut Xvfb down. Here's how to run it:

    xvfb-run -s "-ac -screen 0 1280x1024x24" <node program>

### Does headless-gl work in a browser?

Yes, with [browserify](http://browserify.org/).  The `STACKGL_destroy_context` and `STACKGL_resize_drawingbuffer` extensions are emulated as well.

### How are `<image>` and `<video>` elements implemented?

They aren't for now.  If you want to upload data to a texture, you will need to unpack the pixels into a `Uint8Array` and feed it into `texImage2D`.  To help reading and saving images, you should check out the following modules:

* [`get-pixels`](https://www.npmjs.com/package/get-pixels)
* [`save-pixels`](https://www.npmjs.com/package/save-pixels)

### What extensions are supported?

Only the following for now:

* [`STACKGL_resize_drawingbuffer`](https://github.com/stackgl/headless-gl#stackgl_resize_drawingbuffer)
* [`STACKGL_destroy_context`](https://github.com/stackgl/headless-gl#stackgl_destroy_context)
* [`ANGLE_instanced_arrays`](https://www.khronos.org/registry/webgl/extensions/ANGLE_instanced_arrays/)

### How can I keep up to date with what has changed in headless-gl?

There is a [change log](CHANGES.md).

### Why use this thing instead of `node-webgl`?

Despite the name [node-webgl](https://github.com/mikeseven/node-webgl) doesn't actually implement WebGL - rather it gives you "WebGL"-flavored bindings to whatever OpenGL driver is configured on your system.  If you are starting from an existing WebGL application or library, this means you'll have to do a bunch of work rewriting your WebGL code and shaders to deal with all the idiosyncrasies and bugs present on whatever platforms you try to run on.  The upside though is that `node-webgl` exposes a lot of non-WebGL stuff that might be useful for games like window creation, mouse and keyboard input, requestAnimationFrame emulation, and some native OpenGL features.

`headless-gl` on the other hand just implements WebGL.  It is built on top of [ANGLE](https://bugs.chromium.org/p/angleproject/issues/list) and passes the full Khronos ARB conformance suite, which means it works exactly the same on all supported systems.  This makes it a great choice for running on a server or in a command line tool.  You can use it to run tests, generate images or perform GPGPU computations using shaders.

### Why use this thing instead of [electron](http://electron.atom.io/)?

Electron is fantastic if you are writing a desktop application or if you need a full DOM implementation.  On the other hand, because it is a larger dependency electron is more difficult to set up and configure in a server-side/CI environment. `headless-gl` is more modular in the sense that it just implements WebGL and nothing else.  As a result creating a `headless-gl` context takes just a few milliseconds on most systems, while spawning a full electron instance can take upwards of 15-30 seconds. If you are using WebGL in a command line interface or need to execute WebGL in a service, `headless-gl` might be a more efficient and simpler choice.

### How should I set up a development environment for headless-gl?

After you have your [system dependencies installed](#system-dependencies), do the following:

1. Clone this repo: `git clone git@github.com:stackgl/headless-gl.git`
1. Switch to the headless gl directory: `cd headless-gl`
1. Initialize the angle submodule: `git submodule init`
1. Update the angle submodule: `git submodule update`
1. Install npm dependencies: `npm install`
1. Run node-gyp to generate build scripts: `npm run rebuild`

Once this is done, you should be good to go!  A few more things

* To run the test cases, use the command `npm test`, or execute specific by just running it using node.
* On a Unix-like platform, you can do incremental rebuilds by going into the `build/` directory and running `make`.  This is **way faster** running `npm build` each time you make a change.

## License

See LICENSES
