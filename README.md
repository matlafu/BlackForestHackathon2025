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

---

## Home Assistant: Add Voice Command Webhook Automation

To enable voice commands (e.g., via Siri Shortcuts) to trigger Home Assistant actions and receive a custom response, add the following automation to your `automations.yaml`:

```yaml
- id: 'siri_webhook'
  alias: Handle Siri Command Webhook
  description: 'Handles incoming webhook commands from Siri'
  trigger:
    - platform: webhook
      webhook_id: siri_command
  action:
    - service: rest_command.call_appdaemon
      data_template:
        payload: "{{ trigger.json }}"  # Send the webhook data to AppDaemon for processing
    - wait_for_trigger:
        - platform: event
          event_type: appdaemon_response
          event_data:
            command_id: "{{ trigger.json.command_id }}"  # Match the response to the command
    - service: notify.notify
      data_template:
        message: "{{ trigger.event.data.message }}"  # Use the custom response message from AppDaemon
  mode: single
```

- Adjust the `webhook_id` and actions as needed for your setup.
- The `rest_command.call_appdaemon` should be defined in your `rest_command` configuration to forward the payload to your AppDaemon endpoint.
- This automation sends the webhook data to AppDaemon, waits for a response event (`appdaemon_response`), and then notifies the user with the custom response message from AppDaemon.
