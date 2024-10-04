import ollama

def chunk_text(text, max_size):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Function to process each chunk and aggregate responses
def process_chunks(model, prompt, chunk_size=500):
    chunks = chunk_text(prompt, chunk_size)
    responses = []

    for chunk in chunks:
        response = ollama.generate(model=model, prompt=chunk)
        # Extract only the 'response' key's value, which contains the desired text
        if 'response' in response:
            clean_response = response['response']
            responses.append(clean_response)
        else:
            # If 'response' key is missing, print for debugging
            print("Response does not contain 'response' key:", response)

    return ' '.join(responses)

# Example usage
prompt = '''
 BRETT MARTEL Associated PressNEW ORLEANS -- Saquon Barkley rushed for fourth-quarter touchdowns of 65 and 4 yards, and the Philadelphia Eagles rebounded from a maddening late-game collapse six days earlier to beat the New Orleans Saints 15-12 on Sunday. Barkley's short
... er scoring run came with 1:01 left, one play after Dallas Goedert got free across the middle on third-and-16 for a 61-yard catch and run that gave him a career-high 170 yards on 10 receptions. Eagles safety Reed Blankenship sealed the victory when he intercepted Derek
... Carr's pass over the middle with 48 seconds left, capping a banner performance by Philadelphia's defense against an offense that had scored an NFL-high 91 points during the regular season's first two weeks under new coordinator Klint Kubiak. Coming off a 22-21 home los
... s to Atlanta on Monday night, the Eagles (2-1) did not allow a touchdown until Carr found Chris Olave for a 12-yard, go-ahead score with just  than two minutes left. That gave the Saints a 12-7 lead after a failed 2-point try.People are also reading... 2 arrested in fi
... ght at Atlantic City casino; video of incident has  than 2 million views Murphy questions whether Atlantic City mayor should stay in job after child abuse indictment Oakcrest High School closed for threat; arrest made in separate Upper Township school threat Targeted s
... chools list is actually Excel document of state school improvement plan, superintendent says Ron Jon Surf Shop in Ocean City to close next month Shelter-in-place order lifted at Upper Township schools after State Police investigation Egg Harbor Township Mediterranean r
... estaurant shuts doors Jay-Z, Fanatics CEO Michael Rubin open sportsbook at Ocean Casino Resort Atlantic City mayor, school superintendent to be arraigned Oct. 10 in child abuse case Atlantic City scores twice in 11 seconds to beat 11th-ranked Ocean City Have unused Gil
... lian's Wonderland tickets? This teacher is donating them to local kids. Morris County resident wins $1.45 million at Ocean Casino Resort; 14 jackpots over $1M this year Phillies send Buddy Kennedy back to Triple-A. Which player is taking his spot? Injured Isiah Pacheco
...  provides hopeful update on social media ACIT wins second straight football game The Eagles looked the better team on both sides of the ball, outgaining New Orleans (2-1) in total net yards, 460 to 219. But a number of curious decisions by heavily scrutinized Philadelp
... hia coach Nick Sirianni, along with some clutch plays by the Saints' defense, kept the Eagles off the board for three quarters. Hurts turned the ball over twice in the first half, intercepted by Tyrann Mathieu in the end zone and losing a fumble on a sack by Carl Grand
... erson. The Eagles again threatened to score late in the second quarter, only to come away empty when they eschewed a field goal on fourth-and-1 from the New Orleans 15 with just 14 seconds left. Defensive end Chase Young and linebacker Pete Werner stuffed Barkley's run
...  to the left side, preserving the Saints' 3-0 lead at halftime. The Eagles twice drove into Saints territory in the third quarter, only to fail on fourth-and-short and then have an illegal substitution penalty contribute to a stall near midfield. But after J.T. Gray's
... block of Braden Mann's punt gave New Orleans the ball inside the Philadelphia 30, New Orleans stalled out on their own fourth-and-1 failure late in the third quarter. Barkley's long run came four play's later to make it 7-3. Already missing receiver A.J. Brown, the Eag
... les lost Devonta Smith early in the fourth quarter on a hit by defensive tackle Khristian Boyd that knocked the receiver's helmet off as he tried to prevent two other Saints defenders from bringing him to the turf. What appeared to be a concussion-causing, helmet-to-he
... lmet hit came after Smith's seventh catch, giving him 79 yards receiving for the game. That drive wound up stalling when the Eagles elected to try a 60-yard Jake Elliott field goal, which missed. Injuries Eagles: WR Britain Covey left with a shoulder injury. ... RT Lan
... e Johnson left with a concussion in the first half. Saints: Versatile TE Taysom Hill (chest) was ruled out two hours before kickoff. ... C Erik McCoy limped off the field with a left groin injury on the game's opening possession and could not return. ... RG Cesar Ruiz
... received attention for an apparent lower body injury in the fourth quarter. Up next Eagles: Visit Tampa Bay on Sunday in a third straight game against an NFC South opponent, and second straight on the road. Saints: Visit Atlanta on Sunday. This is a developing story. C
... heck back for further coverage. Philadelphia00015 -- 15New Orleans3009 -- 12 First Quarter NO -- FG Grupe 34, 6:51. Fourth Quarter Phi -- Barkley 65 run (Elliott kick), 13:17. NO -- FG Grupe 38, 9:49. NO -- Olave 13 pass from Carr (pass failed), 2:03. Phi -- Barkley 4
... run (Barkley run), 1:01. A -- 70,006. PhiNOFirst downs2012Total Net Yards460219Rushes-yards25-17229-89Passing288130Punt Returns1-61-0Kickoff Returns3-770-0Interceptions Ret.1-01-23Comp-Att-Int29-38-114-25-1Sacked-Yards Lost4-231-12Punts2-21.54-40.5Fumbles-Lost1-10-0Pen
... alties-Yards7-453-25Time of Possession32:1527:45 INDIVIDUAL STATISTICS RUSHING -- Philadelphia, Barkley 17-147, Hurts 8-25. New Orleans, Kamara 26-87, Carr 2-3, Williams 1-(minus 1). PASSING -- Philadelphia, Hurts 29-38-1-311. New Orleans, Carr 14-25-1-142. RECEIVING -
... - Philadelphia, Goedert 10-170, D.Smith 7-79, Barkley 4-9, Campbell 2-13, Gainwell 2-12, Dotson 2-8, Covey 1-11, Wilson 1-9. New Orleans, Olave 6-86, Kamara 3-40, Tipton 2-11, Wilson 1-3, au 1-2, Williams 1-0. MISSED FIELD GOALS -- Philadelphia, Elliott 60. Close Phila
... delphia Eagles wide receiver Johnny Wilson (89) can't hold onto a pass as he is defended by New Orleans Saints cornerback Alontae Taylor (1) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Phil
... adelphia Eagles fans cheer in the second half of an NFL football game between the Eagles and the New Orleans Saints in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints defensive tackle Bryan Bresee, center, sacks Philadelphia Eag
... les quarterback Jalen Hurts (1) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints defensive tackle Bryan Bresee (90) celebrates his sack of Philadelphia Eagles quarterback Jale
... n Hurts, kneeling on the ground, in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints wide receiver Chris Olave (12) catches a pass as he is defended by Philadelphia Eagles corner
... back Quinyon Mitchell (27) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles' Cooper DeJean (33) returns a punt and is stopped by New Orleans Saints defenders J.T. Gray (48) a
... nd Payton Turner (98) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints safety Jordan Howden (31) runs back a blocked punt as Philadelphia Eagles linebacker Nolan Smith Jr. (3)
...  gives chase in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles running back Saquon Barkley (26) runs 65 yards for a touchdown as New Orleans Saints cornerback Marshon Lattimor
... e (23) gives chase in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles running back Saquon Barkley (26) runs 65 yards for a touchdown against the New Orleans Saints in the second half o
... f an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles running back Saquon Barkley celebrates with fans after he ran 65 yards for a touchdown against the New Orleans Saints in the second half of an NFL footba
... ll game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints running back Alvin Kamara (41) catches a pass over Philadelphia Eagles linebacker Zack Baun (53) in the second half of an NFL football game in New Orleans, Sunday, Sept.
...  22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles cornerback Darius Slay Jr. celebrates after breaking up a pass against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Her
... bert)
... Gerald Herbert New Orleans Saints wide receiver Chris Olave (12) catches a touchdown pass against the Philadelphia Eagles in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024.
... Butch Dill New Orleans Saints wide receiver Chris Olave (12) catches a pass as he is defended by Philadelphia Eagles cornerback Kelee Ringo (22) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadel
... phia Eagles quarterback Jalen Hurts (1) passes over the reach of New Orleans Saints defensive end Cameron Jordan (94) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert)
... Gerald Herbert New Orleans Saints quarterback Derek Carr (4) fakes a pass as she scrambles against Philadelphia Eagles linebacker Zack Baun (53) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert
... Philadelphia Eagles running back Saquon Barkley (26) celebrates after scoring a two-point conversion against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia
... Eagles safety Reed Blankenship (32) celebrates his interception that ended the New Orleans Saints' final drive in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints head coach D
... ennis Allen, left, and Philadelphia Eagles head coach Nick Sirianni meet on the field after an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill
... Philadelphia Eagles tight end Dallas Goedert (88) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles head coach Nick Sirianni leaves the field aft
... er a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill
... Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill
... Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints offensive tackle Taliese Fuaga (75) look
... s up at the scoreboard after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert
... New Orleans Saints players watch from the bench after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans
...  Saints owner Gayle Benson, right, talks with Philadelphia Eagles owner Jeffrey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints owner Gayle Benson, right, talks with Philadelphia Eagles owner
...  Jeffrey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles punter Braden Mann kicks against the New Orleans Saints in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2
... 024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints safety Tyrann Mathieu (32) celebrates with teammates after intercepting a pass against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/G
... erald Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a fumble against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert)
... Gerald Herbert Philadelphia Eagles tight end Dallas Goedert (88) is upended by New Orleans Saints safety Tyrann Mathieu (32) in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles t
... ight end Dallas Goedert (88) is brought down in the first half of an NFL football game against the New Orleans Saints in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a
...  fumble against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert
... New Orleans Saints defensive end Chase Young (99) celebrates a stop against Philadelphia Eagles running back Saquon Barkley (26) in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles lineb
... acker Nakobe Dean (17) celebrates after a play with linebacker Nolan Smith Jr. (3) during an NFL football game against the New Orleans Saints, Sunday, Sept. 22, 2024, in New Orleans. (AP Photo/Tyler Kaufman) Tyler Kaufman PHOTOS Eagles beat New Orleans Saints Philadelp
... hia Eagles wide receiver Johnny Wilson (89) can't hold onto a pass as he is defended by New Orleans Saints cornerback Alontae Taylor (1) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert)
... Gerald Herbert Philadelphia Eagles fans cheer in the second half of an NFL football game between the Eagles and the New Orleans Saints in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill)
... Butch Dill New Orleans Saints defensive tackle Bryan Bresee, center, sacks Philadelphia Eagles quarterback Jalen Hurts (1) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints def
... ensive tackle Bryan Bresee (90) celebrates his sack of Philadelphia Eagles quarterback Jalen Hurts, kneeling on the ground, in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints wi
... de receiver Chris Olave (12) catches a pass as he is defended by Philadelphia Eagles cornerback Quinyon Mitchell (27) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles' Cooper
...  DeJean (33) returns a punt and is stopped by New Orleans Saints defenders J.T. Gray (48) and Payton Turner (98) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints safety Jordan
...  Howden (31) runs back a blocked punt as Philadelphia Eagles linebacker Nolan Smith Jr. (3) gives chase in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert
... Philadelphia Eagles running back Saquon Barkley (26) runs 65 yards for a touchdown as New Orleans Saints cornerback Marshon Lattimore (23) gives chase in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Ph
... iladelphia Eagles running back Saquon Barkley (26) runs 65 yards for a touchdown against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill
... Philadelphia Eagles running back Saquon Barkley celebrates with fans after he ran 65 yards for a touchdown against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Sai
... nts running back Alvin Kamara (41) catches a pass over Philadelphia Eagles linebacker Zack Baun (53) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert
... Philadelphia Eagles cornerback Darius Slay Jr. celebrates after breaking up a pass against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints wide receive
... r Chris Olave (12) catches a touchdown pass against the Philadelphia Eagles in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints wide receiver Chris Olave (12) catches a pass as he is def
... ended by Philadelphia Eagles cornerback Kelee Ringo (22) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill)
... Butch Dill Philadelphia Eagles quarterback Jalen Hurts (1) passes over the reach of New Orleans Saints defensive end Cameron Jordan (94) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orle
... ans Saints quarterback Derek Carr (4) fakes a pass as she scrambles against Philadelphia Eagles linebacker Zack Baun (53) in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles run
... ning back Saquon Barkley (26) celebrates after scoring a two-point conversion against the New Orleans Saints in the second half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles safety Reed Blan
... kenship (32) celebrates his interception that ended the New Orleans Saints' final drive in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert)
... Gerald Herbert New Orleans Saints head coach Dennis Allen, left, and Philadelphia Eagles head coach Nick Sirianni meet on the field after an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles tight end Dallas
... Goedert (88) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles head coach Nick Sirianni leaves the field after a win over the New Orleans Saints
... in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP
...  Photo/Butch Dill) Butch Dill Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints offensive
... tackle Taliese Fuaga (75) looks up at the scoreboard after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Or
... leans Saints players watch from the bench after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saint
... s owner Gayle Benson, right, talks with Philadelphia Eagles owner Jeffrey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints owner Gayle Benson, right, talks with Philadelphia Eagles owner Jeffr
... ey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles punter Braden Mann kicks against the New Orleans Saints in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (
... AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints safety Tyrann Mathieu (32) celebrates with teammates after intercepting a pass against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald
... Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a fumble against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia
...  Eagles tight end Dallas Goedert (88) is upended by New Orleans Saints safety Tyrann Mathieu (32) in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles tight end Dallas Goedert (88
... ) is brought down in the first half of an NFL football game against the New Orleans Saints in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a fumble against the Philade
... lphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints defensive end Chase Young (99) celebrates a stop against Philadelphia Eagles running back Saquon Barkley (26) in t
... he first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles linebacker Nakobe Dean (17) celebrates after a play with linebacker Nolan Smith Jr. (3) during an NFL football game against the New Orlean
... s Saints, Sunday, Sept. 22, 2024, in New Orleans. (AP Photo/Tyler Kaufman) Tyler Kaufman Can't get enough High School sports? Get the latest scores, game highlights and analysis delivered to your inbox each week Sign up! * I understand and agree that registration on or
...  use of this site constitutes agreement to its user agreement and privacy policy. Get in the game with our Prep Sports Newsletter Sent weekly directly to your inbox! Sign up! * I understand and agree that registration on or use of this site constitutes agreement to its
...  user agreement and privacy policy.
>>> Gerald Herbert New Orleans Saints head coach Dennis Allen, left, and Philadelphia Eagles head coach Nick Sirianni meet on the field after an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles tight end Dallas
... Goedert (88) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles head coach Nick Sirianni leaves the field after a win over the New Orleans Saints
... in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP
...  Photo/Butch Dill) Butch Dill Philadelphia Eagles quarterback Jalen Hurts (1) leaves the field after a win over the New Orleans Saints in an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints offensive
... tackle Taliese Fuaga (75) looks up at the scoreboard after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Or
... leans Saints players watch from the bench after the Philadelphia Eagles stopped the Saints' final drive with an interception in the fourth quarter of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saint
... s owner Gayle Benson, right, talks with Philadelphia Eagles owner Jeffrey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill New Orleans Saints owner Gayle Benson, right, talks with Philadelphia Eagles owner Jeffr
... ey Lurie before an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles punter Braden Mann kicks against the New Orleans Saints in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (
... AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints safety Tyrann Mathieu (32) celebrates with teammates after intercepting a pass against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald
... Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a fumble against the Philadelphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia
...  Eagles tight end Dallas Goedert (88) is upended by New Orleans Saints safety Tyrann Mathieu (32) in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert Philadelphia Eagles tight end Dallas Goedert (88
... ) is brought down in the first half of an NFL football game against the New Orleans Saints in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints linebacker Willie Gay celebrates after recovering a fumble against the Philade
... lphia Eagles in the first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Gerald Herbert) Gerald Herbert New Orleans Saints defensive end Chase Young (99) celebrates a stop against Philadelphia Eagles running back Saquon Barkley (26) in t
... he first half of an NFL football game in New Orleans, Sunday, Sept. 22, 2024. (AP Photo/Butch Dill) Butch Dill Philadelphia Eagles linebacker Nakobe Dean (17) celebrates after a play with linebacker Nolan Smith Jr. (3) during an NFL football game against the New Orlean
... s Saints, Sunday, Sept. 22, 2024, in New Orleans. (AP Photo/Tyler Kaufman) Tyler Kaufman Can't get enough High School sports? Get the latest scores, game highlights and analysis delivered to your inbox each week Sign up! * I understand and agree that registration on or
...  use of this site constitutes agreement to its user agreement and privacy policy. Get in the game with our Prep Sports Newsletter Sent weekly directly to your inbox! Sign up! * I understand and agree that registration on or use of this site constitutes agreement to its
...  user agreement and privacy policy.
 It appears you have provided a detailed report of an NFL football game between the Philadelphia Eagles and the New Orleans Saints, which took place on September 22, 2024. The pictures show key moments from the match, such as Jalen Hurts leaving the field after a win
for the Eagles, Taliese Fuaga looking up at the scoreboard after an interception in the fourth quarter by the Eagles, and various other plays and interactions between players on both teams. Additionally, there are images of team owners Jeffrey Lurie and Gayle Benson
conversing before the game, as well as a photo credit for AP Photographers Butch Dill, Gerald Herbert, and Tyler Kaufman. The last two sentences in your message suggest that if someone is interested in high school sports, they can sign up for a weekly newsletter to
receive updates and analysis on those games.
'''
response = process_chunks(model='testing', prompt=prompt)

# Print the cleaned response
print(response)
