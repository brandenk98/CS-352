1. Branden Kushnir (bik9) and Michael Rizzo (mjr336)

2. Briefly discuss how you implemented the LS functionality of tracking which TS responded to the query and timing out if neither TS responded.

First we queried ts1 and ts2. We knew we could try and wait for a connection timeout as each ts would not send a response if nothing was found. This was implemented through exception handling in the LS; we would look for a response from ts1 and if 'socket' timed out we then check ts2. If ts2 had no response and socket timed out as well, then we would return the error message to the client. 

3. Are there known issues or functions that aren't working currently in your attached code? If so, explain.

Once again, there are no known issues at the current time. 

4. What problems did you face developing code for this project?

Minor formatting when sending the messages between servers. This was solved by making sure the files were processed correctly and that each ts opened its respective file. Off-by-One errors are a common bane. 

5. What did you learn by working on this project?

We learned not only how a Load Balancing Server works but how its operation differs from the previous project. 