
# **Discord Resource Optimization Bot**  

A Python-powered Discord bot designed to optimize in-game resource conversions for maximum crafting efficiency. This bot calculates the best conversion strategy for resources like **timber**, **tender**, and **abidos** to maximize the number of fusions while leaving minimal leftover resources.

---

## **Features**  
- **Dynamic Resource Optimization**: Calculates the maximum possible fusions based on the user's available resources.  
- **Optimal Conversion Strategy**: Recommends how to convert timber and tender into additional abidos efficiently.  
- **Interactive Discord Commands**: Users input their resources via the `!optimize` command and receive instant results.  
- **Detailed Reports**: Provides a comprehensive summary of the optimal strategy, resource usage, and remaining resources after conversions.  
- **Secure Token Management**: Uses `.env` files to protect the bot's authentication token.  
- **Cloud Hosting**: Deployed the bot on Google Cloud for 24/7 availability.  

---

## **Getting Started**  

### **Prerequisites**  
- Python 3.8+  
- Discord account and bot token  
- Discord server to invite the bot  


## **How to Add the Bot to Your Server**  

Click the link below to invite the bot to your server:  
[Invite the Bot](https://discord.com/oauth2/authorize?client_id=1305021482988081255&permissions=124928&integration_type=0&scope=bot)

---

## **Cloud Deployment**  

### **Using Google Cloud**  
The bot is hosted on Google Cloud to ensure 24/7 availability.  

**Steps Taken for Deployment**:  
1. Created a virtual machine instance on Google Cloud Platform (GCP) with Python pre-installed.  
2. Transferred the bot files to the virtual machine using SCP or Git cloning.  
3. Installed necessary Python dependencies on the VM.  
4. Used `nohup` to run the bot in the background, ensuring it continues running even after the SSH session is closed:  
   ```bash
   nohup python bot.py &
   ```  
5. Configured the VM to restart the bot automatically if it stops.  

---

## **Usage**  

1. After adding the bot to your server, click on the bot's profile to add the App to your own profile or the server.

2. Use the `/optimize` command to input your resource values:  

```bash
/optimize <timber> <tender> <abidos>
```  

### **Example**:  
```bash
/optimize 470 300 12694
```  

### **Bot Response**:  
```plaintext
**Resource Optimization Results:**
Maximum possible fusions: 33

**Optimal conversion strategy:**
Convert 300 timber to lumber powder
Convert 150 tender to lumber powder

**Conversion details:**
Lumber powder created: 360
New abidos from conversion: 36

**Remaining resources after ALL conversions and fusions:**
Timber: 12
Tender: 0
Abidos: 0

**Verification:**
Resources used in fusions:
Timber used: 2838
Tender used: 1485
Abidos used: 1089
```

---

## **How It Works**  

The bot uses a custom algorithm to:  
1. Determine how many resources can be converted into **lumber powder**.  
2. Convert lumber powder into **additional abidos**.  
3. Calculate the maximum number of fusions possible while respecting resource constraints.  
4. Provide recommendations for optimal conversions and display the results.  

---

## **Technologies Used**  

- **Programming Language**: Python  
- **Discord API**: `discord.py`  
- **Environment Variable Management**: `dotenv`  
- **Cloud Hosting**: Google Cloud Platform (GCP)  
- **Background Execution**: `nohup`  

---

## **Contributing**  

Contributions are welcome! To contribute:  
1. Fork the repository.  
2. Create a new branch: `git checkout -b feature-name`.  
3. Commit your changes: `git commit -m "Add feature"`.  
4. Push to your branch: `git push origin feature-name`.  
5. Open a pull request.  

---

## **License**  

This project is licensed under the MIT License.  

---

## **Contact**  

For questions or feedback, feel free to reach out:  
- **Email**: [jdonghyun02@gmail.com](mailto:jdonghyun02@gmail.com)  
