<img width="796" height="263" alt="image" src="https://github.com/user-attachments/assets/524dc39d-25f8-4bf1-a9a7-7daa7532f729" />

# Meeps Security: Gamified Cybersecurity Training and Awareness Framework

Meeps Security is a mini-game with horror elements designed to extend cybersecurity training and awareness by playing as an L1 Security Operation Center (SOC) analyst. Players handle incoming calls regarding cybersecurity incidents, evaluating and submitting the appropriate threat to the callers within the given service level agreement (SLA). The player must correctly resolve at least 80% of tickets to pass the assessment during the shift. 


## How to Play?

The main menu has four buttons: START SHIFT, MANAGE TICKETS, MANAGE ACCOUNTS, and THREAT DATABASE. To start the game, select the "START SHIFT" button. This will take you to the main game loop, where you play as an L1 SOC analyst. 

The game also allows players to create or delete tickets, accounts (callers), and threats, further expanding the game. The "LOG OFF" button exits the game -- you can also click on the close window button.

![demo](https://github.com/user-attachments/assets/1a37e32a-dacc-4e6b-93b9-3f96d7926bc2)

## Starting Your Shift

When starting your shift, you will receive calls from various Meeps Security clients regarding cybersecurity incidents. A pop-up window will be displayed when an incoming call must be answered within the specified SLA. Failure to answer within the SLA will deny you the opportunity for a possible score.

<img width="798" height="647" alt="image" src="https://github.com/user-attachments/assets/0d101923-25f6-4bff-baf7-a4d80c1c597d" />

After answering the call, the caller's information, specifically their name, organization, email, and contact number, together with their cybersecurity concern, will be displayed. The Meeps security Responder provides players with a list of threats, a brief description of each threat, its indicators, and recommended countermeasures. The player must analyze the ticket, select the appropriate threat, and submit it to the caller. The player will be granted a score when the correct threat is submitted. In addition, the players must be able to submit the appropriate threat within the allotted SLA for a score to be granted.

**Note:** More threats and scenarios will be added over time.

<img width="798" height="653" alt="image" src="https://github.com/user-attachments/assets/7a6cb2e6-4cd5-4534-8614-07b9ae563dc9" />

After your shift, your performance will be evaluated. The players must have submitted at least 80% correct threats to pass the assessment. The shift report also provides the total number of tickets handled, any missed calls, and missed tickets. Click the "END SHIFT" button to end the game. 

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/66c959f0-5629-427d-a11c-6ed31a68a9ff)


## Ticket, Account, and Threat Management

Meeps Security allows players to manage the game's tickets, accounts, and threats. This user data, including the account and threat images, is stored in the `data` folder. 

<img width="796" height="649" alt="image" src="https://github.com/user-attachments/assets/0a1c7998-321b-4fd6-a422-99c67c94461a" />

All three management pages will have two buttons: `+` and `-`, enabling players to create or delete an entry, respectively. It is self-explanatory once the players visit these pages, but all fields must be filled out first before it can be submitted.

<img width="797" height="645" alt="image" src="https://github.com/user-attachments/assets/d9a7d046-4ce1-4613-8d39-27c3ff0b26cd" />

Deleting an entry can result in the deletion of those dependent on it. For example, when deleting an account or threat, all associated tickets will also be deleted, so be careful when performing the delete action. A confirmation pop-up window will be displayed when attempting to delete an entry. Note that the **Guest** account cannot be deleted.

## Releases

A base PE file is available on the release page. This version does not contain any ticket, account, or threat entries. This is useful for those who want to create Meeps Security from scratch with their own threat entry and their cybersecurity scenarios (tickets). 

**NOTE:** Make sure that the `data` directory is present together with the **meeps.exe** file, as this will hold the dynamic assets of the players. Images for the accounts and threats should be stored under the `accounts` and `threats` sub-folders, respectively. 


# Possible Future Improvements
- Create a web-based version
- Add save and resume capability
