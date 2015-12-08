## Up 
### A directory service for machine-payable endpoints

Being able to find machine-payable endpoints is essential to building interesting
applications both for machine and human consumption. To help with this, I wrote a directory
service backed by a crawler and now with a text-based browser front-end.

The best intro is probably to use the endpoint browser. First, it will prompt you for confirmation
and purchase the latest directory results for 250 satoshis. Then it will let you curl each endpoint
through a menu. Start it with:

    python3 browser.py

To get the raw results that this is using, you can open the file that was just created called 
`up-output.cache` or run:

    21 buy --maxprice 250 url http://10.244.34.100:21411/up

To add your own service, provide your url (with port number) in the following command:

    21 buy --maxprice 250 url http://10.244.34.100:21411/put?url=your_endpoint_url

Your endpoint will be crawled on the next run, currently set to every 8 hours. Each run updates the 
name, owner and description from the json provided at the endpoint. For that reason, I recommend 
providing /info urls over 402-required endpoints.

If satoshis are burning a hole in your wallet, you can try the **premium** endpoint which is better 
because it gives you full info (including description and time last seen) about services seen in the 
last week.

    21 buy --maxprice 1000 url http://10.244.34.100:21411/up-premium

If you would like to see if any other endpoints are available, use curl to get the /info endpoint.

    curl http://10.244.34.100:21411/info
