import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import json
import time as tm
from datetime import datetime as dt, timedelta
import random
from PIL import Image
import shutil
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title = "Housie", page_icon="🔢", layout = "wide", initial_sidebar_state = "expanded")

vDrive = os.path.splitdrive(os.getcwd())[0]
if vDrive == "C:": vpth = "C:/Users/Shawn/dev/utils/housie/"   # local developer's disc
else: vpth = "./"

purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"    # thin divider line
horizontal_dashed_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px dashed #635985;'><br>"    # thin divider line

mystate = st.session_state
if "board_gen_no_lst" not in mystate: mystate.board_gen_no_lst = []

if "GameDetails" not in mystate: mystate.GameDetails = ['XP17',      #  0: GRN
                                                        'Shawn',     #  1: Player Name 
                                                        '',          #  2: Game Path
                                                        'auto',      #  3: auto/manual num gen
                                                        6.0,         #  4: default seconds interval for autogen
                                                        False,       #  5: start/stop toggle for auto mode 
                                                        True,        #  6: playsound toggle
                                                        None,        #  7: number animation lottie
                                                        dt.now(),    #  8: last time game event happened
                                                        '',          #  9: win string 
                                                        0,           # 10: current / last board-generated-number displayed on the ticket
                                                        ''           # 11: player avatar
                                                        ]

avtar_bank = ['😺', '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🌜', '🌛', '🐔', '🐧', '🐦', '🐤', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔', '🐥', '🦆', '🦅', '🦉', '🦇', ]

normal_no_colour = """<span style='background-color: #E0E0E0;
                                       color: #000000;
                                       font-size: 20px;
                                       border-radius: 7px;
                                       text-align: center;
                                       display:inline;
                                       padding-top: 3px;
                                       padding-bottom: 3px;
                                       padding-left: 0.4em;
                                       padding-right: 0.4em;
                                       '>
                                       |fill_variable|
                                       </span>"""

selected_no_colour = """<span style='background-color: #AED581;
                                         color: #000000;
                                         font-size: 20px;
                                         border-radius: 7px;
                                         text-align: center;
                                         display:inline;
                                         padding-top: 3px;
                                         padding-bottom: 3px;
                                         padding-left: 0.4em;
                                         padding-right: 0.4em;
                                         '>
                                         |fill_variable|
                                         </span>"""

last_gen_no_colour = """<span style='background-color: #76d7c4;
                                     color: #000000;
                                     font-size: 60px;
                                     border-radius: 7px;
                                     text-align: center;
                                     display:inline;
                                     margin-left: 107px;
                                     padding-top: 3px;
                                     padding-bottom: 3px;
                                     padding-left: 0.4em;
                                     padding-right: 0.4em;
                                     '>
                                     |fill_variable|
                                     </span>"""

win_txt = """<span style='background-color: #90CAF9;
                                     color: #000000;
                                     font-size: 20px;
                                     border-radius: 7px;
                                     text-align: center;
                                     display:inline;
                                     margin-left: 0px;
                                     padding-top: 4px;
                                     padding-bottom: 4px;
                                     padding-left: 0.4em;
                                     padding-right: 0.4em;
                                     '>
                                     |fill_variable|
                                     </span>"""

def ReduceGapFromPageTop():
    st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)  # reduce gap from page top
    st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 2rem; } </style> ", unsafe_allow_html=True)

def ReadPictureFile(wch_fl):
    try:
        pxfl = f"{vpth}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()

    except: return ""

def CreateSubDir(wch_sub_folder):
    vfull_dir_path = f"{vpth}/{wch_sub_folder}"
    chk_if_subdir_exists = os.path.isdir(vfull_dir_path)

    if not chk_if_subdir_exists:
        os.makedirs(vfull_dir_path)
        return False

def GenerateRandomCode():
    alphan_array = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return "".join(random.sample(alphan_array, 6))

@st.cache_data
def load_number_animation():
    number_animation = ReadPictureFile('NumberAnimation.gif')
    return f"<img src='data:png;base64,{number_animation}'>&nbsp;&nbsp;"

def GameDiskFile(what_to_do, GmDtl=""):
    gmfile = mystate.GameDetails[2] + "gamefile.json"

    if what_to_do == "create":
        if os.path.isfile(gmfile) == False:
            tmpdict = {"GameOver": False,
                       "GameAborted": False,
                       "PlayerCount": 0,
                       "CurrentNumber": 0,
                       "ExpiredBoardNumbers": [],
                       "UsedAvatars": [],
                       "Jaldi5": {"isWon": False, "whoWon": ""},
                       "Line1": {"isWon": False, "whoWon": ""},
                       "Line2": {"isWon": False, "whoWon": ""},
                       "Line3": {"isWon": False, "whoWon": ""},
                       "FullHouse": {"isWon": False, "whoWon": ""},
                       }
            json.dump(tmpdict, open(gmfile, "w"))     # write file

    elif what_to_do == "read":
        if os.path.isfile(gmfile) == True:
            vjson = {}
            while True:
                try:
                    vjson = json.load(open(gmfile, "r"))    # read file
                    break
                
                except: pass

            return vjson
        
    elif what_to_do == "write": json.dump(GmDtl, open(gmfile, "w"))

def ClearExpiredGameFolders():
    files_in_path = os.listdir(".")     # current workspace
    gm_fldr_lst = [x for x in files_in_path if not os.path.isfile(x) and x.startswith('HG_')] # chk if folders in dir; only ones that start w/HG_

    for gm_fldr in gm_fldr_lst:
        gmfile = f"./{gm_fldr}/gamefile.json"
        GmDtl = json.load(open(gmfile, "r"))
        if GmDtl["GameOver"] == True or GmDtl["GameAborted"] == True: shutil.rmtree("./" + gm_fldr, ignore_errors=True)

def GenUniqRndmAvatar(GmDtl):
    while True:
        vavatar = random.choice(avtar_bank)
        if vavatar not in GmDtl["UsedAvatars"]: break
    return vavatar

def GenUniqRndmNo():
    while True:
        vno = random.randint(1,90)
        if vno not in mystate.board_gen_no_lst:
            mystate.board_gen_no_lst.append(vno)
            break
    return vno

def GameAborted():
    ReduceGapFromPageTop()
    st.subheader(f"👾 Game Ref. No. (GRN): :blue[{mystate.GameDetails[0]}]:")
    st.markdown(horizontal_bar, True)
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    GmDtl = GameDiskFile("read")
    GmDtl["GameAborted"] = True
    GameDiskFile("write", GmDtl)

    for i in range(2): st.write("")    # vertical filler

    sc1, sc2, sc3 = st.columns((3,3,6))

    with sc1.container(): st.markdown(f"<img src='data:png;base64,{ReadPictureFile('GameAborted.png')}'>", unsafe_allow_html=True)

    with sc2.container():
        st.write("")
        st.subheader("🙋🏻‍♂️ Game Aborted:")

        st.markdown("The Admin. 👨🏼‍⚖️ has been aborted <br>in the game, please take note 📝.", True)
        st.write("Be a sport 🤸🏻‍♂️, don't be a goat 🐐.")
        st.write("")

        if sc2.button("🔙 Return to Main Page"):
            mystate.runpage = Main
            st.rerun()

    for i in range(3): st.write("")    # vertical filler 
    
    st.markdown(horizontal_bar, True)

def GameOver():
    ReduceGapFromPageTop()
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    sc01, sc02 = st.columns((1,25))
    sc01.markdown(f"""<img src="data:png;base64,{ReadPictureFile('GameOver.png')}" width='45' height='45' >""", unsafe_allow_html=True)
    sc02.subheader(f"Game Over: :blue[{mystate.GameDetails[0]}]:")

    st.markdown(horizontal_bar, True)

    GmDtl = GameDiskFile("read")
    GmDtl["GameOver"] = True
    GameDiskFile("write", GmDtl)

    ptxt = """<span style='color: #000000;
                            font-size: 18px;
                            text-align: center;
                            display:inline;
                            margin-left: 0px;
                            padding-top: 3px;
                            padding-bottom: 3px;
                            padding-left: 0.4em;
                            padding-right: 0.4em;
                            '>
                            |fill_variable|
                            </span>"""

    wtxt = """<span style='background-color: #90CAF9;
                            color: #000000;
                            font-size: 18px;
                            border-radius: 7px;
                            text-align: center;
                            display:inline;
                            margin-left: 0px;
                            padding-top: 3px;
                            padding-bottom: 3px;
                            padding-left: 0.4em;
                            padding-right: 0.4em;
                            '>
                            |fill_variable|
                            </span>"""

    for i in range(2): st.write("")    # vertical filler

    sc1, sc2, sc3 = st.columns((1,2,3))

    with sc2.container():
        st.markdown(f"""<img src="data:png;base64,{ReadPictureFile('victorydance.gif')}" width='270' height='270' >""", unsafe_allow_html=True)

    with sc3.container():
        st.subheader("🏆 Win Status:")

        wj5 = "No Winner" if GmDtl["Jaldi5"]["whoWon"] == "" else GmDtl["Jaldi5"]["whoWon"]
        st.markdown(ptxt.replace('|fill_variable|', f"5️⃣ Early 5 {'&nbsp;' * 5}: ") + wtxt.replace('|fill_variable|', wj5), True)

        wl1 = "No Winner" if GmDtl["Line1"]["whoWon"] == "" else GmDtl["Line1"]["whoWon"]
        st.markdown(ptxt.replace('|fill_variable|', f"1️⃣ Line #1 {'&nbsp;' * 5}: ") + wtxt.replace('|fill_variable|', wl1), True)

        wl2 = "No Winner" if GmDtl["Line2"]["whoWon"] == "" else GmDtl["Line2"]["whoWon"]
        st.markdown(ptxt.replace('|fill_variable|', f"2️⃣ Line #2 {'&nbsp;' * 5}: ") + wtxt.replace('|fill_variable|', wl2), True)

        wl3 = "No Winner" if GmDtl["Line3"]["whoWon"] == "" else GmDtl["Line3"]["whoWon"]
        st.markdown(ptxt.replace('|fill_variable|', f"3️⃣ Line #3 {'&nbsp;' * 5}: ") + wtxt.replace('|fill_variable|', wl3), True)
        
        wfh = "No Winner" if GmDtl["FullHouse"]["whoWon"] == "" else GmDtl["FullHouse"]["whoWon"]
        st.markdown(ptxt.replace('|fill_variable|', "🏚️ Full House: ") + wtxt.replace('|fill_variable|', wfh), True)

    for i in range(3): st.write("")    # vertical filler 
    st.markdown(horizontal_bar, True)

    if st.button("🔙 Return to Main Menu"):
        # shutil.rmtree("./" + mystate.GameDetails[0], ignore_errors=True)
        mystate.runpage = Main
        st.rerun()

def GeneratePlayerTicketNos():
    tkt_nos = []
    ntkt_nos = []
    for i in range(1, 91, 10): tkt_nos = tkt_nos + random.sample(range(i,i+10), random.randint(1,3))   # upto 3 nos for each batch of 10 from 1 to 90

    if len(tkt_nos) > 15:
        while len(ntkt_nos) < 15:
            tno = random.choice(tkt_nos)
            if tno not in ntkt_nos: ntkt_nos.append(tno)
        
        tkt_nos = ntkt_nos
    
    else:
        while len(tkt_nos) < 15:
            tno = random.randint(1,90)
            if tno not in tkt_nos: tkt_nos.append(tno)
    
    tkt_nos.sort()
    return tkt_nos

def PlayerBtnPress(vkey):
    if vkey in mystate.board_gen_no_lst: mystate.player_nos[vkey] = not mystate.player_nos[vkey] # btn_clicked
    else: st.toast(f"✋ :red[{vkey} is not yet part of the Game Board Numbers generated...]")

def ResetPlayerBtnColour():
    find_code = """<script>var elements = window.parent.document.querySelectorAll('button'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == '"""
    
    add_colour_code = """') elements[i].style.background = '#76d7c4'; } </script> """ 
    rmv_colour_code = """') elements[i].style.background = ''; } </script> """

    for key, clkd in mystate.player_nos.items():
        colour_code = add_colour_code if clkd == True else rmv_colour_code
        components.html(f"{find_code}{str(key).zfill(2)}{colour_code}", height=0, width=0)

def Jaldi5():
    knt = len([key for key, clkd in mystate.player_nos.items() if clkd == True])
    if knt < 5: st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no First 5 / Jaldi 5 win]")
    else:
        GmDtl = GameDiskFile("read")
        GmDtl["Jaldi5"]["isWon"] = True
        GmDtl["Jaldi5"]["whoWon"] = mystate.GameDetails[1]
        GameDiskFile("write", GmDtl)
        st.balloons()

def Line1():
    knt = len([key for key, clkd in mystate.player_nos.items() if clkd == True])
    if knt < 5: st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 1 win.]")
    else:
        line1_keys = list(mystate.player_nos.keys())[0:5]
        if set(line1_keys).issubset(mystate.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            GmDtl = GameDiskFile("read")
            GmDtl["Line1"]["isWon"] = True
            GmDtl["Line1"]["whoWon"] = mystate.GameDetails[1]
            GameDiskFile("write", GmDtl)
            st.balloons()
        
        else: st.toast(f"Your line #1 numbers are not part of the board numbers... :red[So no Line 1 win.]")

def Line2():
    knt = len([key for key, clkd in mystate.player_nos.items() if clkd == True])
    if knt < 5: st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 2 win.]")
    else:
        line2_keys = list(mystate.player_nos.keys())[5:10]
        if set(line2_keys).issubset(mystate.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            GmDtl = GameDiskFile("read")
            GmDtl["Line2"]["isWon"] = True
            GmDtl["Line2"]["whoWon"] = mystate.GameDetails[1]
            GameDiskFile("write", GmDtl)
            st.balloons()
        
        else: st.toast(f"Your line #2 numbers are not part of the board numbers... :red[So no Line 2 win.]")

def Line3():
    knt = len([key for key, clkd in mystate.player_nos.items() if clkd == True])
    if knt < 5: st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 3 win.]")
    else:
        line3_keys = list(mystate.player_nos.keys())[10:15]
        if set(line3_keys).issubset(mystate.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            GmDtl = GameDiskFile("read")
            GmDtl["Line3"]["isWon"] = True
            GmDtl["Line3"]["whoWon"] = mystate.GameDetails[1]
            GameDiskFile("write", GmDtl)
            st.balloons()
        
        else: st.toast(f"Your line #3 numbers are not part of the board numbers... :red[So no Line 3 win.]")

def FullHouse():
    knt = len([key for key, clkd in mystate.player_nos.items() if clkd == True])
    if knt < 15: st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no fullhouse win.]")
    else:
        fullhouse_keys = list(mystate.player_nos.keys())[0:15]
        if set(fullhouse_keys).issubset(mystate.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            GmDtl = GameDiskFile("read")
            GmDtl["FullHouse"]["isWon"] = True
            GmDtl["FullHouse"]["whoWon"] = mystate.GameDetails[1]
            GameDiskFile("write", GmDtl)
            st.balloons()
            tm.sleep(0.75)
            mystate.runpage = GameOver
            st.rerun()
        
        else: st.toast(f"All your ticket numbers are not part of the board numbers... :red[So no fullhouse win.]")

def PreCreation(what_to_create):
    if what_to_create == "Board":
        if "board_nos" not in mystate: mystate.board_nos = []
        
        mystate.board_gen_no_lst = []
        mystate.board_nos = [0]   # dummy 1st pstn to start next no at 1

        mystate.GameDetails[5] = False
        GameDiskFile("create")  # create a consolidated game file for each game

    if what_to_create == "Ticket":
        if "player_nos" not in mystate: mystate.player_nos = {}

        mystate.player_nos = {}
        tmp_player_nos = GeneratePlayerTicketNos()
        mystate.player_nos = {i: False for i in tmp_player_nos}

        mystate.GameDetails[10] = 0

        GmDtl = GameDiskFile("read")
        GmDtl["PlayerCount"] += 1       # Another new player

        if len(GmDtl['ExpiredBoardNumbers']) > 0: mystate.board_gen_no_lst = [int(x) for x in GmDtl['ExpiredBoardNumbers']]

        mystate.GameDetails[11] = GenUniqRndmAvatar(GmDtl)  
        GmDtl["UsedAvatars"].append(mystate.GameDetails[11])

        GameDiskFile("write", GmDtl)
        GameChat("on behalf of plyr", vtxt=f"Hey, I've joined the game. Please be prepared to lose, or be loose... 😉")

def GameChat(vkey, vtxt=""):
    chatfl = mystate.GameDetails[2] + "ChatHistory.txt"

    if vkey == "adminchat" or vkey == "plyrchat":
        vuser = "Admin" if vkey == "adminchat" else mystate.GameDetails[1]
        vavatar = "👺" if vuser == "Admin" else mystate.GameDetails[11]
        if mystate[vkey] != "":     # write gen no into txt file
            with open(chatfl, encoding="utf8", mode="a+") as f: f.write(f"{vavatar} {vuser} | {mystate[vkey]}\n")
            mystate[vkey] = ""
    
    elif vkey == "on behalf of admin" or vkey == "on behalf of plyr":
        vuser = "Admin" if vkey == "on behalf of admin" else mystate.GameDetails[1]
        vavatar = "👺" if vuser == "Admin" else mystate.GameDetails[11]
        if vtxt != "":              # write gen no into txt file
            with open(chatfl, encoding="utf8", mode="a+") as f: f.write(f"{vavatar} {vuser} | {vtxt}\n")

def ChatHistory():
    chat_history_rows = 4
    chatfl = mystate.GameDetails[2] + "ChatHistory.txt"
    if os.path.isfile(chatfl):
        dsp_lines = []
        with open(chatfl, encoding="utf8", mode="r") as f:   # write gen no into txt file
            f.seek(0)
            vlines = f.readlines()
        
        if len(vlines) <= chat_history_rows: dsp_lines = vlines
        else: dsp_lines = vlines[-chat_history_rows:]

        if len(dsp_lines) > 0:
            dsp_lines = [x.replace('\n', '') for x in dsp_lines]
            for i, vline in enumerate(dsp_lines): st.caption(f"{vline}")

def CreateNewTicket():
    ReduceGapFromPageTop()

    st.subheader(f"Game Ref. No. (GRN): :blue[{mystate.GameDetails[0]}] Ticket | Player: :blue[{mystate.GameDetails[1]}]:")
    st.markdown(horizontal_bar, True)

    tmp_player_nos = list(mystate.player_nos.keys())

    sc1, sc2, sc3, sc4 = st.columns((4,3,1,3))
    with sc3.container(): aftimer = st_autorefresh(interval=2000, key="aftmr")    # let iframe get generated in this container, owise it will add a blank line
    with sc4.container(): st.markdown(f"<img src='data:png;base64,{ReadPictureFile('TicketImg.png')}'>", unsafe_allow_html=True)
    with sc1.container():
        bn_ptr = -1
        for vrow in range(1,4):
            cols = st.columns((1,1,1,1,1,1))
            for vcol in range(1,6):
                bn_ptr += 1
                vkey = tmp_player_nos[bn_ptr]
                cols[vcol-1].button(str(vkey).zfill(2), key=str(vkey), on_click=PlayerBtnPress, args=(vkey,))

    with sc2.container():
        fc = 0
        GmDtl = GameDiskFile("read")
        ph = st.empty()

        if aftimer > 0:
            fc = GmDtl["CurrentNumber"]
            if fc != mystate.GameDetails[10]:
                mystate.GameDetails[10] = fc
                
                for snknt in range(10):     # spin number
                    spin_no = random.randint(1, 90)
                    ph.markdown(last_gen_no_colour.replace('|fill_variable|', str(spin_no).zfill(2)), True)
                    tm.sleep(0.03)

        if fc == 0: ph.markdown(last_gen_no_colour.replace('|fill_variable|', str(0).zfill(2)), True)
        else:
            if fc not in mystate.board_gen_no_lst: mystate.board_gen_no_lst.append(fc)
            ph.markdown(last_gen_no_colour.replace('|fill_variable|', str(fc).zfill(2)), True)
        
        sc21, sc22, sc23, sc24, sc25, sc26 = st.columns(6)
        sc21.button('5️⃣', help="First 5", disabled=GmDtl["Jaldi5"]["isWon"], on_click=Jaldi5)            # if file exists, someone has won jaldi5
        sc22.button('1️⃣', help="Line 1", disabled=GmDtl["Line1"]["isWon"], on_click=Line1)               # if file exists, someone has won line1
        sc23.button('2️⃣', help="Line 2", disabled=GmDtl["Line2"]["isWon"], on_click=Line2)               # if file exists, someone has won line2
        sc24.button('3️⃣', help="Line 3", disabled=GmDtl["Line3"]["isWon"], on_click=Line3)               # if file exists, someone has won line3
        sc25.button('🏚️', help="Full House", disabled=GmDtl["FullHouse"]["isWon"], on_click=FullHouse)   # if file exists, someone has won FullHouse
        if sc26.button('🔙', help="Terminate Play and Return"):
            GameChat("on behalf of plyr", vtxt=f"Sorry, I have to leave the game because I am lame. Bye... 😋")

            GmDtl = GameDiskFile("read")
            GmDtl["PlayerCount"] -= 1
            GameDiskFile("write", GmDtl)

            mystate.runpage = Main
            st.rerun()

    GmDtl = GameDiskFile("read")
    if len(GmDtl["ExpiredBoardNumbers"]) > 0:
        st.markdown(horizontal_dashed_bar, True)
        vexpired_no_knt = len(GmDtl['ExpiredBoardNumbers'])
        vpending_no_knt = (90 - vexpired_no_knt)
        st.info(f"Called-out Board Numbers (sorted): {GmDtl['ExpiredBoardNumbers']} | Pending Numbers: {vpending_no_knt}")

    ws = UpdtWinStatus(GmDtl)
    if ws != '': st.markdown(win_txt.replace('|fill_variable|', ws), True)

    # check if another player has finished the game or admin has aborted the game
    if GmDtl["GameOver"] == True or GmDtl["FullHouse"]["isWon"] == True or len(GmDtl['ExpiredBoardNumbers']) >= 89:
        mystate.runpage = GameOver
        st.rerun()
    
    if GmDtl["GameAborted"] == True:
        mystate.runpage = GameAborted
        st.rerun()

    st.markdown(horizontal_bar, True)

    if mystate.GameDetails[10] == 0: st.write("📢 :red[Please wait for the Admin to start the game...]")

    # User chat 
    st.text_input(f"{mystate.GameDetails[11]} Player Chat", placeholder=f"Say something, if required, {mystate.GameDetails[1]}...", key="plyrchat", on_change=GameChat, args=("plyrchat", ""))
    ChatHistory()

    st.markdown(horizontal_bar, True)
    ResetPlayerBtnColour()
    
def PlayPause():
    mystate.GameDetails[5] = not mystate.GameDetails[5]

    if mystate.GameDetails[5]: GameChat("on behalf of admin", vtxt="Game has been re/started...")
    else: GameChat("on behalf of admin", vtxt="Game has been paused...")

def NewGeneratedNumber(msgph):
    GmDtl = GameDiskFile("read")
    
    vno = GenUniqRndmNo()
    mystate.board_nos[vno].markdown(selected_no_colour.replace('|fill_variable|', str(vno).zfill(2)), True)

    GmDtl["CurrentNumber"] = vno
    GmDtl["ExpiredBoardNumbers"].append(str(vno).zfill(2))
    GmDtl["ExpiredBoardNumbers"].sort()
    GameDiskFile("write", GmDtl)

    msgph.empty()

def UpdtWinStatus(GmDtl):
    winstr = ''

    if GmDtl["Jaldi5"]["isWon"] == True: winstr += f"5️⃣: {GmDtl['Jaldi5']['whoWon']} | "
    if GmDtl["Line1"]["isWon"] == True: winstr += f"1️⃣: {GmDtl['Line1']['whoWon']} | "
    if GmDtl["Line2"]["isWon"] == True: winstr += f"2️⃣: {GmDtl['Line2']['whoWon']} | "
    if GmDtl["Line3"]["isWon"] == True: winstr += f"3️⃣: {GmDtl['Line3']['whoWon']} | "
    if GmDtl["FullHouse"]["isWon"] == True: winstr += f"🏚️: {GmDtl['FullHouse']['whoWon']} | "
        
    if len(winstr) > 0: winstr = 'Win Status: ' + winstr[:-3]   # rmv trailing spc|spc

    return winstr

def CreateNewBoard():
    ReduceGapFromPageTop()
    st.subheader(f"Game Reference Number (GRN: :blue[{mystate.GameDetails[0]}]):")

    GmDtl = GameDiskFile("read")
    vexpired_no_knt = len(GmDtl["ExpiredBoardNumbers"])
    if vexpired_no_knt == 23: GameChat("on behalf of admin", vtxt="25% of the game has been completed. Anyone's winning...?")
    elif vexpired_no_knt == 45: GameChat("on behalf of admin", vtxt="50% of the game has been completed. More winners, please...")
    elif vexpired_no_knt == 68: GameChat("on behalf of admin", vtxt="75% of the game has been completed. Anyone's sweating...?")

    sc1, sc2 = st.columns((2,1))
    with sc2.container():
        sc21, sc22 = st.columns((1,1))
        sc21.markdown(f"""<img src="data:png;base64,{ReadPictureFile('MainBoard.png')}" width="140" height="100" >""", True)
        sc22.markdown("""<span style="font-size: 32px; font-weight: bold; text-align: center;">Housie Gameboard: </span>""", True)
        st.markdown("<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px dashed #635985;'>", True)

        st.text_input("👺 Admin Chat", placeholder="Say something, Admin...", key="adminchat", on_change=GameChat, args=("adminchat", ""))
        ChatHistory()

        if GmDtl["PlayerCount"] == 0:
            st.caption(f"📢 :red[This game currently has {GmDtl['PlayerCount']} players. Players need to connect with the above GRN. Please wait until they do...]")

    with sc1.container():
        bn_ptr = 0
        gap_spc = 1
        for vrow in range(1,10):    # dont include 91-99
            cols = st.columns((1,1,1,1,1,1,1,1,1,1,gap_spc))
            for vcol in range(0,10):
                bn_ptr += 1
                btnobj = None
                
                if bn_ptr not in mystate.board_gen_no_lst:
                    btnobj = cols[vcol].markdown(normal_no_colour.replace('|fill_variable|', str(bn_ptr).zfill(2)), True)
                else: btnobj = cols[vcol].markdown(selected_no_colour.replace('|fill_variable|', str(bn_ptr).zfill(2)), True)
                
                mystate.board_nos.append(btnobj)

    st.markdown(horizontal_bar, True)
    c1, c2, c3 = st.columns((1, 1, 15))
    
    if len(mystate.board_gen_no_lst) > 0:
        winstats = c3.empty()
        if GmDtl != {}:
            winstr = UpdtWinStatus(GmDtl)
            if winstr != "": winstats.markdown(win_txt.replace('|fill_variable|', winstr), True)
        
        elif mystate.GameDetails[9] != "": winstats.markdown(mystate.GameDetails[9], True)

    msgph = st.empty()
    mbtn_dsble = True if len(GmDtl["ExpiredBoardNumbers"]) >= 90 else False
    if mystate.GameDetails[3] == "manual":
        msgph.write(":blue[Waiting to generate next board number with manual button click...]")
        c1.button("🔄", help="Generate another board number", key='gan', on_click=NewGeneratedNumber, args=(msgph,), disabled=mbtn_dsble)

    else: # auto mode
        if mystate.GameDetails[5] == False: msgph.write(":blue[Waiting to generate next board number with manual button click...]")

        c1.button("⏯", help="Play / pause auto number generation.", on_click=PlayPause)
        if mystate.GameDetails[5] == True:
            if mbtn_dsble == False:
                msgph.write(":blue[Generating next board number in a few seconds...]")
                gentimer = st_autorefresh(interval=mystate.GameDetails[4] * 1000, limit=91, key="gentmr")
                if gentimer > 0: NewGeneratedNumber(msgph)
    
    if c2.button("🔙", help="Return to Main Menu"):
        GmDtl = GameDiskFile("read")
        if len(GmDtl["ExpiredBoardNumbers"]) < 89:
            GmDtl["GameAborted"] = True
            GameDiskFile("write", GmDtl)
            mystate.runpage = GameAborted
            st.rerun()

    if len(mystate.board_gen_no_lst) >= 89:
        GmDtl["GameOver"] = True
        GameDiskFile("write", GmDtl)
        mystate.runpage = Main

def GameSettings():
    ReduceGapFromPageTop()

    st.subheader('🛠️ Game Settings:')
    st.markdown(horizontal_bar, True)
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    c1, c2, c3 = st.columns((2,1,7))
    w1hlp = "Set the main board number generation to manual/auto"
    w2hlp = "Seconds interval between each main board number generation when in auto mode"
    w3hlp = "Play a beep for each new number generated on the board and ticket."
    vbr = c1.radio("Board Run", ("", "manual", "auto"), index=2, horizontal=True, help=w1hlp)
    vam_dsble = True if vbr == "manual" else False
    vam = c2.number_input("Seconds", min_value=1.00, max_value=10.00, value=6.00, step=0.25, disabled=vam_dsble, help=w2hlp)
    btn_dsbld = True if vbr == "" else False
    vsnd = st.radio("Sounds for new number generation", ('No', 'Yes'), index=0, horizontal=True, help=w3hlp, disabled=True)
    st.markdown(horizontal_bar, True)

    sc1, sc2, sc3 = st.columns((2,3,10))
    if sc1.button("💾 Save Settings", disabled=btn_dsbld):
        mystate.GameDetails[3] = vbr
        mystate.GameDetails[4] = vam
        mystate.GameDetails[5] = True if vbr == "auto" else False
        mystate.GameDetails[6] = False if vsnd == 'No' else True
        st.info("☑️ Settings update completed.")

        tm.sleep(0.75)
        mystate.runpage = Main
        st.rerun()

    if sc2.button("🔙 Return to Main Page"):
        mystate.runpage = Main
        st.rerun()

def NewTicketCallback(gm_ref, plyr_nme):
    mystate.GameDetails[0] = gm_ref
    mystate.GameDetails[1] = plyr_nme
    mystate.GameDetails[2] = vpth + gm_ref + '/'  # Game Path

def Main():
    st.markdown('<style>[data-testid="stSidebar"]{min-width: 288px;}</style>', unsafe_allow_html=True,) # set min sidebar width

    main_page_image = Image.open('MainPage.png').resize((1000, 650))
    st.image(main_page_image, use_column_width='auto')

    with st.sidebar:
        ticket_icon = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                         <i class="fa-solid fa-ticket">&nbsp;&nbsp;
                         </i> <span style="font-size: 18px; font-weight: bold;">Housie | Tambola | Bingo:</span>'''

        st.markdown(ticket_icon, unsafe_allow_html=True)

        st.markdown(horizontal_bar, True)
        sc01, sc02 = st.columns(2)
        game_rules = sc01.button(f"📚 Rules", use_container_width=True)
        game_settings = sc02.button(f"🛠️ Settings", use_container_width=True)
        new_game = st.button(f"🎲 New Game Board", use_container_width=True)
        
        new_tkt = False
        sc1, sc2 = st.columns((3,1))
        sc1.markdown("", True)
        sc1.markdown("🎟️ New Game Ticket", True)
        if sc2.button("🔄", help="Refresh Games List / GRNs"): st.rerun()

        # new ticket for an existing game
        files_in_path = os.listdir(".")     # current workspace
        gm_fldr_lst = [x for x in files_in_path if not os.path.isfile(x) and x.startswith('HG_')] # chk if folders in dir; only ones that start w/HG_
        with st.expander("Player Options", True):
            if len(gm_fldr_lst) > 0:
                gm_ref = st.selectbox("👇 Choose Game Ref. No. (GRN): :red[*]", gm_fldr_lst, index=None, placeholder="Choose a game to play", help="Choose a game for which a ticket needs to be created")
                plyr_nme = st.text_input("👨🏻‍💼 Player Name: :red[*]")
                ntdsbld = True if gm_ref == '' or plyr_nme == '' else False
                new_tkt = st.button("⚙️ Generate Game Ticket", on_click=NewTicketCallback, args=(gm_ref, plyr_nme), disabled=ntdsbld, use_container_width=True)
                if new_tkt:
                    PreCreation("Ticket")
                    mystate.runpage = CreateNewTicket
                    st.rerun()

        if len(gm_fldr_lst) > 0:
            sc21, sc22 = st.columns((3,1))
            gm_ref2 = sc21.selectbox("Delete GRN:", gm_fldr_lst, index=None, placeholder="Delete which game?", label_visibility="collapsed")
            ntdsbld2 = True if gm_ref2 == None else False
            if sc22.button("🚮", help="👇 Choose a completed game to delete.", disabled=ntdsbld2):
                shutil.rmtree("./" + gm_ref2, ignore_errors=True)
                st.rerun()

        if game_settings == True:
            mystate.runpage = GameSettings
            st.rerun()

        elif game_rules == True:
            mystate.runpage = ViewHelp
            st.rerun()

        elif new_game == True:
            gm_fldr_nme = "HG_" + GenerateRandomCode()  # Game project folder

            subdircreated = CreateSubDir(gm_fldr_nme)
            if not subdircreated:
                mystate.GameDetails[0] = gm_fldr_nme
                mystate.GameDetails[2] = vpth + gm_fldr_nme + '/'  # Game Path

                PreCreation("Board")
                mystate.runpage = CreateNewBoard
                st.rerun()
        
            else: st.error("😲 Couldnt create game folder. Unknown Error.")

    st.sidebar.markdown(horizontal_bar, True)    
    author_dtl = "<strong>😎 Shawn Pereira: Happy Playing:<br>shawnpereira1969@gmail.com</strong>"
    st.sidebar.markdown(author_dtl, unsafe_allow_html=True)

def HelpHeader(hdr_txt, icon_dtl):
    vhdr = f'''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                         {icon_dtl}&nbsp;&nbsp;
                         <span style="font-size: 28px; font-weight: bold;">{hdr_txt}:</span>'''
    return vhdr

def ViewHelp():
    ReduceGapFromPageTop()
    st.markdown(purple_btn_colour, unsafe_allow_html=True) 
    st.sidebar.header("🤔 Game Help:")

    hlp_dtl = [''] * 5
    hlp_dtl[0] = """<span style="font-size: 20px;">
    <strong>New Game Board:<br></strong>
    <ol>
    <li style="font-size:18px";>Admin to open browser tab.</li>
    <li style="font-size:18px";>Load game.</li>
    <li style="font-size:18px";>Choose New Game Board.</li>
    <li style="font-size:18px";>Inform players about Game Reference Number (GRN).</li>
    <li style="font-size:18px";>Click on Play/Pause to start (play) board number generation, after all players have connected to the game.</li>
    <li style="font-size:18px";>It is a good practice to delete a game after game play, using its GRN.</li>
    </ol></span>""" + """<span style="font-size: 20px;">
    <strong>New Player Ticket:<br></strong>
    <ol>
    <li style="font-size:18px";>Each player to open separate browser tab, only after the Game Board has been created and is alive.</li>
    <li style="font-size:18px";>Load game.</li>
    <li style="font-size:18px";>Choose Game Reference Number (GRN) provided by Admin.</li>
    <li style="font-size:18px";>Enter player name.</li>
    <li style="font-size:18px";>Create Game Ticket.</li>
    <li style="font-size:18px";>Refresh window (🔄) if GRN and/or Player name options are not seen.</li>
    </ol></span>
    """ + """<span style="font-size: 20px;"><strong>Note: </strong>For any given game, the Tickets are to be created only after the Game Board has been created.</span><br><br>"""

    hlp_dtl[1] = """<span style="font-size: 20px;">
    You can use this section to do the following:<br><ul>
    <li style="font-size:18px";>Set the numbers to be randomly generated on the board, to be automatic or manual. <i>Default: Automatic</i>.</li>
    <li style="font-size:18px";>For automatic, you will need to specify the time interval (seconds) between the generation of two numbers. <i>Default: 6.0 seconds</i>.</li>
    <li style="font-size:18px";>You can activate sounds to provide feedback after each number is generated. (Temporarily deactivated because of cloud service compatibility.)</li>
    </ul></span>
    """

    hlp_dtl[2] = """<span style="font-size: 20px;">
    The following prizes / wins are considered in this game:<br><ul>
    <li style="font-size:18px";><strong>Early 5 / Jaldi 5</strong>: These are the first 5 numbers, matched by the player against the board generated numbers, denoted by the button symbol 5️⃣ on the ticket.</li>
    <li style="font-size:18px";><strong>Line 1</strong>: These are the 5 line numbers of line <i>#1</i>, matched by the player against the board generated numbers, denoted by the button symbol 1️⃣ on the ticket.</li>
    <li style="font-size:18px";><strong>Line 2</strong>: These are the 5 line numbers of line <i>#2</i>, matched by the player against the board generated numbers, denoted by the button symbol 2️⃣ on the ticket.</li>
    <li style="font-size:18px";><strong>Line 3</strong>: These are the 5 line numbers of line <i>#3</i>, matched by the player against the board generated numbers, denoted by the button symbol 3️⃣ on the ticket.</li>
    <li style="font-size:18px";><strong>Full House</strong>: These are all the 15 line numbers of all 3 lines, matched by the player against the board generated numbers, denoted by the button symbol 🏚️ on the ticket.</li>
    </ul>
    On any win, the first player to press the buttons denoted by the above symbols (in the case on multiple wins per option), will be considered the winner for that option (line 1, 2, 3...) 
    </span>
    """

    hlp_dtl[3] = """<span style="font-size: 20px;">
    <ul>
    <li style="font-size:18px";>A New Game Board must be created before any tickets (for that game) can be created.</li>
    <li style="font-size:18px";>The newly created game board will be auto-assigned a unique Game Reference Number (GRN). Eg. HG_0ER8AH.</li>
    <li style="font-size:18px";>This GRN must be communicated to all players, so that they can connect and create tickets against that particular game.</li>
    <li style="font-size:18px";>The new game board will consist of numbers between 1-90. Random numbers will be generated between these number limits every n seconds, for the players to match against their individual tickets. </li>
    <li style="font-size:18px";>The Play/Pause button will need to be clicked to start the game board number run. Thereafter, the next numbers will generate by either (a) repeated clicks of this button (manual mode) or (b) automatically, as per the time interval (seconds) as defined in the game settings (Default: 6 seconds).</li>
    <li style="font-size:18px";>If the back button is pressed during game play, the game will be aborted and game play for all players will terminate thereafter.</li>
    <li style="font-size:18px";>The Admin. has a monologue text chat option to broadcast messages to all the players.</li>
    </ul></span>
    """

    hlp_dtl[4] = """<span style="font-size: 20px;">
    <ul>
    <li style="font-size:18px";>Before creating a new ticket, a player must choose a game to play in and provide his/her name.</li>
    <li style="font-size:18px";>It is suggested that all players have unique names to differentiate between them during wins.</li>
    <li style="font-size:18px";>If a player wrongly chooses a game that has already started, or has joined in late, he/she will need to catch up on all the numbers generated during that game run until that point of entry. Such a player / any other player can at anytime exit the game.</li>
    <li style="font-size:18px";>Each player ticket will consist of a random set of 15 numbers, set in 3 rows of 5 numbers each.</li>
    <li style="font-size:18px";>The player will sequentially see all the numbers generated on the board after either the (a) time interval set in the games setting in the automatic mode, or after the (b) button press on the game board in the manual mode (by an Admin.).</li>
    <li style="font-size:18px";>All the board numbers can be seen at the bottom of the ticket, sorted ascendingly.</li>
    <li style="font-size:18px";>If the player presses a number on his/her ticket, that is not generated by the game board, a warning message will display at the bottom right of the player’s screen.</li>
    <li style="font-size:18px";>Only board generated numbers can be clicked by each player. Clicking such numbers will turn them green on the ticket.</li>
    <li style="font-size:18px";>Please refer to the Prizes / Wins section for how to declare a win.</li>
    <li style="font-size:18px";>Each player has a text chat option to broadcast messages to all other players. Chat display history is set at the last 5 chats.</li>
    </ul></span>
    """

    icon_optns = ('<i class="fa-solid fa-hands-asl-interpreting fa-xl"></i>', 
                  '<i class="fa-solid fa-screwdriver-wrench fa-xl"></i>', 
                  '<i class="fa-solid fa-gifts fa-xl"></i>', 
                  '<i class="fa-solid fa-table-cells fa-xl"></i>', 
                  '<i class="fa-solid fa-ticket fa-xl"></i>')
    hlp_optns = ('Game Overview', 'Game Settings', 'Prizes | Wins', 'New Game Board', 'New Game Ticket')
    vhradio = st.sidebar.radio("Help Topic:", options=hlp_optns, index=None)
    
    if vhradio in hlp_optns:
        idx = int(hlp_optns.index(vhradio))
        vicon_dtls = icon_optns[idx]
        vftxt = HelpHeader(vhradio, vicon_dtls)

        st.markdown(vftxt, unsafe_allow_html=True)
        st.markdown(horizontal_bar, True)
        st.markdown(hlp_dtl[idx], unsafe_allow_html=True)
        st.markdown(horizontal_bar, True)

    else:
        game_help_image = Image.open('GameHelp.png').resize((1000, 650))
        st.image(game_help_image, use_column_width='auto')

    if st.sidebar.button("🔙 Return to Main Page"):
        mystate.runpage = Main        
        st.rerun()

def LandingPage():
    ReduceGapFromPageTop()
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    bkgrnd_img = f"{vpth}/LandingPage.jpg"
    bkgrnd_img_ext = bkgrnd_img[-4:-1]
    img_code = f"""<style>
                        .stApp {{
                            background: url(data:image/{bkgrnd_img_ext};base64,{base64.b64encode(open(bkgrnd_img, 'rb').read()).decode()});
                            background-repeat: no-repeat;
                            background-attachment: fixed;
                            background-size: 100% 100%;
                        }}
                    </style>"""

    st.markdown(img_code, unsafe_allow_html=True)
    c1, c2 = st.columns((8,3))
    for i in range(38): c2.write("")    # vertical filler

    mystate.GameDetails[7] = load_number_animation()
    if c2.button("Press a key to continue..."): # bypass time delay
        mystate.runpage = Main
        st.rerun()

    tm.sleep(8)
    mystate.runpage = Main
    st.rerun()

if 'runpage' not in mystate:
    # ClearExpiredGameFolders()
    mystate.runpage = LandingPage

mystate.runpage()