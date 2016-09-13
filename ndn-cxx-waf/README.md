Usage
=====

WAF build system uses two build stages:

1. Configuration

        ./waf configure [optional-flags]

2. Build

        ./waf build
        # or just ./waf

After successful build, the compiled binaries will be located in `./build` folder and can be installed to standard location using `./waf install` command.
