# OpenC2 Python Package

## Pre build
1. Set the PKG_NAME env variable
	
	```bash
	PKG_NAME=oc2
	export PKG_NAME
	```
	 
2. Edit the version.json file as necessary
3. Copy the contents of the jadn/libs folder to package in the folder PKG_NAME is set as (oc2)
	
	```bash
	mkdir -p $PKG_NAME && cp ../jadn/libs ./$PKG_NAME
	```

## Building manually
	1. Install required packages for building - setuptools, wheel
		- setuptools should be installed with pip

		```bash
		pip install setuptools wheel
		```

	2. Run command to build the wheel

		```bash
		pip wheel . -w ./dist
		```

	3. Use the build whl as neeeded
		- The file is located in the dist folder with the naming schema of
			- {distribution}-{version}(-{build tag})?-{python tag}-{abi tag}-{platform tag}.whl
