<div align="center">
  <img src="https://github.com/cailmaminiaina/AI-ChatBot-for-Companies/blob/main/assets/public/ampalibe.png" alt="Ampalibe" width="100"/>
  <img src="https://github.com/cailmaminiaina/AI-ChatBot-for-Companies/blob/main/assets/public/ChatGPT-Logo.svg.png" alt="Openai's AI" width="100"/>
</div>

# **AI Chatbot Messenger for Company Customer Service**

![Status](https://img.shields.io/badge/status-running-brightgreen?style=for-the-badge)

This project is an AI chatbot designed to enhance customer service for companies on Messenger, using the Ampalibe framework. It integrates unofficial OpenAI's API (Open Source) to support interactions, provide answers, and offer helpful information to customers.


![Status](https://img.shields.io/badge/FEATURES-red?style=for-the-badge)

**Reverse engeenering**: Uses OpenAI's unofficial API (reverse proxy) for improved accuracy in responses.

**Customizable**: Easily add your company's informations to **info_bot.txt**.

**Environment Variable**: Configure your PAGE ACCESS TOKEN, API KEY and ADMIN_ID (messenger id of the chat responsable) in the **.env** file.


## **🚀 Getting Started**

[![Facebook](https://img.shields.io/badge/Facebook-blue?style=for-the-badge)](https://developers.facebook.com/)
[![Messenger](https://img.shields.io/badge/Messenger-purple?style=for-the-badge)](https://developers.facebook.com/docs/messenger-platform/getting-started/app-setup)

### **Facebook App Creation**

**1. Create a Facebook Developer Account:**

  . Go to the [Facebook Developer](https://developers.facebook.com/) and log in or create an account if you don’t have one.
    
**2. Create a New App:**

        
  . Go to **My Apps** > **Create App**.
  
  . Choose the **Business** option, then click Next.
  
  . Fill in the required fields, then click **Create App ID**.

**3. Set Up Messenger:**

  . In the **Add a Product** section, select **Messenger** and click **Set Up**.
  
  . In the **Messenger setting**s, generate a **Page Access Token** by connecting a Facebook Page and add **Subscription** (**messages** and **messaging_pstbacks**).
  
  . Copy the **PAGE_ACCESS_TOKEN** for later use in the .env file.

**4. Webhook Setup:**
**(Do this after running the Ampalibe App and Ngrok)**

  . Under **Webhooks**, click **Add Callback URL**.
  
  . Use https://YOUR_NGROK_URL/ as the callback URL (replace YOUR_NGROK_URL with your actual ngrok URL).
  
  . Set a **Verify Token** (any secure token of your choice) and add it to your **.env** file.
  
  . Subscribe to the required fields (e.g., **messages**, **messaging_postbacks**).

**5. App Review:**

  . Submit for App Review to get permission to use the bot in production.

### **Installation**

[![Install Ampalibe](https://img.shields.io/badge/Install-Ampalibe-blue?style=for-the-badge)](https://pypi.org/project/ampalibe/)
[![Install OpenAI](https://img.shields.io/badge/OpenAI-white?style=for-the-badge)](https://pypi.org/project/openai/)
[![Run App](https://img.shields.io/badge/Run-App-brightgreen?style=for-the-badge)](#)

**Fork or Clone this repository**

    git clone https://github.com/cailmaminiaina/AI-ChatBot-for-Companies.git && cd AI-ChatBot-for-Companies
    
**Install Ampalibe Framework**

    pip install ampalibe
    
**Install OpenAI**

     pip install openai

**or**

    pip install -r requirements.txt
     
### **Get API KEY**

. Join our [Discord server](https://discord.pawan.krd).

. Obtain an API key from the `#Bot` channel with the `/key` command.
   
### **Environment Setup**

. Add Company Info: Include details in **info_bot.txt**.

. Environment Variables: Add PAGE_ACCESS_TOKEN, VERIF_TOKEN, ADMIN_ID (messnger id of the chat responsable) and API_KEY in the **.env** file.

### **Run the Application**

    ampalibe run

### **Testing Locally**

Use ngrok to expose the local server for testing.

. Download and set up ngrok [here](https://ngrok.com/) and run on another terminal:

    ngrok http 4555
    
. Use https://YOUR_NGROK_URL/ as the callback URL for the **Webhooks** (replace YOUR_NGROK_URL with your actual ngrok URL).

## **💻 Developers and Contributors**

Developed by: **Cail Maminiiana**

[GitHub](https://github.com/maminiainalaic) | [Facebook](https://facebook.com/maminiaina.cail)

Contributor: **Pawan Osman**

## **☕ Support the Project**

If you find this project useful, consider buying me a coffee!

![Status](https://img.shields.io/badge/TaptapSend-darkgreen)

    +261341820966
    +261324903869
