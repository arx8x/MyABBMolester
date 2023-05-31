## **My ABB PoC**

MyAbb is vulnerable. It leaks user data without even the user having to login or obtain any security token from the server.  
If you send a request to reset password by just entering the user id, it sends back the password in plaintext. Beautiful!

You can then login on the website or programmatically and get the user data such as 
- Name
- Address
- Phone number
- Email
- Password (well, this is available before login as well)
- Mac Address 
- Currently assigned IP address (DHCP unless you have static IP)
- Plan details
- Outstanding amount
- Usage details, per session
- Invoices
- Tickets
- Other misc info about the connection

This is really bad because a lot of people use the same password for other websites and social media. 
The incompetence is all over the website, API design and data structures.

## I reported this
In 2018, I reported this issue to the developers, but they did nothing to fix it. My report was ignored countless times. It's only with the help of a nodal officer that I was able to get the report to the developers. Asianet doesn't care about this issue at all. At that point, the password reset OTP was time-based. As in, if the time was `13:26:11`, the OTP would be `132611`. You can't accurately predict the seconds value but it was fairly easy to make a few guesses based on the server time from the response. 

They later fixed this. It took the developer an unreasonable amount of time to understand why this is bad and what I'm talking about. But then there was another issue. 

When a user sent a password reset request, they were directed to a page where the reset email and password were partially concealed. This page makes a request to the API to obtain user data. In the response, the email and phone number could be observed along with the plaintext password. For users who haven't ever set a password on this portal, the password wouldn't be available and they need to trigger a password reset. It was possible to intercept or forge the password reset request and replace the user's information with your own email and/or phone number. Consequently, the OTP would be sent to you instead of the intended user, allowing you to proceed with the password reset and gain unauthorized access to their account.

I don't know if this is fixed or not, but they have better things to worry about... like, you know, sending the password to user (or attacker) in plaintext without even needing a login.

## I was actually surprised to learn that they actually do the password verification server side and not client side. 

