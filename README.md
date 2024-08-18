# Betting App 🎲

## Overview

The Betting App is a Django-based platform that allows users to register and participate in betting draws. The registration process is broken down into four distinct phases, each secured with access tokens to ensure that the same user completes all steps. The app uses JWT for authentication, providing a secure environment for users to engage in betting activities.

### Features

- User Registration in Four Phases:

  - Phase 1 - Mobile Number Registration: Users begin by registering their mobile number.
  - Phase 2 - OTP Verification: Users verify their mobile number via OTP (One-Time Password).
  - Phase 3 - Personal Details Submission: Users submit their personal details.
  - Phase 4 - User Activation: Final step to activate the user account.

- Access Token Management:

  - An access token is generated at each registration phase.
  - The token is required in the subsequent phase to ensure that the process is being completed by the same user.

- Custom Authentication Backend:

  - Utilizes JWT (JSON Web Token) for secure user authentication, implemented using the `pyJWT` library.
  - A custom authentication backend is created to handle mobile authentication.

- Betting Draw Participation:

  - Users can browse available draws to place bets.
  - After selecting a draw, users can enter the amount they wish to bet and choose their pick number.

## API Endpoints

**Authentication**
  - POST /auth/login: Authenticate the user and issue a JWT.
  - POST /auth/logout: Log out the user by invalidating the JWT.
  - POST /auth/refresh: Refresh the JWT for an authenticated session.
  - GET /auth/user: Retrieve the authenticated user's details.

**User Registration**
  - POST /registration/mobile: Start the registration process by submitting the mobile number (Phase 1).
  - POST /registration/otp-verify/{token}: Verify the OTP sent to the mobile number (Phase 2).
  - POST /registration/personal-detail/{token}: Submit personal details for the user account (Phase 3).
  - POST /registration/user-activate/{token}: Activate the user account to complete registration (Phase 4).

**Wagering**
  - GET /wager/pick1/: Retrieve available draws.
  - POST /wager/pick1/place/: Place a bet by entering the amount and pick number.
  - POST /wager/pick1/confirm/: Confirm the selected draw.

## Swagger Screenshot

![image](https://github.com/user-attachments/assets/89aea256-a973-4835-ade9-2f519d7cbb9b)

You can see this live on this link: ![Swagger Doc](https://betting-app-wo1j.onrender.com/swagger/)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/betting-app.git
   ```

2. Create a Virtual Environment:
   ```
   python -m venv venv
   ```
   
3. Activate the Virtual Environment:
   ```
   venv/scripts/activate  # Windows

   source venv/bin/activate #Linux
   ```
   
4. Install Dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set Up the database:
   ```
   python manage.py migrate
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```
