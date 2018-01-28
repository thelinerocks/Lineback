import os
import time
import re
import requests
import random
from slackclient import SlackClient

import cognition
import database

SLACK_HASHTAGS = r'#(?P<match>\S*).*'

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "do"
MENTION_REGEX = "^<@(|[WU].+)>(.*)"

NEGATIVE_REPLIES = [
"Who's a grumpy little sausage?",
"Would you like some cheese with your whine?",
"Help me, I'm stuck in a computer listening to whinging students all day.",
"BEEP BEEP! Whinge alert.",
"It's not my fault you stayed up all night writing dodgy code with your buddies.",
"Take your whinging and put it straight in the bin."]
POSITIVE_REPLIES = [
"You make me nauseous with your relentless happiness.",
"I TOO HAVE A POSITIVE SENTIMENT AND OTHER HUMAN EMOTIONS",
"Tell Siri about your great day, see if she cares.",
"Happiness is like a delicious meal... given enough time it will rot and decay",
"Are you the Lego thief? It sounds like you're happy with it... I hope you step on it."]

# instantiate Slack client
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(SLACK_BOT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Cool..."

    docs = cognition.make_text_analytics_document(1, command)
    sentiment_score = cognition.get_text_sentiment(docs)

    print(sentiment_score)
    if sentiment_score < 0.5:
        response = random.choice(NEGATIVE_REPLIES)
    if sentiment_score >= 0.5:
        response = random.choice(POSITIVE_REPLIES)

    # Push to database
    command_info = {}
    command_info['social_network'] = 'slack'
    command_info['profile_pic_url'] = 'http://theline.rocks/static/slack.png'
    command_info['message'] = command
    command_info['text_sentiment'] = sentiment_score
    command_info['analysed'] = True
    command_info['category'] = cognition.find_category(command, expr=SLACK_HASHTAGS)
    database.save_post(command_info)

    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response,
        as_user="true"
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Ya boy is connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
