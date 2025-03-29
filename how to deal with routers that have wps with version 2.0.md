# Dealing with Routers that Have WPS 2.0

To work with routers that use WPS 2.0, you’ll need to follow a more advanced approach due to the stronger security measures it implements compared to WPS 1.0. Here's a method you can try, which involves running reaver with a sophisticated set of rules to test WPS PINs.

## Steps for WPS 2.0 Attack:
Run reaver with the following command:

bash
Copy
Edit
reaver -i wlan0 -c 1 -b TARGET_ROUTER_MAC -vv -L -N -d 15 -T .5 -r 3:20
This command adjusts the timing to simulate human behavior, but note that you will eventually lock the router after 3-4 attempts. Changing your MAC address after 1-2 attempts won’t help—the router will still lock.

If you get locked out, you’ll need to reset the router to clear the locked state.

## Resetting the Router:
To reset a router after locking it, follow these steps, which require running multiple commands at once. Open 5 terminal windows and run these commands concurrently:

mdk3 monX a -a xx:xx:xx:xx:xx:xx -m

mdk3 monX m -t xx:xx:xx:xx:xx:xx

mdk3 monX d -b blacklist -c X

mdk3 monX b -t xx:xx:xx:xx:xx:xx -c X

wash -i monX -C

This may not work with all routers, but it's worth trying.

## Detailed Experience and Challenges:
In my tests with 7 different routers, I found a mix of WPS 1.0 and WPS 2.0 routers, with chipsets from Atheros, Realtek, Ralink, and Broadcom. I used a Panda PAU05 adapter, which supports injection with 94%-100% success. However, new PAU05 adapters with chipset RT5372 do not support injection (Note: check the chipset before buying).

I focused on testing WPS 2.0 security. After running reaver for 40 minutes without success, I adjusted the settings to introduce timeouts between attempts, simulating human behavior. While this approach improved my results, it still took 40-70 seconds per PIN, which means 9 days to test all possible PIN combinations, but likely closer to 4-5 days to find the correct one.

## Router Lockout Issue:
The main problem with WPS 2.0 was that I got locked out after 3-4 attempts. When this happens, reaver will retry the first PIN (e.g., 12345670), and wash will show that the router is locked. I attempted to solve this by spoofing my MAC address and using a different Wi-Fi card, but I still got locked out.

## Resetting the Router with MDK3:
Eventually, I found a forum post (Source) describing how to reset the router by spamming it until it resets. All the routers I tested were old models, and they were vulnerable to this type of reset. However, this may not work on all routers, and some may be resistant to such attacks.

## Automating the Process:
To bypass lockouts, I wrote a script that ran reaver with longer delays to appear more human, and used mdk3 to reset the router if it got locked. After resetting, the process would continue. Later, I wrote another script using crunch (a password-generating tool) to create custom PINs and fed them into reaver.

While this approach worked, it’s not fast. The attack took days to succeed and was highly noticeable—your router will periodically reset itself.

## Final Thoughts and Future Work:
Although I achieved the desired result, I’m not satisfied with the performance. It took much longer than I expected, and WPS 2.0 remains much more secure than WPS 1.0.

I'll continue testing to see if there are ways to optimize the process using tools like reaver or bully. However, if you are working in a real-world scenario, keep in mind that WPS 2.0 is not foolproof, and attacks against it can be slow and cumbersome.

## Legal Disclaimer:
Remember that hacking into other people's networks, restarting their routers, or disrupting their services is illegal in many countries. This guide is for educational purposes only. Always get permission before testing any network.

This version should address the question and offer a clear, step-by-step approach to dealing with WPS 2.0 routers while providing insights into the process. Let me know if you need further adjustments!
