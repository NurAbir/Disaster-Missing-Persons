# Disaster Missing Persons - User Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [For Administrators](#for-administrators)
3. [For Rescuers](#for-rescuers)
4. [For General Users](#for-general-users)
5. [Report Status System](#report-status-system)
6. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Accessing the System

Open your web browser and navigate to the application URL (e.g., `http://localhost:8000`).

The system works on:
- Desktop computers
- Tablets
- Mobile phones (recommended for field use)

### First Login

**Default Admin Account:**
- Email: `admin@disaster-response.org`
- Password: `admin123`

> **Important**: Change the default password immediately after first login.

---

## For Administrators

### Creating Rescuer Accounts

Rescuers cannot register themselves. Only administrators can create rescuer accounts.

1. Log in with your admin account
2. Navigate to **Admin Dashboard** (link in navigation)
3. Click the **"Create Rescuer"** tab
4. Fill in the rescuer's details:
   - Full Name
   - Username (unique)
   - Email (unique)
   - Phone (optional)
   - Organization (optional)
   - Password (minimum 6 characters)
5. Click **"Create Rescuer Account"**

The rescuer will receive their login credentials and can immediately start creating reports.

### Viewing System Statistics

The **Statistics** tab shows:
- **Total Reports**: All reports ever created
- **Active**: Currently active missing person cases
- **Found**: Persons who have been located
- **Tips**: Total tips received from the public
- **Urgent**: Active urgent cases requiring immediate attention

### Managing Rescuers

The **Rescuers** tab lists all rescuer accounts with:
- Contact information
- Organization
- Account status (Active/Inactive)

### Changing Any Report Status

As an admin, you can change the status of **any** report:
1. Open any report
2. Scroll to the **"UPDATE STATUS"** section
3. Click the appropriate status button

---

## For Rescuers

### Logging In

Use the username/email and password provided by your administrator.

### Creating a Missing Person Report

1. Click **"Create Report"** in the navigation
2. Fill in all known information:
   - **Full Name** (required)
   - **Age**, **Gender**, **Height**, **Weight** (if known)
   - **Distinguishing Features**: Scars, tattoos, birthmarks
   - **Clothing Description**: What they were wearing
   - **Medical Conditions**: Important for medical emergencies
3. **Last Seen Information** (required):
   - Date and time
   - GPS coordinates (optional)
   - Address or location description
4. **Contact Information** (required):
   - Phone number for inquiries
   - Email (optional)
5. **Photos**: Upload up to 3 photos (max 5MB each by default)
   - Photos are automatically compressed for fast loading over slow connections
6. Check **"MARK AS URGENT"** if this is a critical case
7. Click **"Create Report"**

### Viewing Tips on Your Reports

1. Navigate to any report you created
2. Scroll to the **"Tips Received"** section
3. Tips are automatically marked as read when viewed
4. Contact tip providers using the provided phone/email

### Updating Report Status

When a person is found or the case is closed:
1. Open any report
2. Scroll to the **"UPDATE STATUS"** section
3. Click:
   - **Mark Found** - when the person is located
   - **Mark Closed** - when the case is resolved
   - **Mark Active** - to reopen a closed case

> **Note**: Any rescuer can change the status of any report.

---

## For General Users

### Creating an Account

Anyone can create an account to submit tips:

1. Click **"Register"** in the navigation
2. Fill in:
   - Full Name
   - Username (unique)
   - Email (unique)
   - Phone (optional)
   - Password (minimum 6 characters)
3. Click **"Create Account"**

### Viewing Reports

All active missing person reports are publicly visible:
- Browse the **"View Reports"** page
- Use filters:
  - **Search**: Find by name
  - **Urgent Only**: Show only urgent cases
  - **Status**: Active or Found
- Click any report to view full details

### Submitting a Tip

If you have information about a missing person:

1. Open the person's report
2. Scroll to **"Submit a Tip"**
3. Provide:
   - **Message** (required, minimum 10 characters): Describe what you know
   - **Your Phone** (optional): For follow-up contact
   - **Your Email** (optional): For follow-up contact
4. Click **"Submit Tip"**

> **Tip**: Be as specific as possible. Include dates, times, locations, and descriptions of who you saw and what they were doing.

---

## Report Status System

### Status Definitions

| Status | Description | Who Can Change |
|--------|-------------|----------------|
| **Active** | Person is missing, case is open, accepting tips | Rescuer who created it, or Admin |
| **Found** | Person has been located safely | Rescuer who created it, or Admin |
| **Closed** | Case is resolved or no longer active | Rescuer who created it, or Admin |

### Status Visibility

| Action | Admin | Rescuer (Owner) | Rescuer (Other) | User |
|--------|-------|-----------------|-----------------|------|
| View report | Yes | Yes | Yes | Yes |
| Submit tip | Yes | Yes | Yes | Yes |
| View tips | All reports | Own reports only | No | No |
| Change status | Any report | Own reports only | No | No |
| Create report | Yes | Yes | No | No |

---

## Troubleshooting

### Cannot Log In

- Verify your username/email and password
- Check if your account is active
- Clear browser cache and try again

### Cannot Create Report

- Ensure you are logged in as a **Rescuer** (not a regular User)
- Rescuer accounts must be created by an Admin
- Check your internet connection

### Photos Not Uploading

- Maximum file size: 5MB per photo
- Supported formats: JPEG, PNG, GIF
- Maximum 3 photos per report
- Try compressing photos before upload if they are too large

### Tips Not Submitting

- You must be logged in to submit tips
- Message must be at least 10 characters
- Tips can only be submitted for **Active** reports

### Cannot Change Report Status

- Only **rescuers** and **admins** can change status
- Regular users cannot change report status
- Make sure you are logged in

### Page Not Loading

- Check your internet connection
- The system is designed to work on slow connections
- Try refreshing the page
- Contact your system administrator if problems persist

---

## Support

For technical issues, contact your system administrator.

For emergencies, always call your local emergency services first.
