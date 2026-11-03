# Campus Lost and Found System (PHINMA COC)

A console-based Python application developed for PHINMA Cagayan de Oro College to manage, search, mask, and update lost and found property records.

## 📌 System Highlights
- **Role-Based Workflows:** Distinct transaction paths for Students and System Administrators.
- **Privacy Detail Masking:** Automated title masking (`title[:3] + "****** [PRIVACY]"`) for sensitive items (IDs, wallets) when viewed by non-admin accounts.
- **Category Indexing:** Filter and search items via standardized category tags (`Electronics`, `Identification`, `Personal Items`, `Books`).
- **Status Tracking:** Admin controls for updating item states (`Unclaimed`, `Claim Pending`, `Returned`).
- **In-Memory Architecture:** Native Python lists and dictionaries with zero external database dependencies.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the System
1. Clone this repository:
   ```bash
   git clone https://github.com/emz1-main/Campus-Lost-and-Found-System.git