DiscussionUpdater
=================

This is a program written for reddit.com/r/onepiece to update the links to discussion links for newly submitted anime and manga links.

The program is written in python and uses The Python Reddit Api Wrappe (PRAW).

The program is currently meant to be scheduled to run during certain times on computer based on when you expect a user to submit data, or integrated into a bot used by the subreddit.

Note: Make user a useragent name is unique to you

How it works:

- This code downloads the wiki into a file
- Checks the file for the latest currently linked discussion, and then if there is newer
- If there is newere it writes it to the file locally, the online

