#!/bin/bash

echo "Executing create_pkg.sh..."
pip install virtualenv

pwd

dir_name=lambda_dist_pkg/
mkdir -p $path_cwd/$dir_name

# Create and activate virtual environment...
virtualenv -p $runtime env_$function_name
ls -altr
source env_$function_name/bin/activate

# Installing python dependencies...
FILE=./requirements.txt

if [ -f "$FILE" ]; then
  echo "Installing dependencies..."
  echo "From: requirements.txt file exists..."
  pip install -r "$FILE"

else
  echo "Error: requirement.txt does not exist!"
fi

# Deactivate virtual environment...
deactivate

# Create deployment package...
echo "Creating deployment package..."
ls -altr
cp -r env_$function_name/lib/$runtime/site-packages/* $path_cwd


echo $path_cwd/$dir_name
ls -alt $path_cwd

# Removing virtual environment folder...
echo "Removing virtual environment folder..."
rm -rf $path_cwd/env_$function_name

echo "Finished script execution!"
