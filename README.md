<img width="853" height="292" alt="image-removebg-preview" src="https://github.com/user-attachments/assets/f9bb08ce-c469-462c-a6c7-9ebaca11dda8" />

# Meeps Security: Gamified Cybersecurity Training and Awareness Framework

**Meeps Security** is a gamified cybersecurity training and awareness framework. In the game, players handle incoming calls about cybersecurity incidents, analyze the situation, and submit the appropriate threat classification within the defined service level agreement (SLA). Towards the end of the shift, players must correctly resolve at least 80% of the tickets to pass their assessments.

The goal of the game is to help players become familiar with different types of cyber threats and to improve their analysis skills while also introducing key concepts commonly found in Security Operations Center (SOC) environments, such as SLAs and ticket management.


## How to Play Meeps Security?

The main menu features four buttons: **START SHIFT**, **MANAGE TICKETS**, **MANAGE ACCOUNTS**, and **THREAT DATABASE**. To start the game, select the **START SHIFT** button. This will take you to the main game loop, where you take on the role of an L1 SOC analyst.

The game also allows players to create or delete tickets, accounts (callers), and threats, adding depth and flexibility to the gameplay. The **LOG OFF** button exits the game.

![demo](https://github.com/user-attachments/assets/1a37e32a-dacc-4e6b-93b9-3f96d7926bc2)

## Starting Your Shift

When starting your shift, you will receive calls from various Meeps Security clients regarding cybersecurity incidents. A pop-up window will notify you of an incoming call, which must be answered within the specified SLA. Failing to answer within the SLA will cause you to miss the opportunity to earn a score for that ticket.

<img width="798" height="647" alt="image" src="https://github.com/user-attachments/assets/0d101923-25f6-4bff-baf7-a4d80c1c597d" />


After answering the call, the caller's information: name, organization, email, and contact number will be displayed, along with the details of their cybersecurity concern. A list of threats, their description, indicators, and countermeasures will also be provided. 

Your task as an analyst is to analyze the ticket, identify the correct threat, and submit it as a resolution to the caller. A score is awarded for each correctly classified threat.

**💡 Tip**: _It is therefore recommended that players review the **Threat Database** before starting a shift. Familiarity with the available threats will make it easier to classify the incidents accurately and submit them before the SLA expires._

<img width="798" height="653" alt="image" src="https://github.com/user-attachments/assets/7a6cb2e6-4cd5-4534-8614-07b9ae563dc9" />

At the end of your shift, your performance will be evaluated. To pass the assessment, you must correctly resolve at least 80% of tickets. The shift report will also display:
- Total number of tickets
- Tickets accurately resolved
- Number of missed calls
- Number of missed tickets

![image](https://github.com/UncleSocks/meeps-security-cybersecurity-awareness-and-training-game/assets/79778613/66c959f0-5629-427d-a11c-6ed31a68a9ff)


## Ticket, Account, and Threat Management

Meeps Security also provides players with the ability to manage tickets, accounts, and threats, allowing for a customizable and evolving gameplay experience. All user data, including images for accounts and threats, is stored in the `data` folder. 

<img width="796" height="649" alt="image" src="https://github.com/user-attachments/assets/0a1c7998-321b-4fd6-a422-99c67c94461a" />

All three management pages will have two buttons: `+` (Add) and `-` (Delete). These allow players to create or remove entries as needed. When adding a new entry, all fields must be completed before submission. 

<img width="797" height="645" alt="image" src="https://github.com/user-attachments/assets/d9a7d046-4ce1-4613-8d39-27c3ff0b26cd" />

⚠️ **Important:** Deleting an entry may also remove other data linked to it. For example:
- Deleting an account will also delete all tickets associated with that account.
- Deleting a threat will remove any tickets tied to that threat.

To prevent accidental data loss, a confirmation pop-up will always appear before final deletion. Note that the **Guest** account is protected and cannot be deleted.

## Releases

A base PE file is available on the release page. This version does not contain any ticket, account, or threat entries. This is useful for those who want to create Meeps Security from scratch with their own threat entry and their cybersecurity scenarios (tickets). 

**NOTE:** Make sure that the `data` directory is present together with the **meeps.exe** file, as this will hold the dynamic assets of the players. Images for the accounts and threats should be stored under the `accounts` and `threats` sub-folders, respectively. 


# Possible Future Improvements
- Create a web-based version
- Add save and resume capability
