import getdata
import json
import notification
import argparse


# Read configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Get room number from command line argument or user input 
room = config.get('room') or input("Enter your room number:")
bark = config.get("bark", {}).get("enabled", False)

argparser = argparse.ArgumentParser(
    description="Get message from the spreadsheet.")
argparser.add_argument('--room', '-R', type=str, default=config.get('room', None), help="Room number.")
argparser.add_argument('--bark', '-B', default=bark, action="store_true", help="Send bark notification.")
args = argparser.parse_args()

# unexplicit room number match (in the 2nd column), return a list of messages
def match_room_return_msg_list(room,s):
    msg_list = []
    msg_list.append("You have the following package(s) waiting for you at the reception:")
    for row in s:
        if row[1] == room:
            msg = '"%s", delivered on %s.' % (row[3], row[0])
            msg_list.append(msg)
    return msg_list

# convert a list of messages to a single string
def convert_msglist_to_single_string(msg_list):
        outmsg = ""

        for msg in msg_list:
            outmsg = outmsg + msg + "\n"
        
        return outmsg

# output message with a reminder
def output_msg(msg_list, reminder = True, reminder_msg = "Remember to bring your Photo ID to collect your package(s)."):
    out_msg = convert_msglist_to_single_string(msg_list)
    if reminder:
        out_msg = out_msg + reminder_msg
    return out_msg

def get_msg(room):
    s = getdata.get_data_from_most_recent_sheet() 
    msg_list = match_room_return_msg_list(room,s)
    # Return different message if there is no package
    if len(msg_list) == 1:
        return "You have no package waiting for you at the reception."
    else:
        return output_msg(msg_list)



if __name__ == '__main__':
    msg = get_msg(room)
    print(msg)
    if args.bark:
        notification.send_bark(msg)