## Usage

### Setting up ID Category Notifications

1. Go to **Contacts > Configuration > Partner ID Categories**
2. Select an existing ID category or create a new one
3. In the category form, enable the **"Send Notification"** checkbox
4. Set the **"Days Before Expiration"** field to specify how many days before the ID expires the notification should be sent
5. Select an **"Email Template"** to be used for sending the notification
6. Save the category

### Creating Partner IDs with Expiry Dates

1. Go to any **Partner form**
2. Navigate to the **"Other Info"** tab (or similar, depending on your localization)
3. Click on **"ID Categories"** or **"Identity Documents"**
4. Create a new ID record by:
   - Selecting the appropriate **ID Category** (one with notifications enabled)
   - Entering the **ID Number**
   - Setting the **Valid From** and **Valid Until** dates
5. The system will automatically check for expiring IDs based on your configuration

### How Notifications Work

The module works through a scheduled action that:

1. Searches for ID numbers that meet the following criteria:
   - The ID category has **"Send Notification"** enabled
   - The ID category has a **"Days Before Expiration"** value greater than 0
   - The ID number status is either **"open"** or **"pending"**
   - The ID is expiring within the specified number of days
   - The ID hasn't been notified already (no **"Notification Date"**)

2. For each matching ID number, it sends an email using the configured template

3. Records the notification date to avoid sending duplicate notifications

### Testing Notifications

To test the notification system:

1. Set up a test ID category with notification settings
2. Create a test partner ID with an expiry date within the notification window
3. Manually execute the scheduled action: **"Send Expiry Notifications"** 
4. Check that the notification email is sent and the notification date is recorded

### Email Templates

The module uses email templates to customize notification messages:

1. Go to **Settings > Technical > Email > Email Templates**
2. Create or modify templates for the **"res.partner.id_number"** model
3. Use placeholders like `{{ object.name }}` for ID number and `{{ object.partner_id.name }}` for partner name
4. Set the template in your ID category configuration

### Scheduled Action

The notification process runs automatically via a scheduled action:
- **Name**: "Send Expiry Notifications"
- **Interval**: Daily by default
- **Next Execution**: Configurable in **Settings > Technical > Automation > Scheduled Actions**

You can modify the frequency of the scheduled action based on your requirements.