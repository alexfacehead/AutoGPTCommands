# Auto-GPT: An Autonomous GPT-4 Experiment

---------------------------------------------

# THIS IS A FORK.

I have updated the project to WORK. This is enough for *baseline functionality*-
but it isn't perfect! The original project is getting bigger every day, and
unfortunately, I'm not impressed.  I've begun development on a langchain from scratch
which is currently private but working much, much faster than this.

When the kinks are ironed out, it'll be here :)

# HOW TO USE
* `download dependencies please!`
* `setup your .env file with at LEAST your keys, desired LLM + filepathing`
* run `python main.py`
Enjoy! If you have issues, I'm hoping it's not too difficult to patch them up, so please let me know if there are. Part of the reason I forked this was to keep a snapshot of it before it got complexified
and all messy.

Remember, this script uses SearX. Remove the functionality from file_operations or simply omit the key
if you don't want to - but it's free, and Google API isn't (after a certain num of requests)

TODO:
* Fix the horrible, horrible json prompting
  * Possibly remove json altogether. There are better formats - even XML would be 
  less intensive on the LLM than json. We shouldn't be using LLMs illustrious 
  processing power for json formatting!
* Make SearX optional
* Switch to pinecone or ChromaDB over this crappy array-based short-term memory
