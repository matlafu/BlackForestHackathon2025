### UNQUACK

## Miro for the project
https://miro.com/welcomeonboard/UHRWSFI5a3Job3cxSTVzanYvTG1YRWN3bkF2Z2VKcWRLeHFTWUlFTyt4TjNRQXVVYTIrQ0VhR0VXdDJIU0ZibFNnLzRHSEhieWhsVUxwd1dPWjFHVzY0akg0aVlwa2N3OVJUUzN2TU9CU1g0eXJENGFSaDdDanhBL2lUeU83TjJhWWluRVAxeXRuUUgwWDl3Mk1qRGVRPT0hdjE=?share_link_id=440103296435

## Relevant data
https://cloud.sbamueller.de/index.php/s/xazJLz2L6nQtLeB

## Quickstart for Developers

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   ```bash
   cp balkonsolar/.env.example balkonsolar/.env
   # Edit balkonsolar/.env with your credentials and configuration
   ```

5. **Run AppDaemon:**
   - Using the provided script (recommended, loads environment variables automatically):
     ```bash
     ./run_appdaemon.sh
     ```
   - Or run directly (if your environment is already set up):
     ```bash
     appdaemon -c balkonsolar/appdaemon
     ```

For more details, see the technical documentation in `memory-bank/techContext.md`.
