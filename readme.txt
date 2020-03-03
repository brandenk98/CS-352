0. Branden Kushnir () and Michael Rizzo (mjr336)

1. Briefly discuss how you implemented your recursive client functionality.

Because there are two servers, a Root Server(RS) and a Top-Level Server(TS), we used two sockets in the Client, one socket per server. In either server, the DNS tables are stored as Python dictionaries in whichthe keys are the hostnames. The Client will query the RS first. The RS will either return the "A" flag which means the queries is found on the RS. Or the RS will return the "NS" flag and the hostname of the TS. The Client then queries the TS. From the there, the TS will either have the hostname and "A" flag or report "Error: HOST NOT FOUND". 

2. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

So far there are no none issues.

3. What problems did you face developing code for this project?

Remebering to have the server threads running befor the client was the most recurrent and tedious problem. The second most prominent problem was making sure the port inputs were consistent across all files. Our solution was to write down stages of execution before testing. 

4. What did you learn by working on this project?

We learned to manage multiple sockets across multiple machines and exhchanging data between various formats. It demystified how a Recurisve-DNS works. 