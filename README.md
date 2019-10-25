# RDDT-Discord-Bot-Azure
RDDT Discord bot migrated to Serverless using Azure

# Required Azure Services
RDDT Discord Bot is reliant on two Azure Services, Azure CosmosDB and Azure ServiceBus

# Microservices and functions
citadel_check.py - Handles allowing and removing clans from citadel and removing people who have left clans, run every 6 hours, kept alive by Docker  
cone_remover.py - Handles removing Cone from users when time expires  
discord_listener.py - Connects to Discord Gateway and put various discord events on service bus for processing  
flask_site.py - Runs registration site for users  
message_handler.py - Removes events from Service bus and processes them  
wot_updater.py - Checks Wargaming API and handles updates for users who have changed  
