# Frame-Counting-Bot Version 1.02 by DrHandlock

#btw, there is no file for version 1.00 and 1.01 because they evolved into this file

print("Frame_Counter_Bot_v102 booting up ...")

import praw
from moviepy.editor import VideoFileClip
from praw.exceptions import RedditAPIException
from praw.exceptions import ClientException
import time





par = "Post Analysis Restrainment" # this i will used to prevent analysis of already alalized posts

em_break = False 
skip_first = False
event_number = 0



# Authentication
reddit = praw.Reddit(
    client_id=(''),
    client_secret=(''),
    user_agent=(),
    username=(''),
    password=('')
)
print("PRAW authenticated")






#   Functions
def log_submission_type(submission):
    if submission.is_video:
        print(f"Submission {submission.id} is a video post.")
        
    elif submission.url:
        if submission.url.endswith(('.jpg', '.jpeg', '.png', '.gif', '.gifv')):
            print(f"Submission {submission.id} is an image or GIF post.")
            
        else:
            print(f"Submission {submission.id} is a link post.")
            
    elif submission.selftext:
        print(f"Submission {submission.id} is a text post.")
        
    else:
        print(f"Submission {submission.id} type is unknown.")
        





def frame_counting(video_path, promotion):
    global event_number

    print("frame_counting active...")

    print('video attaching to analysis device')
    video = VideoFileClip(video_path)



    print('getting fps')
    FPS = video.fps

    print('getting total frames')
    total_frames = int(FPS * video.duration)

    print("...now sending resolution")
    
    result = f"This video contains {total_frames} frames at (Rounded) {int(FPS)} frames per second."

    
    # basically this will advertise the new subreddit for this bot
    if promotion:
        result += " \n \n Check out r/REcountableFrame for a subreddit that is for people who want to count frames and this bot"

    result += f"\n\n^(I am a bot, and this response is automated) \n \n ^(Warning: This bot is still in early development and bugs may occure, if there are any bugs please contact: u/)^(DrHandlock) \n \n ^({event_number})"

    return result



#subreddit_assist seems stable
def subreddit_assist():
    print("subreddit_assist was called")
    global event_number
    global par
    
    
    for subr_post in reddit.subreddit('REcountableFrame').new(limit=1):
        
        print(f"newest post being checked... {subr_post.title} ; {subr_post.id}")
        
        post_flair = subr_post.link_flair_text

        

        
        if subr_post.id != par and post_flair == "Bot Usage":
            print(f"Criteria Met: \n \n ID({subr_post.id}) doesn't match PAR({par})... Continuing...")
            if subr_post.is_video or subr_post.url.endswith(('.gif', '.gifv')):

                
                print("video/GIF contained")
                
                try:
                    
                    print('trying normal URL capture method')
                    video_url = subr_post.media['reddit_video']['fallback_url']

                except TypeError:

                    print('swapping to TypeError alternate')
                    video_url = video_url = subr_post.url  # For GIF or other media types



                
                response = frame_counting(video_url, False)

                
                try:
                    print("now trying subr_post.reply(response)")
                    subr_post.reply(response)
                    par = subr_post.id
                
                except RedditAPIException as rae:
                    print("RedditAPIException... Transfering")
                    for subextention in rae.items:
                        if subextention.error_type == "RATELIMIT":
                            wait_time = int(''.join(filter(str.isdigit, subextention.message)))
                            print(f"entering RAE sleep time of: {wait_time}")
                            time.sleep(wait_time)
                            print("waking from RAE and returning to normal vitals")
                            return


            # CROSS POSTING
            
            elif hasattr(subr_post, 'crosspost_parent_list'):
                print("crosspost contained")
                
                original_id = subr_post.crosspost_parent.split('_')[1] # this is how we get the original ID
                print(f"original_id: {original_id}") 
                og_sub = reddit.submission(id=original_id)

                if og_sub.is_video:
                    
                    print("video contained with in crossposting methods")
                    video_url = og_sub.media['reddit_video']['fallback_url']
                    
                    response = frame_counting(video_url, False)

                
                    try:
                        print("now trying subr_post.reply(response)")
                        subr_post.reply(response)
                        par = subr_post.id
                
                    except RedditAPIException as rae:
                        print("RedditAPIException... Transfering")
                        for subextention in rae.items:
                            if subextention.error_type == "RATELIMIT":
                                wait_time = int(''.join(filter(str.isdigit, subextention.message)))
                                print(f"entering RAE sleep time of: {wait_time}")
                                time.sleep(wait_time)
                                print("waking from RAE and returning to normal vitals")
                                return

                

               

#To my current knowledge this also finsihed
def inbox_assist():
    global event_number
    global em_break
    
    print("inbox_assist called")
    
    unread_messages = list(reddit.inbox.unread(limit=None))
    print(f"Number of unread messages: {len(unread_messages)}")

    print("======= \n messages include:")
    for item in unread_messages:
        print(item.body)


    print("======")
    for message in reddit.inbox.unread(limit=None):
        print(f"unread message detected within INBOX...   {message}")
        
        if message.body.lower() == "u/frame-counting-bot":
            print("username detected")

            try:
            
                comment = reddit.comment(message.id)
                submission = comment.submission

                if submission.is_video or submission.url.endswith(('.gif', '.gifv')):
                    print("submission from inbox message_origin is video")

            

                    subm_url = submission.media['reddit_video']['fallback_url']

                    try:
                        print("now trying m.reply(f_c(v_u))")
                        message.reply(frame_counting(subm_url, True))
                        print("unread message solved")
                        message.mark_read()

                
                    except RedditAPIException as RAE:
                        print("RAE CALLED within inbox_assist")
                        for subexception in RAE.items:
                            if subexception.error_type == 'RATELIMIT':
                                wait_time = int(''.join(filter(str.isdigit, subexception.message)))
                                print(f"Rate limit exceeded. Sleeping for {wait_time} minutes.")
                                time.sleep(float(wait_time) * 60)



                # ======== CROSS POST ========
                elif hasattr(submission, 'crosspost_parent_list'):
                    
                    original_id = submission.crosspost_parent.split('_')[1] # this is how we get the original ID
                    print(f"original_id: {original_id}") 
                    og_sub = reddit.submission(id=original_id)

                    
            

                    subm_url = og_sub.media['reddit_video']['fallback_url']

                    try:
                        print("now trying m.reply(f_c(v_u))")
                        message.reply(frame_counting(subm_url, True))
                        print("unread message solved")
                        message.mark_read()

                
                    except RedditAPIException as RAE:
                        print("RAE CALLED within inbox_assist")
                        for subexception in RAE.items:
                            if subexception.error_type == 'RATELIMIT':
                                wait_time = int(''.join(filter(str.isdigit, subexception.message)))
                                print(f"Rate limit exceeded. Sleeping for {wait_time} minutes.")
                                time.sleep(float(wait_time) * 60)
                    


                
                else:
                    print("This post can't be accepted")
                    log_submission_type(submission)
                    message.mark_read()
                    message.reply(f"Sorry this post could not accepted, it you believe this an error, please try again. (This problem may occur if your requested post is a GIF) \n \n ^({event_number})")


            except praw.exceptions.ClientException as peCE:
                print(f"Failed to fetch comment or submission: {peCE}")
                    
                continue
                    
                    
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                    
                continue


        
        elif message.body == "Frame-Counting-Bot_BreakMAINLOOP True [CODE: 9997q]" and str(message.author) == "DrHandlock":
            print("detected reguest for BREAKING MAIN LOOP detected...")
            message.mark_read()

        elif message.body.lower() == "good bot":
            message.mark_read()


        


    




# ========================================= Entering Functionality =======================================================

print("functions syntax stable")  

print("Checking Main Post for signed of existing analysis")
for first_post in reddit.subreddit('REcountableFrame').new(limit=1):
    print(f"most recent most ============================ {first_post.title}")
    first_post_id = first_post.id
    for comment in first_post.comments.list():
        print(comment)
        if comment.author == "Frame-Counting-Bot":
            print(f"{comment} is shown to be from the bot itself")
            skip_first = True

if skip_first:
    print("par being set based on recent most")
    par = first_post_id
    



print(f"skip_first ============================================================ {skip_first}")
time.sleep(9)


    
print("Now Entering MAIN LOOP >>>")
#===================================================== MAIN LOOP ==============================================
while True:

    event_number += 1
    print(f"event_number =================================== {event_number}")
     
    subreddit_assist()


    
    print("resting event #1; please wait a minute")
    time.sleep(60)
    print("resting event #1 over")
                

    inbox_assist()

    print("checking emergency break variable")
    if em_break:
        print("now breaking loop")
        break

    print("resting event #2; please wait a minute")
    time.sleep(60)
    print("resting event #2 over")

print("Frame_Counting_Bot_v102 has shutdown")