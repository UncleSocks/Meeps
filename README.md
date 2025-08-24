<img width="730" height="257" alt="image" src="https://github.com/user-attachments/assets/84868228-75c4-49b1-8e38-4f64c34b200f" />

# Meeps Security: Cybersecurity Awareness and Training Mini Horror Game

Meeps Security is a mini-game with horror elements designed to extend cybersecurity training and awareness by playing as an L1 Security Operation Center (SOC) analyst. Players handle incoming calls regarding cybersecurity incidents, evaluating and submitting the appropriate threat to the callers within the given service level agreement (SLA). The player must correctly resolve at least 80% of tickets to pass the assessment during the shift. 

## Prerequisites

Run `pip install -r requirements.txt` to install the tool's dependencies.

### Dependencies

MEEPS SECURITY is written in Python 3 using the `PyGame` and `PyGame GUI` libraries.

## Gameplay

The main menu has three buttons: START SHIFT, CREATE TICKETS, and LOG OFF. To play MEEPS SECURITY, select the "START SHIFT" button. This will take you to the main game loop, where you play as an L1 SOC analyst. 

MEEPS SECURITY also allows players to manage the tickets, including creating custom tickets by clicking the "MANAGE TICKET" button. At the time of writing, threat management is still under development.

<img width="797" height="650" alt="image" src="https://github.com/user-attachments/assets/6bc6d817-21ba-4287-bfc4-74b4a3ba1253" />



The "LOG OFF" button exits the game -- you can also click on the close window button.

### Starting Your Shift

When starting your shift, you will anticipate calls from various MEEPS SECURITY clients regarding cybersecurity incidents. 

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/8762a4d7-10e2-48c0-86f3-4bbc45fdcddc)

A pop-up window will be displayed when an incoming call must be answered within the specified SLA. Failure to answer within the SLA will deny you the opportunity for a possible score.

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/831045de-8828-40f7-b06c-862076ae6ca0)

After answering the call, MEEPS SECURITY will display the current caller's information, specifically their name, organization, email, and contact number, together with their cyber security concern (ticket). MEEPS SECURITY provides the players with a list of threats, a brief description of the threat, its indicators, and countermeasures. The player must analyze the ticket, select the appropriate threat (from the list), and submit it to the caller. The player will be granted a score when the correct threat is submitted. In addition, the players must be able to submit the appropriate threat within the allotted SLA for a score to be granted.

**Note:** More threats and scenarios will be added over time.

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/c651298a-4344-4456-81e1-2ac5e8048382)

After your shift, your performance will be evaluated. The players must have submitted at least 80% correct threats to pass the assessment. The shift report also provides the total number of tickets handled, any missed calls, and missed tickets.

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/66c959f0-5629-427d-a11c-6ed31a68a9ff)

Click the "END SHIFT" button to end the game. 


Currently, MEEPS SECURITY does not save your progress. It selects a random ticket from the SQLite database.


### Managing Tickets

MEEPS SECURITY also allows you to manage the tickets. Users can view, delete, or even create custom tickets to expand the game further. Select a ticket title to view its details. To delete a ticket, click the "-" button. To create a ticket, click the "+" button to take you to the ticket creation page.

**Note:** Be careful when deleting a ticket. Currently, it does not provide a confirmation mechanism.

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/da17fdf0-15d8-4917-8f17-c0c8da9741f8)

Enter the ticket title and description, then choose the threat (answer) relating to the ticket. Click the "CREATE TICKET" button to add the custom ticket. MEEP SECURITY automatically correlates the Guest account to all custom tickets.

**Note:** You can manually create new accounts and correlate them to a certain ticket.

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/6358106d-63f7-4106-b264-01f97c89a3ea)

A confirmation pop-up window will notify the player that the new ticket has been successfully inserted into the database.



