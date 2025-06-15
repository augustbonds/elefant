#!/bin/bash

# Deploy static files to nginx directory
# Run this script after updating CSS or other static files

echo "Deploying static files to nginx directory..."

# Copy static files to nginx directory
sudo cp -r /home/pi/elefant/app/static/* /var/www/elefant.augustbonds.com/

# Set proper ownership and permissions
sudo chown -R www-data:www-data /var/www/elefant.augustbonds.com/
sudo chmod -R 644 /var/www/elefant.augustbonds.com/*.css
sudo chmod -R 644 /var/www/elefant.augustbonds.com/css/*
sudo chmod 755 /var/www/elefant.augustbonds.com/css

echo "Static files deployed successfully!"
echo "Updated files:"
ls -la /var/www/elefant.augustbonds.com/css/