# Auto-GPT: An Autonomous GPT-4 Experiment

---------------------------------------------

# THIS IS A FORK.

I have updated the project to WORK. This is enough for *baseline functionality*-
but it isn't perfect! The original project is getting bigger every day, and
unfortunately, I'm not impressed.  I've begun development on a langchain from scratch
which is currently private but working much, much faster than this.

When the kinks are ironed out, it'll be here :)

# HOW TO USE
**IMPORTANT**: Please rename your `.env.template` file to just `.env`, this will make your environment variables viewable. If it isn't recognized and you are getting missing API key errors, please hardcode your `.env` filepath to whatever it may be in `config.py` (line 5)

**ALSO IMPORTANT** If you don't have a SearX search server, then remove those lines (all 3 - server, user, pass included) from the `.env` file. You will need *some* type of search, so please setup a google search API if you want to have search functionality.

If you don't want to use any type of search, please use the --no-search flag.

(so run `python main.py --no-search`  or `./run.sh --no-search` from the right directories)

* `download dependencies please!`
* `setup your .env file according to the template with at LEAST your keys, desired LLM + filepathing`
* run `python main.py` from /Auto-GPT/scripts/ or `./run.sh` from /Auto-GPT/
Enjoy! If you have issues, I'm hoping it's not too difficult to patch them up, so please let me know if there are. Part of the reason I forked this was to keep a snapshot of it before it got complexified
and all messy.

Remember, this script uses SearX. Remove the functionality from `commands.py` on lines 104/105 if you don't want to use it - but it's free and decent.

TODO:
* Fix the horrible, horrible json prompting
  * Possibly remove json altogether. There are better formats - even XML would be 
  less intensive on the LLM than json. We shouldn't be using LLMs illustrious 
  processing power for json formatting!
* Make SearX optional
* Switch to pinecone or ChromaDB over this crappy array-based short-term memory
