#!/usr/bin/python
import os
import re
import xml.etree.ElementTree as ET
import csv
import json


# Open JSON dictionary of all cards
with open('Dictionary.json') as infile:    
    allcards = json.load(infile)

# CSV output
csvfile = open('stats.csv', 'w')
# Edit 'fieldnames' to change output values
# fieldnames = ["QuestName", "EnemyTotal", "EnemyThreatTotal", "EnemyAttackTotal", "EnemyDefenseTotal", "EnemyHealthTotal", "EnemyThreatAverage", "EnemyAttackAverage", "EnemyDefenseAverage", "EnemyHealthAverage", "LocationTotal", "LocationQuestPointsTotal", "LocationThreatTotal", "LocationThreatAverage", "LocationQuestPointsAverage"]
fieldnames = ["QuestName", "EnemyTotal", "EnemyThreatTotal", "EnemyAttackTotal", "EnemyDefenseTotal", "EnemyHealthTotal"]
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
writer.writeheader() # comment this if you don't want a header row

# Loop over quests
#directories = ['Easy','Quests','Nightmare', 'PoD', 'Campaign']
directories = ['Quests']
for directory in directories:
    for o8dfile in sorted(os.listdir(directory)):
        tree = ET.parse(directory+'/'+o8dfile)
        root = tree.getroot()
        stats = {
            "QuestName": "",
            "CardsTotal": 0,
            "EnemyTotal": 0,
            "EnemyThreatTotal": 0,
            "EnemyAttackTotal": 0,
            "EnemyDefenseTotal": 0,
            "EnemyHealthTotal": 0,
            "EnemyThreatAverage": 0,
            "EnemyAttackAverage": 0,
            "EnemyDefenseAverage": 0,
            "EnemyHealthAverage": 0,
            "LocationTotal": 0,
            "LocationQuestPointsTotal": 0,
            "LocationThreatTotal": 0,
            "ShadowTotal": 0,
            "ShadowProbability": 0
        }

        # Parse the quest name. Only works for normal quests - Needs adjustment for campaign
        stats["QuestName"] = o8dfile[10:-4]

        for card in root.getiterator('card'):
            OctgnID = card.get('id',0)
            Quantity = int(card.get('qty',0))
            cardObject = allcards.get(OctgnID,{});

            # Count all cards
            stats['CardsTotal'] = stats['CardsTotal'] + Quantity

            # Check and count shadow effects
            if 'Shadow' in cardObject:
                stats["ShadowTotal"] = stats["ShadowTotal"]  + Quantity

            # Enemies
            if (cardObject.get("Type","") == "Enemy"):
                stats["EnemyTotal"] = stats["EnemyTotal"] + Quantity
                # Calculate threat
                Threat = cardObject.get("Threat",0)
                if (Threat.isdigit()): 
                    Threat = int(Threat)
                else:  # in case Threat == 'X' or '-'
                    Threat = 0;                
                stats["EnemyThreatTotal"] = stats["EnemyThreatTotal"] + Threat*Quantity
                # Calculate Attack
                Attack = cardObject.get("Attack",0)
                if (Attack.isdigit()): 
                    Attack = int(Attack)
                else:  # in case Attack == 'X' or '-'
                    Attack = 0;                
                stats["EnemyAttackTotal"] = stats["EnemyAttackTotal"] + Attack*Quantity
                # Calculate Defense
                Defense = cardObject.get("Defense",0)
                if (Defense.isdigit()): 
                    Defense = int(Defense)
                else:  # in case Defense == 'X' or '-'
                    Defense = 0;                
                stats["EnemyDefenseTotal"] = stats["EnemyDefenseTotal"] + Defense*Quantity
                                # Calculate Health
                Health = cardObject.get("Health",0)
                if (Health.isdigit()): 
                    Health = int(Health)
                else:  # in case Health == 'X' or '-'
                    Health = 0;                
                stats["EnemyHealthTotal"] = stats["EnemyHealthTotal"] + Health*Quantity

            # Locations
            if (cardObject.get("Type","") == "Location"):
                stats["LocationTotal"] = stats["LocationTotal"] + Quantity
                # Calculate quest points
                QuestPoints = cardObject.get("Quest Points",0)
                if (QuestPoints.isdigit()): 
                    QuestPoints = int(QuestPoints)
                else:  # in case QP == 'X' or '-'
                    QuestPoints = 0;                    
                stats["LocationQuestPointsTotal"] = stats["LocationQuestPointsTotal"] + QuestPoints*Quantity
                # Calculate threat
                Threat = cardObject.get("Threat",0)
                if (Threat.isdigit()): 
                    Threat = int(Threat)
                else:  # in case Threat == 'X' or '-'
                    Threat = 0;                
                stats["LocationThreatTotal"] = stats["LocationThreatTotal"] + Threat*Quantity


        # Calculate averages
        stats["EnemyThreatAverage"] = float(stats["EnemyThreatTotal"])/stats["EnemyTotal"]
        stats["EnemyAttackAverage"] = float(stats["EnemyAttackTotal"])/stats["EnemyTotal"]
        stats["EnemyDefenseAverage"] = float(stats["EnemyDefenseTotal"])/stats["EnemyTotal"]
        stats["EnemyHealthAverage"] = float(stats["EnemyHealthTotal"])/stats["EnemyTotal"]
        stats["LocationQuestPointsAverage"] = float(stats["LocationQuestPointsTotal"])/stats["LocationTotal"]
        stats["LocationThreatAverage"] = float(stats["LocationThreatTotal"])/stats["LocationTotal"]
        stats["ShadowProbability"] = float(stats["ShadowTotal"])/stats["CardsTotal"]

        # Print to stout - uncomment this if you want console output
        # print o8dfile
        # print stats

        # Write row to csvfile
        writer.writerow(stats)





