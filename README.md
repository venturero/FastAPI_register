# FastAPI Registration Application

## Project Overview
This is a FastAPI application that provides user registration functionality through a local host endpoint. The project utilizes decorators for handling registration errors, OpenTelemetry for monitoring, and Docker for containerization.

## Requirements

### MongoDB Setup
* Only MongoDB URL is needed
* No specific database requirements
* Works with standard MongoDB configuration

### Browser Recommendations
Chrome users should adjust their security settings:
1. Navigate to chrome://settings/security
2. Set to "Standard Protection"
3. This prevents unnecessary password security warnings during login

## Testing Instructions
Test the registration endpoint with these combinations:
* Valid email + valid password
* Valid email + wrong password
* Valid email + empty password
* Empty email + valid password
* Empty email + empty password

## API Endpoints
* `/register` - Main registration endpoint

## Known Limitations
* MongoDB and Docker have memory limitations on free plans
* Resource usage should be monitored

## Features
* User registration
* Error handling with decorators
* OpenTelemetry integration
* Docker containerization
* MongoDB database integration

## Additional Notes
The application is designed for easy local deployment and testing. Users can access the endpoints through localhost after setting up the required environment.

---
For more details or technical support, please raise an issue in the repository.
