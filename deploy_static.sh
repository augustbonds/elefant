#!/bin/bash

# Deploy static files to nginx directory
# Run this script after updating CSS, JavaScript, or other static files

echo "Deploying static files to nginx directory..."

# Copy static files to nginx directory
sudo cp -r /home/pi/elefant/app/static/* /var/www/elefant.augustbonds.com/

# Set proper ownership and permissions
sudo chown -R www-data:www-data /var/www/elefant.augustbonds.com/

# CSS files permissions
sudo chmod -R 644 /var/www/elefant.augustbonds.com/*.css
sudo chmod -R 644 /var/www/elefant.augustbonds.com/css/*
sudo chmod 755 /var/www/elefant.augustbonds.com/css

# JavaScript files permissions
sudo chmod -R 644 /var/www/elefant.augustbonds.com/js/*
sudo chmod 755 /var/www/elefant.augustbonds.com/js

# Other static files permissions (favicon, etc.)
sudo chmod 644 /var/www/elefant.augustbonds.com/*.ico
sudo chmod 644 /var/www/elefant.augustbonds.com/*.png

echo "Static files deployed successfully!"
echo "Updated CSS files:"
ls -la /var/www/elefant.augustbonds.com/css/
echo
echo "Updated JavaScript files:"
ls -la /var/www/elefant.augustbonds.com/js/