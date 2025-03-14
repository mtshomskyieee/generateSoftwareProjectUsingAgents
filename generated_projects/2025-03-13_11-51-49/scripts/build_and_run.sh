#!/bin/bash

# Install dependencies
echo "Installing dependencies..."
# Assuming there are some npm packages required for the JavaScript game
npm install

# Compile project if necessary
# As this is a JavaScript project, there is typically no compilation needed.
# If we had C++ code or something similar, we would run a hypothetical compile command.
# For example: g++ -o asteroids_game asteroids_game.cpp 
# echo "Compiling the project..."

# Create a script that runs unit tests
echo "Creating script to run unit tests..."
cat <<EOL > run_tests.sh
#!/bin/bash
echo "Running unit tests..."
# Assuming we are using a JavaScript testing framework like Jest for unit tests
# Install jest if not already installed
npm install --save-dev jest
# Run tests
npx jest --verbose
EOL

chmod +x run_tests.sh
echo "Setup complete! You can now run the unit tests with ./run_tests.sh"