from redditf import *
import praw, json, time, Phrases

reddit = get_reddit()

ctime = time.ctime
bot_user_name = reddit.user.me().name
comment_reply = M.GetMessage(1)

WriteLog("\n****\nTime:{} Event: Starting Bot {}".format(ctime(time.time()), bot_user_name))

SubToScan = "test+testingground4bots+bottesting"
phrases = Phrases.Phrase
sleep_time = 60*1
print("The Bot is in control",bot_user_name)



for comment in reddit.subreddit(SubToScan).stream.comments():
    commentbody = comment.body
    commentbody = commentbody.lower()
    if inString(phrases,commentbody)[0]:
        print("Triggered by {}".format(inString(phrases,commentbody)[1]))
        WriteLog("\nTime:{} Event: Bot Triggered by phrase={}".format(ctime(time.time()),inString(phrases,commentbody)[1]))
        if isValid(comment):
            try:
                AuthorID = comment.author.id
                IncrementHugs(AuthorID)
                comment.reply(comment_reply.format(comment.author.name,GetHugs(AuthorID)))  
                print("Reply made to {}".format(comment.author.name))
                WriteLog("\nTime:{} Action: Reply made to {}".format(ctime(time.time()),comment.author.name))
                
            except praw.exceptions.APIException  as error:
                print(error)
                print("Error! Slepping for {} seconds".format(sleep_time))
                WriteLog("\nTime:{} ->Action: Error! Slepping for {} seconds".format(ctime(time.time()),sleep_time))
                time.sleep(sleep_time)
                # Try second time after cooldown
                try:
                    comment.reply(comment_reply.format(comment.author.name,GetHugs(AuthorID)))
                    print("Replying second time")
                    WriteLog("\nTime:{} Action: Replying second time".format(ctime(time.time())))
                except Exception as e:
                    DecrementHugs(AuthorID)
                    print("Reply Failed!")
                    WriteLog("\n->Message: Replying second time FAILED")
                    continue

                print("Continuing")
                WriteLog("\nTime:{} Event: Continuing".format(ctime(time.time())))
        else:
            print("Already Replied")
            WriteLog("\nTime:{} Message: Already replied to comment".format(ctime(time.time())))

input("Shhh! The Bot is sleeping")

