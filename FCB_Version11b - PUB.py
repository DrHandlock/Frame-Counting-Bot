
print("Frame_Counter_Bot_v11 booting up ...")

import praw
from moviepy.editor import VideoFileClip, AudioFileClip
from praw.exceptions import RedditAPIException
from praw.exceptions import ClientException
import time
import numpy as np
import re





# Variables/Lists
par = "Post Analysis Restrainment" # this will be used to prevent analysis of already alalized posts
rar = "Reply Analysis Restrainment" 
em_break = False 
skip_first = False
event_number = 0

ID_list = []
decibel_list = []
resol_list = []
ratio_list = []
pixel_list = []






# Changeable Variables for testing purposes

username_var = ""
subreddit_var = ""
assisting_var = ""
assisting_sub = ""





# Authentication


reddit = praw.Reddit(
    client_id=(''),
    client_secret=(''),
    user_agent=(''),
    username=(''),
    password=('')
)


print("PRAW authenticated")





#   Functions


def list_record(): # this is so that if the loop ever ends, we still have the recorded list
    global ID_list
    global decibel_list
    global resol_list
    global ratio_list
    global pixel_list

    lists = [ID_list, decibel_list, resol_list, ratio_list, pixel_list]
    names_of_lists = ["ID_list", 'decibel_list', 'resol_list', 'ratio_list', 'pixel_list']

    testing_var = "TESTING"
    
    print("======================= RECORDED LIST ========================")

    for list_object in list(lists):

        list_index = lists.index(list_object)

        response = str(names_of_lists[list_index]) + ' = ['

        for item in list(list_object):

            if list_object.index(item) == len(list_object) - 1:
                response += f"{item}]"

            else:
                response += f"{item}, "

        print(response)

    print("======================== END RECORDED =====================")
        
        
        
"""     
def bonus_recall(command, post_id):
    global ID_list
    global decibel_list
    global resol_list
    global ratio_list
    global pixel_list
    
    print("Activating bonus_recall...")

    if post_id in ID_list:
        print('id found and usable')

        index = ID_list.index(post_id)

        if command == "!!decibel":
            print('fetching decibel information...')
            output = f"the average decibel rate in this post is {decibel_list[index]}"

        elif command == "!!resolution":
            print('fetching resolution information...')
            output = f"the resolution of this video is {resol_list[index]}"

        elif command == "!!ratio":
            print('fetching aspect ratio information...')
            output = f"the ratio of this video put in whole number terms is {ratio_list[index]}"

        elif command == "!!pixel":
            print('fetching pixel information...')
            pixel_factors = pixel_list[index].split('-') # one frame - all frames
            output = f"for a single frame there would be {pixel_factors[0]}, but for the entire material there would be {pixel_factors[1]}"

        else:
            print('command denied...')
            output = f"This has been read as a command, but there is no command there is no command in out catalog called: {command}"

    
    else:
        print('id not found')
        output = "This post either had it's information removed due to it exceeding the it's 2 day life-span or this post could have not been processed"

    output += f"\n\n^(I am a bot, and this response is automated) \n \n ^(Warning: This bot is still in early development and bugs may occure, if there are any bugs please contact: u/)^(DrHandlock) \n \n ^(FrameCountingBotv1.1-Prop-Of-REcountableFrame-EN: {event_number})"

    print('now sending output message...')
    
    command.reply(output)
"""





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
        





def frame_counting(video_path, promotion, post_id, support):
    global event_number
    global decibel_list
    global resol_list
    global ratio_list
    global pixel_list
    global AR_list

    
    result = ""

    print("frame_counting active...")


    print('video attaching to analysis device')
    video = VideoFileClip(video_path)

    if video.duration > 900: # 15 minutes

        video_object = video.subclip(0, 900)
        estimate = True

    else:

        video_object = video
        estimate = False





    
    if estimate:
        result += "due to your request exceeding our 15 minute recommendation, your calulation was put in HEAVY DUTY mode, which means it may rely on a estimate"
    
    print('getting fps')
    FPS = video_object.fps

    print('getting total frames')
    total_frames = int(FPS * video.duration)

    print("...now creating resolution")
    
    

    
    # basically this will advertise the new subreddit for this bot
    

    




    # ================== Bonus Information Finding ======================

    audio_info = "No audio track"
    average_decibel = 0
    if video.audio:
        print("Audio detected...")
        audio = video.audio
        
        try:
            audio_array = audio.to_soundarray(fps=44100)
            rms = np.sqrt(np.mean(audio_array**2, axis=0))
            decibel = 20 * np.log10(rms)

            if len(decibel) > 1:
                print("Stereo audio detected")
                average_decibel = np.mean(decibel)
            else:
                print("Mono audio detected")
                average_decibel = decibel[0]
            
            audio_info = f"Average Decibel Level: {average_decibel:.2f} dB"
        
        except Exception as e:
            print(f"Error processing audio: {e}")
            audio_info = "Error processing audio"
    

    resolution = f"{video.w}x{video.h}"

    pixel_frame = video.w * video.h

    total_pixels = pixel_frame * total_frames

    # ratio finding
    ratio_mult = 0
    start_ratio = video.w / video.h
    while True:
        
        ratio_mult += 1


        
        ratio_result = ratio_mult * start_ratio

        if int(ratio_result) == float(ratio_result):
            break


    ratio = f"{ratio_result}:{ratio_mult}"

    # APPENDING BONUS INFORMATION
    print("NOW ENTERING APPENDING MODE...")

    ID_list.append(post_id)
    ratio_list.append(ratio)
    
    resol_list.append(resolution)
    pixel_list.append(f"{pixel_frame}-{total_pixels}")




    result += f"This video  contains {total_frames} frames at (Rounded) {int(FPS)} frames per second. BONUS INFORMATION: It is kept in a resolution of {resolution} otherwise {ratio} in ratio terms, and I don't want to steal pixel-counter-bot's job there is a total of {total_pixels} due to a single frame having {pixel_frame} pixels in it." 

    if promotion:
        result += " \n \n Check out r/REcountableFrame for a subreddit that is for people who want to count frames and this bot"
    
    
    result += f"\n\n^(I am a bot, and this response is automated) \n \n ^(Warning: This bot is still in early development and bugs may occure, if there are any bugs please contact: u/)^(DrHandlock) \n \n ^(FrameCountingBotv1.1-Prop-Of-REcountableFrame-EN: {event_number})"

    if support:
        f"{total_frames}_{total_pixels}"
    else:
        return result



#======================================================================================
def subreddit_assist():
    print("subreddit_assist was called")
    global event_number
    global par
    global subreddit_var


    #local variable reset (lvr)
    
    post_object = "lvr"
    countable = False
    
    
    for subr_post in reddit.subreddit(subreddit_var).new(limit=1):
        
        print(f"newest post being checked... {subr_post.title} ; {subr_post.id}")
        
        post_flair = subr_post.link_flair_text

        

        
        if subr_post.id != par and post_flair == "Bot Usage":
            print(f"Criteria Met: \n \n ID({subr_post.id}) doesn't match PAR({par})... Continuing...")


            # NORMAL POSTING
            
            if subr_post.is_video or subr_post.url.endswith(('.gif', '.gifv')):

                
                print("video/GIF contained and now settting post_object as this post, as well as setting booleen variable")

                post_object = subr_post

                countable = True


            # CROSS POSTING
            
            elif hasattr(subr_post, 'crosspost_parent_list'):
                print("crosspost contained")
                
                original_id = subr_post.crosspost_parent.split('_')[1] # this is how we get the original ID
                
                print(f"original_id: {original_id}") 
                og_sub = reddit.submission(id=original_id)

                if og_sub.is_video or og_sub.url.endswith(('.gif', '.gifv')):  # this is for the CROSS POSTING

                    post_object = og_sub

                    countable = True


    
    # Part 2


        
        
    if countable:
        
        print("Now Entering Part 2 of Subreddit_Assist")
                
        try:
                    
            print('trying normal URL capture method')
            video_url = post_object.media['reddit_video']['fallback_url']

        except TypeError:

            print('swapping to TypeError alternate')
            video_url = post_object.url  # For GIF or other media types


         
        response = frame_counting(video_url, False, post_object, False)

        
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




    print('leaving subreddit_assist')

                

               

#To my current knowledge this also finsihed
def inbox_assist():
    global event_number
    global em_break
    global username_var


    # local variable reset

    countable = False



    
    print("inbox_assist called")
    
    unread_messages = list(reddit.inbox.unread(limit=None))
    print(f"Number of unread messages: {len(unread_messages)}")

    print("======= \n messages include:")
    for item in unread_messages:
        print(item.body)


    print("======")
    for message in reddit.inbox.unread(limit=None):
        print(f"unread message detected within INBOX...   {message}")
        
        if f"u/{username_var}" in message.body.lower() or '!!' in message.body.lower():
            print("username/!! detected")

            # you see we reuse this strand of code to also access the post_id for the bonus information
            if f"u/{username_var}" in message.body.lower():
                request_type = 'frame'

            elif '!!' in message.body.lower():
                request_type = 'bonus_information'


                

            try:
            
                comment = reddit.comment(message.id)
                submission = comment.submission





                
                if submission.is_video or submission.url.endswith(('.gif', '.gifv')):
                    print("submission from inbox message_origin is video")

                    countable = True


                    
                    post_object = submission


                # ======== CROSS POST ========
                elif hasattr(submission, 'crosspost_parent_list'):
                    
                    original_id = submission.crosspost_parent.split('_')[1] # this is how we get the original ID
                    print(f"original_id: {original_id}") 
                    og_sub = reddit.submission(id=original_id)

                    if og_sub.is_video or og_sub.url.endswith(('.gif', '.gifv')):
                    
                        countable = True

                    
                        post_object = og_sub


                
                else:
                    print("This post can't be accepted")
                    log_submission_type(submission)
                    message.mark_read()
                    message.reply(f"Sorry this post could not accepted, it you believe this an error, please try again. (This problem may occur if your requested post is a GIF) \n \n ^({event_number})")

                    


                if request_type == 'frame' and countable:
                    print("inbox request is countable")


                    try:
                    
                        print('trying normal URL capture method')
                        video_url = post_object.media['reddit_video']['fallback_url']

                    except TypeError:

                        print('swapping to TypeError alternate')
                        video_url = post_object.url  # For GIF or other media types

                    

                    try:
                        print("now trying m.reply(f_c(v_u))")
                        message.reply(frame_counting(subm_url, True, post_object, False))
                        print("unread message solved")
                        message.mark_read()

                
                    except RedditAPIException as RAE:
                        print("RAE CALLED within inbox_assist")
                        for subexception in RAE.items:
                            if subexception.error_type == 'RATELIMIT':
                                wait_time = int(''.join(filter(str.isdigit, subexception.message)))
                                print(f"Rate limit exceeded. Sleeping for {wait_time} minutes.")
                                time.sleep(float(wait_time) * 60)
            
                #elif request_type == 'bonus_information':
                    #bonus_recall(message.body.lower, post_object)
                    #message.mark_read()
                

            

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


        

def bot_assist(): # For supporting fellow bot: Pixel-Counter-Bot incorrect estimate
    global rar


    
    countable = False
    for new_post in reddit.subreddit(assisting_sub).new(limit=1):
        for comment in first_post.comments.list():
            print(comment)
            if comment.author == assisting_var and comment != rar:
                print("Pixel-Counter-Bot comment found")
                pcb_response = comment.body.lower() # the PCB stands for Pixel-Counter-Bot
                pcb_response = pcb_response.replace(',','') #removes commas
                if "pixels per frame and an estimated" in pcb_response:
                    pcb_numbers = pcb_response.re.findall(r'\d+', pcb_response)
                    
                    pcb_frames = pcb_numbers[3]

                    try:
            
                        comment = reddit.comment(message.id)
                        submission = comment.submission





                
                        if submission.is_video or submission.url.endswith(('.gif', '.gifv')):
                            print("submission from inbox message_origin is video")

                            countable = True


                    
                            post_object = submission


                        # ======== CROSS POST ========
                        elif hasattr(submission, 'crosspost_parent_list'):
                    
                            original_id = submission.crosspost_parent.split('_')[1] # this is how we get the original ID
                            print(f"original_id: {original_id}") 
                            og_sub = reddit.submission(id=original_id)

                            if og_sub.is_video or og_sub.url.endswith(('.gif', '.gifv')):
                    
                                countable = True


                                post_object = og_sub



                
                            try:
                    
                                print('trying normal URL capture method')
                                video_url = post_object.media['reddit_video']['fallback_url']

                            except TypeError:

                                print('swapping to TypeError alternate')
                                video_url = post_object.url  # For GIF or other media types
                    
                        if countable:
                
                            fcb_frame = frame_counting(video_url, False, post_object, False)
                            fcb_answer = fcb_frame.split('_')
                            corrected_frame = fcb_answer[0]
                            corrected_pixel = fcb_answer[1]

                            correction = f"Correction: There is actually {corrected_frame}, and thus there is acutally {corrected_pixel}. \n \n ^(I am bot and this response is automated)"

                            if pcb_frame != pcb_frames:
                                print("sending correction")
                                comment.reply(correction)




                                
    




# ========================================= Entering Functionality =======================================================

print("functions syntax stable")  

print("Checking Main Post for signed of existing analysis")
for first_post in reddit.subreddit(subreddit_var).new(limit=1):
    print(f"most recent most ============================ {first_post.title}")
    first_post_id = first_post.id
    for comment in first_post.comments.list():
        print(comment)
        if comment.author == username_var:
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
    #time.sleep(60)
    print("resting event #1 over")
                

    inbox_assist()

    print("checking emergency break variable")
    if em_break:
        print("now breaking loop")
        break

    print("resting event #2; please wait a minute")
    time.sleep(60)
    print("resting event #2 over")



    #list_record()





print("Frame_Counting_Bot_v102 has shutdown")