import openai
import os
from dotenv import load_dotenv
class OpenAIClient:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls.client = openai.OpenAI(api_key=api_key)
        return cls._instance
    def ai_processor(self, prompt):
        system_prompt = '''
        I have game analysis data that includes team performances and key events:

Team A: '[Insert team A's analysis text here]'
Team B: '[Insert team B's analysis text here]'
Please assign numerical scores to each team's performance based on these descriptions. Generate scores for:

Team morale (on a scale of 1 to 10)
Offensive efficiency (on a scale of 1 to 10)
Defensive performance (on a scale of 1 to 10)
Key player impact (on a scale of 1 to 10 for each player mentioned)
Provide the results in this structured format:

json
Copy code
{
  "Team A": {
    "team_morale": ...,
    "offensive_efficiency": ...,
    "defensive_performance": ...,
    "player_impact": {
      "Player A": ...,
      "Player B": ...
    }
  },
  "Team B": {
    "team_morale": ...,
    "offensive_efficiency": ...,
    "defensive_performance": ...,
    "player_impact": {
      "Player C": ...,
      "Player D": ...
    }
  }
}
        '''
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()

def main():
    client = OpenAIClient()
    prompt = '''
    {
  "teams": ["New Orleans Saints", "Philadelphia Eagles"],
  "score": {
    "New Orleans Saints": 0,
    "Philadelphia Eagles": 0
  },
  "events": [
    {
      "type": "fumble_recovery",
      "player": "Willie Gay",
      "team": "New Orleans Saints",
      "quarter": 1,
      "half": "first"
    },
    {
      "type": "tackle",
      "player": "Chase Young (99)",
      "team": "New Orleans Saints",
      "player_target": "Saquon Barkley (26)",
      "team_target": "Philadelphia Eagles",
      "quarter": 1,
      "half": "first"
    }
  ],
  "analysis": {
    "New Orleans Saints_performance": "Defensive players Willie Gay and Chase Young (99) made significant impacts in the first half with a fumble recovery and a tackle on Saquon Barkley, respectively. These plays showcased the Saints' determination to maintain control of the game.",
    "Philadelphia Eagles_performance": "Despite having a talented running back like Saquon Barkley, the Eagles struggled in the first half, failing to capitalize on drives due to key defensive stops by the Saints.",
    "key_moments": "The fumble recovery and tackle on Saquon Barkley were game-defining moments that halted potential scoring opportunities for the Eagles, giving the Saints a significant advantage in momentum."
  }
}
```

In this analysis, I have extracted teams, players, coaches, and events dynamically without relying on hardcoded assumptions. The key event extraction focuses on game-critical events such as fumble recovery and tackle that directly impacted the score or momentum. The sentiment & performance analysis highlights the defensive prowess of the New Orleans Saints in the first half, while the Philadelphia Eagles struggled offensively. The contextual understanding captures the critical moments that favored the New Orleans Saints over the Philadelphia Eagles. The game summarization includes major moments and key performances, a focus on game-defining events and game flow, and a breakdown of each team's performance and shifts in momentum. Finally, the analysis is presented in a consistent JSON format for easy parsing and storage.  {
      "teams": ["Philadelphia Eagles", "New Orleans Saints"],
      "score": {"Philadelphia Eagles": 31, "New Orleans Saints": 21},
      "events": [
          {
              "type": "touchdown",
              "player": "Nakobe Dean (17)",
              "team": "Philadelphia Eagles",
              "quarter": 4
          },
          {
              "type": "incomplete_pass",
              "player": "Johnny Wilson (89)",
              "team": "Philadelphia Eagles",
              "quarter": 2,
              "defender": "Alontae Taylor (1)"
          }
      ],
      "analysis": {
          "philadelphia_eagles_performance": "The Philadelphia Eagles showcased a strong performance, scoring the winning touchdown in the fourth quarter by Nakobe Dean. However, they had a drop from Johnny Wilson that could have extended their lead in the second half.",
          "new_orleans_saints_performance": "Despite a valiant effort, the New Orleans Saints struggled with key plays, including an incomplete pass defended by Alontae Taylor. However, they showcased resilience and managed to keep the game close until the end.",
          "key_moments": "Key moments included the Eagles' touchdown in the fourth quarter that sealed the victory, and the incomplete pass by the Eagles' Johnny Wilson in the second half."
      }
  }  Based on the provided articles and images, here is a summary of the NFL game between the Philadelphia Eagles and the New Orleans Saints on September 22, 2024:

```json
{
 "teams": ["Philadelphia Eagles", "New Orleans Saints"],
 "score": {
   "Philadelphia Eagles": 17,
   "New Orleans Saints": 24
 },
 "events": [
   {
     "type": "touchdown",
     "player": "Jalen Reagor (Eagles Wide Receiver)",
     "team": "Philadelphia Eagles",
     "quarter": 1,
     "time": "12:05"
   },
   {
     "type": "touchdown",
     "player": "Michael Thomas (Saints Wide Receiver)",
     "team": "New Orleans Saints",
     "quarter": 2,
     "time": "08:43"
   },
   {
     "type": "interception",
     "player": "Marshon Lattimore (Saints Cornerback)",
     "team": "New Orleans Saints",
     "quarter": 2,
     "time": "05:17"
   },
   {
     "type": "penalty",
     "player": "Andrus Peat (Saints Offensive Lineman)",
     "team": "New Orleans Saints",
     "quarter": 3,
     "time": "09:12"
   },
   {
     "type": "touchdown",
     "player": "Jalen Hurts (Eagles Quarterback)",
     "team": "Philadelphia Eagles",
     "quarter": 4,
     "time": "13:05"
   }
 ],
 "analysis": {
   "philadelphia_eagles_performance": "The Eagles got off to a good start with a touchdown by Jalen Reagor in the first quarter. However, their offense struggled for most of the game until Jalen Hurts managed to score another touchdown late in the fourth quarter. Defensively, they had some trouble containing the Saints' passing attack.",
   "new_orleans_saints_performance": "The Saints responded to the Eagles' initial touchdown with a score by Michael Thomas. Their defense came up big throughout the game, including an interception by Marshon Lattimore and a crucial penalty on Andrus Peat that stalled an Eagles drive in the third quarter.",
   "key_moments": "The Saints' touchdown in the first quarter responded to the Eagles' initial score and set the tone for the game. The interception by Marshon Lattimore in the second quarter and the penalty on Andrus Peat in the third quarter were key turning points that favored the Saints."
 }
}
```
In this game, the New Orleans Saints came out victorious with a score of 24-17 over the Philadelphia Eagles. The Saints' defense played a crucial role in limiting the Eagles' offense and capitalizing on key moments such as an interception by Marshon Lattimore and a penalty on Andrus Peat. Offensively, the Saints scored two touchdowns, one by Michael Thomas and another by their quarterback (unspecified). The Eagles managed to score once in each half but struggled offensively for much of the game.  Based on the provided text, here is the analysis:

{
  "teams": ["New Orleans Saints", "Philadelphia Eagles"],
  "score": {"New Orleans Saints": 17, "Philadelphia Eagles": 14},
  "events": [
    {
      "type": "sack",
      "player": "Bryan Bresee (90)",
      "team": "New Orleans Saints",
      "quarter": "second half"
    },
    {
      "type": "reception",
      "player": "Chris Olave (12)",
      "team": "New Orleans Saints",
      "quarter": "second half"
    }
  ],
  "analysis": {
    "New_Orleans_Saints_performance": "Defensive tackle Bryan Bresee made a crucial play with a sack on Eagles' quarterback Jalen Hurts, highlighting the Saints' defensive prowess and disrupting Philadelphia's offense. Wide receiver Chris Olave showcased his agility by catching a pass amidst tight coverage from Quinyon Mitchell of the Eagles. These plays contributed to the Saints' victory.",
    "Philadelphia_Eagles_performance": "The Eagles demonstrated resilience in the face of adversity, managing to stay within striking distance despite the Saints' strong defensive effort and key plays. The team will need to focus on improving their offensive execution to capitalize on scoring opportunities.",
    "key_moments": "Bresee's sack and Olave's reception were game-defining moments that ultimately determined the outcome in favor of the Saints."
  }
}  {
     "teams": ["Philadelphia Eagles", "New Orleans Saints"],
     "score": {"Philadelphia Eagles": 14, "New Orleans Saints": 20},
     "events": [
         {
             "type": "punt_return",
             "player": "Jordan Howden (31)",
             "team": "New Orleans Saints",
             "quarter": 2,
             "details": "Blocked punt by New Orleans Saints"
         },
         {
             "type": "tackle",
             "player": "Gerald Herbert (not a player)", // This is actually the photographer who took the picture
             "team": "Philadelphia Eagles defenders",
             "quarter": "2nd half"
         },
         {
             "type": "punt_stop",
             "player": "J.T. Gray (48) and Payton Turner (98)",
             "team": "New Orleans Saints",
             "quarter": "2nd half"
         }
     ],
     "analysis": {
         "philadelphia_eagles_performance": "The Eagles had a standout blocked punt return by Jordan Howden, but struggled in the second half on defense due to a series of missed tackles, including one by Gerald Herbert who is actually a photographer and not a player.",
         "new_orleans_saints_performance": "The Saints successfully blocked a punt and made key stops on special teams, demonstrating their ability to adapt in critical moments. However, they relied heavily on defense and may need to work on offensive productivity for future games.",
         "key_moments": "The blocked punt return by Jordan Howden shifted momentum towards the Saints, ultimately leading to a win. The missed tackles on special teams by the Eagles in the second half proved costly."
     }
 }  {
   "teams": ["Philadelphia Eagles", "New Orleans Saints"],
   "score": {"Philadelphia Eagles": 7, "New Orleans Saints": 0},
   "events": [
      {
         "type": "touchdown",
         "player": "Saquon Barkley (26)",
         "team": "Philadelphia Eagles",
         "quarter": 3
      }
   ],
   "analysis": {
      "philadelphia_eagles_performance": "The Philadelphia Eagles demonstrated a strong ground game, with Saquon Barkley scoring a decisive touchdown in the third quarter. This momentum-shifting play significantly boosted the Eagles' chances of winning.",
      "new_orleans_saints_performance": "Despite a strong defensive effort, the Saints struggled offensively, failing to score any points. The defense was able to contain Barkley for most of the game, but ultimately couldn't stop him from scoring the touchdown that sealed the win for the Eagles.",
      "key_moments": "The key moment in this game was Saquon Barkley's 65-yard touchdown run in the third quarter. This play changed the momentum of the game and helped the Eagles secure a victory."
   }
}  {
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 21, "New Orleans Saints": 17},
  "events": [
    {
      "type": "touchdown",
      "player": "Saquon Barkley",
      "team": "Philadelphia Eagles",
      "quarter": 3
    },
    {
      "type": "reception_td",
      "player": "Alvin Kamara",
      "team": "New Orleans Saints",
      "quarter": 4
    }
  ],
  "analysis": {
    "Philadelphia_Eagles_performance": "The Eagles dominated the second half, with Saquon Barkley's 65-yard touchdown run being a pivotal moment. The team showcased excellent ball control and capitalized on opportunities.",
    "New_Orleans_Saints_performance": "The Saints struggled in the third quarter but rallied back in the fourth, scoring a touchdown with Alvin Kamara's reception to narrow the gap. However, they were unable to maintain momentum in the final minutes.",
    "key_moments": "Saquon Barkley's touchdown and Alvin Kamara's reception played significant roles in the game's outcome, demonstrating the importance of capitalizing on opportunities and maintaining momentum."
  }
}  Based on the provided text, here is the analysis in JSON format:

```json
{
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 21, "New Orleans Saints": 24},
  "events": [
    {
      "type": "touchdown",
      "player": "Chris Olave (12)",
      "team": "New Orleans Saints",
      "quarter": 2
    },
    {
      "type": "defensive_play",
      "player": "Darius Slay Jr.",
      "team": "Philadelphia Eagles",
      "quarter": 2
    }
  ],
  "analysis": {
    "Philadelphia_Eagles_performance": "Philadelphia Eagles showed a strong defensive performance, particularly in the second quarter where Darius Slay Jr. broke up a pass, but struggled offensively, allowing the Saints to take a lead.",
    "New_Orleans_Saints_performance": "The New Orleans Saints demonstrated a potent offensive game with Chris Olave scoring a touchdown in the second quarter. However, they also had to deal with a strong defensive effort from the Eagles in the same quarter which momentarily halted their momentum.",
    "key_moments": "The key moments of the game were the New Orleans Saints' touchdown and Philadelphia Eagles' defensive play in the second quarter. These events significantly impacted the game flow, with the Saints taking a lead after the touchdown and the Eagles attempting to regain momentum following their defensive stand."
  }
}
```

In this analysis, we have identified the teams (Philadelphia Eagles and New Orleans Saints), extracted game-critical events such as touchdowns and defensive plays, provided details about the players involved, and summarized the performance of each team. We also highlighted key moments that had a significant impact on the final outcome of the game. The information is concise, relevant, and structured in a consistent JSON format for easy parsing and storage.  {
   "teams": ["New Orleans Saints", "Philadelphia Eagles"],
   "score": {"New Orleans Saints": 14, "Philadelphia Eagles": 21},
   "events": [
      {
         "type": "catch",
         "player": "Chris Olave",
         "team": "New Orleans Saints",
         "quarter": 2
      },
      {
         "type": "interception",
         "player": "Kelee Ringo",
         "team": "Philadelphia Eagles",
         "quarter": 2
      },
      {
         "type": "pass",
         "player": "Jalen Hurts",
         "team": "Philadelphia Eagles",
         "quarter": 2
      }
   ],
   "analysis": {
      "new_orleans_saints_performance": "New Orleans Saints struggled offensively, with Chris Olave's catch being the only touchdown. The team's defense showed promising signs but couldn't prevent Philadelphia from scoring in the second half.",
      "philadelphia_eagles_performance": "Philadelphia Eagles capitalized on their opportunities, scoring 21 points. Jalen Hurts had a decent passing game and Kelee Ringo made a crucial interception to shift momentum towards the Eagles.",
      "key_moments": "The interception by Kelee Ringo in the second quarter was pivotal as it halted New Orleans' scoring drive, allowing Philadelphia to take control of the game."
   }
}  {
    "teams": ["New Orleans Saints", "Philadelphia Eagles"],
    "score": {"New Orleans Saints": X, "Philadelphia Eagles": Y},
    "events": [
        {
            "type": "scramble",
            "player": "Derek Carr",
            "team": "New Orleans Saints",
            "quarter": 2
        },
        {
            "type": "two-point conversion",
            "player": "Saquon Barkley",
            "team": "Philadelphia Eagles",
            "quarter": 2
        }
    ],
    "analysis": {
        "New Orleans Saints_performance": "Derek Carr showcased a mobile quarterback performance with a notable scramble in the second half. However, the Saints struggled offensively and failed to convert this play into points.",
        "Philadelphia Eagles_performance": "Saquon Barkley's two-point conversion was a pivotal moment that helped the Eagles maintain momentum in the second half, eventually leading to a narrow victory.",
        "key_moments": "The scramble by Derek Carr and Saquon Barkley's two-point conversion were game-defining moments, as they each impacted their respective teams' performance and overall game flow."
    }
}  {
   "teams": ["Philadelphia Eagles", "New Orleans Saints"],
   "score": {"Philadelphia Eagles": 24, "New Orleans Saints": 17},
   "events": [
      {
         "type": "interception",
         "player": "Reed Blankenship (32)",
         "team": "Philadelphia Eagles",
         "quarter": 4
      }
   ],
   "analysis": {
      "team_A_performance": "The Philadelphia Eagles demonstrated a strong defensive performance, particularly in the fourth quarter when Reed Blankenship intercepted the ball on the Saints' final drive, securing their victory. The Eagles offense also performed well, scoring 24 points and maintaining momentum throughout the game.",
      "team_B_performance": "The New Orleans Saints put up a good fight but struggled defensively in the fourth quarter. Dennis Allen's team managed 17 points but could not hold off the Eagles when it mattered most. Notable offensive performances include...",
      "key_moments": "The critical moment of the game was Reed Blankenship's interception, effectively ending the Saints' comeback attempt and securing a 24-17 victory for the Eagles."
   }
}  Based on the provided textual content, here is the analysis:

```json
{
 "teams": ["Philadelphia Eagles", "New Orleans Saints"],
 "score": {"Philadelphia Eagles": 30, "New Orleans Saints": 24},
 "events": [
 {
 "type": "touchdown",
 "player": "Dallas Goedert (88)",
 "team": "Philadelphia Eagles",
 "quarter": 1
 },
 {
 "type": "interception",
 "player": "Player not mentioned",
 "team": "New Orleans Saints",
 "quarter": 2
 },
 {
 "type": "penalty",
 "player": "Player Z (not specified)",
 "team": "New Orleans Saints",
 "quarter": 3
 }
 ],
 "analysis": {
 "philadelphia_eagles_performance": "The Philadelphia Eagles showcased a strong performance, with tight end Dallas Goedert scoring the first touchdown of the game in Q1. The team maintained momentum throughout the match, demonstrating impressive passing and running plays.",
 "new_orleans_saints_performance": "Despite a valiant effort, the New Orleans Saints struggled to maintain consistency. A key turning point was an unspecified interception in Q2 that temporarily disrupted their offensive flow. A penalty in Q3 further hampered their chances of securing a victory.",
 "key_moments": "The crucial moments of the game were Dallas Goedert's touchdown and the interception (unspecified player, Q2), which significantly impacted the game flow by shifting momentum towards the Philadelphia Eagles."
 }
}
```  {
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 28, "New Orleans Saints": 14},
  "events": [
    {
      "type": "win",
      "player": null,
      "team": "Philadelphia Eagles",
      "quarter": 4
    },
    {
      "type": "touchdown",
      "player": "Jalen Hurts",
      "team": "Philadelphia Eagles",
      "quarter": 1
    },
    {
      "type": "interception",
      "player": null,
      "team": "New Orleans Saints",
      "quarter": 2
    }
  ],
  "analysis": {
    "team_Eagles_performance": "The Philadelphia Eagles demonstrated a strong offensive performance with quarterback Jalen Hurts leading the team to a touchdown in the first quarter. The team's defense also showcased resilience, holding the Saints scoreless for three quarters, ultimately securing the win.",
    "team_Saints_performance": "The New Orleans Saints struggled offensively, failing to score until late in the fourth quarter. A key turning point was an interception in the second quarter that prevented the Saints from mounting a significant challenge.",
    "key_moments": "The game-defining moments were the Eagles' touchdown in the first quarter and the Saints' inability to score until late in the fourth. These critical events significantly impacted the overall game flow, with the Eagles dominating for most of the game."
  }
}  Here is the analysis based on the provided text:

```json
{
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 24, "New Orleans Saints": 21},
  "events": [
    {
      "type": "interception",
      "player": "Not specified (Interceptor from Philadelphia Eagles)",
      "team": "Philadelphia Eagles",
      "quarter": 4
    }
  ],
  "analysis": {
    "philadelphia_eagles_performance": "The Philadelphia Eagles secured a crucial interception in the fourth quarter, which halted the Saints' comeback attempt and ultimately sealed the win for them.",
    "new_orleans_saints_performance": "Despite a valiant effort, the New Orleans Saints were unable to score in their final drive, losing the game by 3 points.",
    "key_moments": "The interception in the fourth quarter was the defining moment of the game, shifting the momentum towards the Philadelphia Eagles and resulting in their victory."
  }
}
```

In this analysis:
- The teams involved are the Philadelphia Eagles and the New Orleans Saints.
- The score at the end of the game is 24 for the Philadelphia Eagles and 21 for the New Orleans Saints.
- The critical event that impacted the game's flow was an interception made by a player from the Philadelphia Eagles in the fourth quarter, which prevented the New Orleans Saints from scoring and ultimately led to their defeat.
- The analysis focuses on the key performance of the Philadelphia Eagles for securing the win with their interception and the unsuccessful final drive by the New Orleans Saints that cost them the game.
- The analysis also highlights the fourth quarter as the defining moment of the game, where the momentum shifted towards the Philadelphia Eagles.  Based on the provided text, here is the analysis:

{
 "teams": ["Philadelphia Eagles", "New Orleans Saints"],
 "score": {"Philadelphia Eagles": 0, "New Orleans Saints": 0},
 "events": [],
 "analysis": {
   "philadelphia_eagles_performance": "The Philadelphia Eagles started the game strong with solid punting from Braden Mann in the first half. However, their offense struggled to find a rhythm, resulting in no points on the board.",
   "new_orleans_saints_performance": "The New Orleans Saints mirrored the Eagles' performance, failing to score any points as well. Both teams seemed evenly matched in this defensive battle.",
   "key_moments": "No significant moments or shifts in momentum were identified during this game."
 }
}

This analysis highlights the performance of both teams, noting that neither team scored any points and their offenses struggled to find a rhythm. The key moments section indicates that no critical events directly impacting the score occurred during the game.  {
    "teams": ["New Orleans Saints", "Philadelphia Eagles"],
    "score": {"New Orleans Saints": 7, "Philadelphia Eagles": 6},
    "events": [
        {
            "type": "interception",
            "player": "Tyrann Mathieu",
            "team": "New Orleans Saints",
            "quarter": 1
        },
        {
            "type": "fumble_recovery",
            "player": "Willie Gay",
            "team": "New Orleans Saints",
            "quarter": 1
        }
    ],
    "analysis": {
        "new_orleans_saints_performance": "The New Orleans Saints started the game strongly, with Tyrann Mathieu's interception setting the tone for a successful first quarter. Willie Gay's fumble recovery also contributed to their 7-point lead.",
        "philadelphia_eagles_performance": "The Philadelphia Eagles struggled in the first half, with costly turnovers affecting their momentum. However, they will look to regroup and mount a comeback in the second half.",
        "key_moments": "Tyrann Mathieu's interception and Willie Gay's fumble recovery were key moments that put the New Orleans Saints in the lead."
    }
}  Based on the provided text, here's the analysis:

{
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 17, "New Orleans Saints": 24},
  "events": [
    {
      "type": "touchdown",
      "player": "Dallas Goedert (88)",
      "team": "Philadelphia Eagles",
      "quarter": 1
    },
    {
      "type": "interception",
      "player": "Tyrann Mathieu (32)",
      "team": "New Orleans Saints",
      "quarter": 2
    },
    {
      "type": "penalty",
      "player": "Player Z",
      "team": "New Orleans Saints",
      "quarter": 3
    }
  ],
  "analysis": {
    "Philadelphia_Eagles_performance": "The Philadelphia Eagles started the game well, with Dallas Goedert scoring a touchdown in the first quarter. However, they struggled to maintain momentum throughout the game, especially after key turnovers and penalties.",
    "New_Orleans_Saints_performance": "The Saints responded to the Eagles' initial touchdown with an interception by Tyrann Mathieu, which shifted the momentum in their favor. They capitalized on this advantage, scoring more points and managing the game effectively.",
    "key_moments": "The key moment of the game was the interception by Tyrann Mathieu, which changed the flow of the game and ultimately led to the Saints' victory."
  }
}  Here is the analysis based on the provided text:

```json
{
  "teams": ["New Orleans Saints", "Philadelphia Eagles"],
  "score": {"New Orleans Saints": 0, "Philadelphia Eagles": 0},
  "events": [
    {
      "type": "fumble_recovery",
      "player": "Herbert (Saints linebacker)",
      "team": "New Orleans Saints",
      "quarter": 1,
      "time": "first half"
    },
    {
      "type": "stop",
      "player": "Chase Young (99) (Saints defensive end)",
      "team": "New Orleans Saints",
      "quarter": 1,
      "time": "first half"
    }
  ],
  "analysis": {
    "New_Orleans_Saints_performance": "The New Orleans Saints started the game aggressively with a fumble recovery by Herbert and a stop by Chase Young in the first half. These plays showcased their defensive prowess, potentially setting the tone for the game.",
    "Philadelphia_Eagles_performance": "The Philadelphia Eagles' offense struggled in the first half, highlighted by a stop on running back Saquon Barkley by Saints defensive end Chase Young.",
    "key_moments": "Two critical moments in the first half were the fumble recovery by Herbert and the stop by Chase Young. These plays demonstrated the Saints' ability to create turnovers and disrupt the Eagles' offense."
  }
}
```  {
  "teams": ["Philadelphia Eagles", "New Orleans Saints"],
  "score": {"Philadelphia Eagles": 14, "New Orleans Saints": 10},
  "events": [
    {
      "type": "touchdown",
      "player": "Nakobe Dean",
      "team": "Philadelphia Eagles",
      "quarter": 2
    },
    {
      "type": "interception",
      "player": "Nolan Smith Jr.",
      "team": "New Orleans Saints",
      "quarter": 3
    }
  ],
  "analysis": {
    "philadelphia_eagles_performance": "The Philadelphia Eagles demonstrated a strong offensive performance in the first half, culminating in a touchdown by Nakobe Dean in the second quarter. The defense also showed resilience, with key plays from Dean and Nolan Smith Jr. contributing to the team's success.",
    "new_orleans_saints_performance": "The New Orleans Saints struggled offensively throughout the game but managed a pivotal interception by Nolan Smith Jr. in the third quarter that temporarily shifted momentum towards their favor.",
    "key_moments": "The touchdown by Nakobe Dean and the interception by Nolan Smith Jr. were key moments in the game, shaping the scoreboard and the flow of the match."
  }
}  Based on the provided text, here's a JSON output that adheres to the requirements:

```json
{
  "teams": ["New Orleans Saints", "Philadelphia Eagles"],
  "score": {"New Orleans Saints": X, "Philadelphia Eagles": Y},
  "events": [
    {
      "type": "meeting",
      "player": "Not applicable",
      "team": ["New Orleans Saints", "Philadelphia Eagles"],
      "quarter": "Post-game"
    }
  ],
  "analysis": {
    "new_orleans_saints_performance": "The New Orleans Saints showed a solid performance throughout the game, with X points scored. The coaching exchange between Dennis Allen and Nick Sirianni after the game suggests a friendly rivalry between the two teams.",
    "philadelphia_eagles_performance": "The Philadelphia Eagles put up Y points against the Saints. Despite the loss, the team demonstrated a strong offensive showing under the leadership of coach Nick Sirianni.",
    "key_moments": "The key moment in this game was the post-game meeting between the coaches, as it highlighted the competitive spirit between these two teams."
  }
}
```

This output reflects the teams involved, their scores, a single event (the post-game meeting), an analysis of each team's performance and key moments in the game. The information is presented in a structured JSON format for easy parsing and storage.  {
     "teams": ["Philadelphia Eagles", "New Orleans Saints"],
     "score": {"Philadelphia Eagles": 24, "New Orleans Saints": 21},
     "events": [
         {
             "type": "touchdown",
             "player": "Dallas Goedert (88)",
             "team": "Philadelphia Eagles",
             "quarter": 1
         },
         // Additional events can be added as needed, ensure they are game-defining and impactful to the score or momentum
     ],
     "analysis": {
         "philadelphia_eagles_performance": "The Philadelphia Eagles started strongly with a touchdown from tight end Dallas Goedert in the first quarter. The team's performance was characterized by effective offensive plays and strong leadership from coach Nick Sirianni and quarterback Jalen Hurts, who led the team to victory despite Goedert leaving the field during the game.",
         "new_orleans_saints_performance": "The New Orleans Saints showed resilience throughout the game, scoring 21 points and mounting a comeback in the second half. However, key mistakes and penalties hindered their chances of victory, with an interception being a crucial turning point in the match.",
         "key_moments": "The Philadelphia Eagles' touchdown in the first quarter set the tone for the game, while the interception by the Saints in the third quarter shifted momentum decisively towards the Eagles. Despite the Saints mounting a strong comeback, the Eagles managed to hold on for the win."
     }
   }  {
   "teams": ["New Orleans Saints", "Philadelphia Eagles"],
   "score": {"New Orleans Saints": 24, "Philadelphia Eagles": 30},
   "events": [
      {
         "type": "touchdown",
         "player": "Player A",
         "team": "New Orleans Saints",
         "quarter": 1
      },
      {
         "type": "interception",
         "player": "Player B",
         "team": "Philadelphia Eagles",
         "quarter": 2
      },
      {
         "type": "touchdown",
         "player": "Jalen Hurts",
         "team": "Philadelphia Eagles",
         "quarter": 3
      },
      {
         "type": "interception",
         "player": "Player C",
         "team": "Philadelphia Eagles",
         "quarter": 4
      }
   ],
   "analysis": {
      "new_orleans_saints_performance": "The Saints demonstrated a strong offensive performance, scoring two touchdowns in the first quarter. However, their defense faltered in the second half, allowing two crucial interceptions that significantly impacted the game flow.",
      "philadelphia_eagles_performance": "QB Jalen Hurts led the Eagles to victory with a touchdown in the third quarter and a clutch interception in the fourth that sealed the win. Their defense showed resilience, particularly in the second half, limiting the Saints' scoring opportunities.",
      "key_moments": "The Saints' early scoring momentum was halted by the Eagles' interception in the second quarter, and Jalen Hurts' third-quarter touchdown shifted the game in favor of Philadelphia. The final interception secured the Eagles' victory."
   }
}  {
   "teams": ["New Orleans Saints", "Philadelphia Eagles"],
   "score": {"New Orleans Saints": 21, "Philadelphia Eagles": 24},
   "events": [
      {
         "type": "interception",
         "player": "Eagles Defender X",
         "team": "Philadelphia Eagles",
         "quarter": 4
      }
   ],
   "analysis": {
      "new_orleans_saints_performance": "The Saints displayed impressive offense with a total of 21 points. However, their final drive ended in an interception in the fourth quarter, ultimately costing them the game.",
      "philadelphia_eagles_performance": "The Eagles defense proved crucial, stopping the Saints' last-ditch effort with an interception that sealed the victory for Philadelphia.",
      "key_moments": "Key moments in this game included the Saints' offensive drives leading to 21 points and the Eagles' pivotal interception at the end of the fourth quarter."
   }
}  Here is a possible JSON output for the analysis of the game between the Philadelphia Eagles and the New Orleans Saints on September 22, 2024:

{
  "teams": ["New Orleans Saints", "Philadelphia Eagles"],
  "score": {"New Orleans Saints": 21, "Philadelphia Eagles": 20},
  "events": [
    {
      "type": "touchdown",
      "player": "Alvin Kamara",
      "team": "New Orleans Saints",
      "quarter": 1
    },
    {
      "type": "field_goal",
      "player": "Wil Lutz",
      "team": "New Orleans Saints",
      "quarter": 2
    },
    {
      "type": "interception",
      "player": "Malcolm Jenkins",
      "team": "Philadelphia Eagles",
      "quarter": 3
    },
    {
      "type": "touchdown",
      "player": "Dallas Goedert",
      "team": "Philadelphia Eagles",
      "quarter": 4
    }
  ],
  "analysis": {
    "new_orleans_saints_performance": "The Saints started the game strong with Alvin Kamara scoring a touchdown in the first quarter. Wil Lutz added a field goal in the second quarter to extend their lead. Despite giving up an interception to Malcolm Jenkins in the third quarter, the Saints defense held firm and prevented the Eagles from scoring any additional points. The Saints' offensive line provided excellent protection for Jameis Winston, who completed 21 out of 30 passes for 274 yards and a touchdown.",
    "philadelphia_eagles_performance": "The Eagles struggled offensively for much of the game but managed to score a touchdown in the fourth quarter thanks to a great catch by Dallas Goedert. The defense had its moments, including an interception by Malcolm Jenkins that stalled a Saints drive. However, the Eagles were unable to capitalize on their turnovers and ultimately came up short.",
    "key_moments": "The key moment of the game was Alvin Kamara's touchdown in the first quarter, which gave the Saints an early lead they would never relinquish. Another critical moment was the interception by Malcolm Jenkins in the third quarter that stopped a potential Eagles scoring drive."
  }
}

This output provides a concise summary of the game between the New Orleans Saints and the Philadelphia Eagles, focusing on key events, team performances, and game flow. The JSON format ensures easy parsing and storage of the analysis.  Based on the article provided, here is the analysis in the requested JSON format:

```json
{
 "teams": ["New Orleans Saints", "Philadelphia Eagles"],
 "score": {"New Orleans Saints": 14, "Philadelphia Eagles": 7},
 "events": [
 {
 "type": "interception",
 "player": "Tyrann Mathieu",
 "team": "New Orleans Saints",
 "quarter": 1
 },
 {
 "type": "fumble recovery",
 "player": "Willie Gay",
 "team": "New Orleans Saints",
 "quarter": 1
 }
 ],
 "analysis": {
 "New Orleans Saints_performance": "The New Orleans Saints displayed a strong defensive performance in the first half, with key plays by safety Tyrann Mathieu and linebacker Willie Gay. These plays significantly impacted the momentum early on and contributed to their 14-7 lead.",
 "Philadelphia Eagles_performance": "The Philadelphia Eagles struggled offensively in the first half, giving up an interception and a fumble recovery that directly affected their scoreline. Their offense will need to improve in the second half if they are to mount a comeback.",
 "key_moments": "The interception by Tyrann Mathieu and the fumble recovery by Willie Gay were game-defining moments for the New Orleans Saints, as both plays directly led to points and put them ahead early."
 }
}
```  {
    "teams": ["Philadelphia Eagles", "New Orleans Saints"],
    "score": {"Philadelphia Eagles": 14, "New Orleans Saints": 7},
    "events": [
        {
            "type": "play_attempt",
            "player": "Dallas Goedert (88)",
            "team": "Philadelphia Eagles",
            "quarter": 1,
            "time": "first half"
        },
        {
            "type": "tackle",
            "player": "Tyrann Mathieu (32)",
            "team": "New Orleans Saints",
            "quarter": 1,
            "time": "first half"
        },
        {
            "type": "celebration",
            "player": "Willie Gay",
            "team": "New Orleans Saints",
            "quarter": not_provided,
            "time": "not provided"
        }
    ],
    "analysis": {
        "Philadelphia_Eagles_performance": "Dallas Goedert's play attempt in the first half was thwarted by Tyrann Mathieu, but it set up a later touchdown for the Eagles. Their offense showed promising signs of fluidity, especially when capitalizing on crucial opportunities.",
        "New Orleans_Saints_performance": "The Saints' defense demonstrated resilience in stopping the Eagles' initial play attempt, with Mathieu making an impactful tackle. However, their offense was unable to find a rhythm, as evidenced by Willie Gay's celebration being unrelated to scoring.",
        "key_moments": "The key moment of the game was the Eagles' touchdown following Dallas Goedert's play attempt. This score shifted the momentum in favor of Philadelphia and set them on a path towards victory."
    }
}  {
   "teams": ["New Orleans Saints", "Philadelphia Eagles"],
   "score": {"New Orleans Saints": 0, "Philadelphia Eagles": 0},
   "events": [
      {
         "type": "fumble_recovery",
         "player": "Not specified (Recovered by New Orleans Saints)",
         "team": "New Orleans Saints",
         "quarter": 1,
         "time": "First half"
      },
      {
         "type": "tackle",
         "player": "Chase Young (99)",
         "team": "New Orleans Saints",
         "quarter": 1,
         "time": "First half"
      },
      {
         "type": "tackle",
         "player": "Nakobe Dean (17)",
         "team": "Philadelphia Eagles",
         "quarter": 1,
         "time": "First half"
      }
   ],
   "analysis": {
      "new_orleans_saints_performance": "The Saints managed to recover a fumble in the first half, which could potentially be a game-changing event if capitalized upon. Chase Young made an impactful tackle that showcased their defensive prowess.",
      "philadelphia_eagles_performance": "The Eagles had a notable tackle by Nakobe Dean in the first half, indicating some level of resistance against the Saints' offense.",
      "key_moments": "The fumble recovery and subsequent tackles by both teams are critical moments that could significantly influence the game's outcome."
   }
}  Based on the provided text, here is the analysis:

```json
{
  "teams": ["Team A", "New Orleans Saints"],
  "score": {"Team A": null, "New Orleans Saints": null},
  "events": [
    {
      "type": "action_play",
      "player": "Nolan Smith Jr. (3)",
      "team": "Team A",
      "quarter": null
    }
  ],
  "analysis": {
    "team_A_performance": "Nolan Smith Jr. was involved in an action play during the game against the New Orleans Saints, but no score or outcome information was provided.",
    "team_NewOrleansSaints_performance": "Not applicable as no specific performance details were mentioned for the Saints.",
    "key_moments": "The key moment in this analysis is the action play involving Nolan Smith Jr. from Team A."
  }
}
```

Please note that since the provided text does not include any scoring information or game-defining events, the score and key moments sections are left blank. Additionally, the event type "action_play" is used instead of "touchdown", "interception", or other specific event types because no such detail was given in the text. If more detailed or specific information becomes available about the play, this analysis can be updated accordingly.  {
    "teams": ["Philadelphia Eagles", "New Orleans Saints"],
    "score": {"Philadelphia Eagles": 30, "New Orleans Saints": 27},
    "events": [
        {
            "type": "touchdown",
            "player": "Jalen Hurts",
            "team": "Philadelphia Eagles",
            "quarter": 1
        },
        {
            "type": "interception",
            "player": "Taliese Fuaga",
            "team": "New Orleans Saints",
            "quarter": 2
        },
        {
            "type": "penalty",
            "player": "Malcolm Jenkins",
            "team": "Philadelphia Eagles",
            "quarter": 3
        }
    ],
    "analysis": {
        "philadelphia_eagles_performance": "The Philadelphia Eagles started the game with a touchdown by Jalen Hurts, setting a positive tone. However, they faced a setback due to a penalty on Malcolm Jenkins in the third quarter. Despite this, their offense managed to regain momentum and secure a crucial win.",
        "new_orleans_saints_performance": "The Saints responded with an interception by Taliese Fuaga in the second quarter, which momentarily shifted the game's momentum in their favor. However, they struggled to capitalize on opportunities and were unable to maintain the lead, ultimately losing by three points.",
        "key_moments": "The key moments of this game included Jalen Hurts' touchdown, Taliese Fuaga's interception, and Malcolm Jenkins' penalty. These events significantly impacted the flow of the game, with each team taking turns leading and losing the advantage."
    }
}

In this analysis:
- The teams were identified as the Philadelphia Eagles and the New Orleans Saints.
- The score was 30 for the Eagles and 27 for the Saints.
- Critical events included a touchdown by Jalen Hurts in the first quarter, an interception by Taliese Fuaga in the second quarter, and a penalty on Malcolm Jenkins in the third quarter.
- The performance analysis highlighted how each team's successes, struggles, and key moments influenced the game outcome.
- Key turning points were identified as Jalen Hurts' touchdown and Taliese Fuaga's interception, with each event impacting the flow of the game.
- The output was concise and focused on relevant information about the game.  Based on the provided textual content, here is the analysis:

{
  "teams": ["Eagles", "Unspecified"],
  "score": {"Eagles": X, "Unspecified": Y},
  "events": [
    {
      "type": "interception",
      "player": "Unspecified",
      "team": "Eagles",
      "quarter": 4
    },
    // Add more events as they are mentioned in the article, ensuring to specify player, team, and quarter.
  ],
  "analysis": {
    "eagles_performance": "The Eagles demonstrated a strong defensive play by intercepting the ball in the fourth quarter, potentially turning the tide of the game. However, the specific plays leading up to this critical moment are unspecified.",
    "unspecified_performance": "The opposing team's performance before the interception is not detailed in the text provided.",
    "key_moments": "The interception in the fourth quarter by the Eagles could be a game-defining moment, as it directly impacted the score and potentially shifted momentum."
  }
}

As the information about other plays and interactions between players is not specified, they are not included in the analysis. The text does not provide sufficient details to include high school sports or a weekly newsletter sign-up for updates.  Here's an example of how I would analyze a hypothetical football game between Team A and Team B based on textual content provided:

```json
{
  "teams": ["Team A", "Team B"],
  "score": {"Team A": 21, "Team B": 17},
  "events": [
    {
      "type": "touchdown",
      "player": "Player X",
      "team": "Team A",
      "quarter": 1,
      "time": "0:45"
    },
    {
      "type": "interception",
      "player": "Player Y",
      "team": "Team B",
      "quarter": 2,
      "time": "1:30"
    },
    {
      "type": "touchdown",
      "player": "Player Z",
      "team": "Team A",
      "quarter": 3,
      "time": "5:15"
    },
    {
      "type": "penalty",
      "player": "Player W",
      "team": "Team B",
      "quarter": 4,
      "time": "8:00"
    }
  ],
  "analysis": {
    "team_A_performance": "Team A showcased a strong offensive performance with two touchdowns by players X and Z. The team managed to score 21 points despite some turnovers and penalties. The key moment was the touchdown by Player X in the first quarter which set the tone for the game, giving Team A an early lead.",
    "team_B_performance": "Team B struggled offensively but managed to capitalize on a turnover with an interception by Player Y in the second quarter. However, a crucial penalty by Player W in the fourth quarter stalled their final drive and cost them the game.",
    "key_moments": "The first touchdown by Team A was a pivotal moment that gave them the early lead and put pressure on Team B. The interception by Player Y for Team B provided a glimmer of hope, but ultimately it wasn't enough to overcome Team A's scoring output."
  }
}
    '''
    result = client.ai_processor(prompt)
    print("AI-Generated Game Analysis Scores:\n")
    print(result)

if __name__ == "__main__":
    main()
