import streamlit as st
import streamlit.components.v1 as components
import base64
import os
import time as tm
from datetime import datetime as dt, timedelta
import random
from PIL import Image
import shutil
from streamlit_autorefresh import st_autorefresh
from notifypy import Notify     # pip install notify-py
import pandas as pd

st.set_page_config(page_title = "Housie", page_icon="🔢", layout = "wide", initial_sidebar_state = "expanded")

vDrive = os.path.splitdrive(os.getcwd())[0]
if vDrive == "C:":
    vpth = "C:/Users/Shawn/dev/utils/housie/"   # local developer's disc
else:
    vpth = "./"

purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"    # thin divider line
horizontal_dashed_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px dashed #635985;'><br>"    # thin divider line

if "board_gen_no_lst" not in st.session_state:
    st.session_state.board_gen_no_lst = []

if "WinStatus" not in st.session_state:
    st.session_state.WinStatus = [''] * 5  # 0: Jaldi5, Line1, Line2, Line3, Fullhouse

# 0: Game No, 1: Player Name, 2: Game Path, 3: auto/manual num gen, 4: sec interval for autogen, 5: auto/man = true/false, 6: playsound 
if "GameDetails" not in st.session_state:   
    st.session_state.GameDetails = ['XP17', 'Shawn', '', 'auto', 6.0, False, True]

if "disp_player_no" not in st.session_state:
    st.session_state.disp_player_no = 0

if "mydf" not in st.session_state:
    st.session_state.mydf = pd.DataFrame()

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
                                     font-size: 24px;
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

notification = Notify()
notification.title = "Housie Number"
# notification.icon = vpth + "Speak.png"

def ReduceGapFromPageTop():
    st.markdown(" <style> div[class^='block-container'] { padding-top: 3rem; } </style> ", unsafe_allow_html=True)  # reduce gap from page top

def ReadPictureFile(wch_fl):
    try:
        pxfl = f"{vpth}{wch_fl}"
        return base64.b64encode(open(pxfl, 'rb').read()).decode()

    except:
        return ""

def CreateSubDir(wch_sub_folder):
    vfull_dir_path = f"{vpth}/{wch_sub_folder}"
    chk_if_subdir_exists = os.path.isdir(vfull_dir_path)

    if not chk_if_subdir_exists:
        os.makedirs(vfull_dir_path)
        return False
    
def ClearExpiredGameFolders():
    # chk for game folders in current dir
    # delete if dt of previous_board_number.txt is less than today (for orphaned games)

    files_in_path = os.listdir(".")     # current workspace
    gm_fldr_lst = [x for x in files_in_path if not os.path.isfile(x) and x.startswith('HG')] # chk if folders in dir; only ones that start w/HG

    for gm_fldr in gm_fldr_lst:
        chkfl = vpth + gm_fldr + '/previous_board_number.txt'
        if os.path.isfile(chkfl):
            sttm = os.path.getmtime(chkfl)
            sttm = dt.fromtimestamp(sttm)

            # determine game folder validity as 2 hours since last time previous_board_number.txt file was updated
            if sttm + timedelta(hours=2) < dt.now():	# current time > start time + 2 hours; del (expired) game folder
                shutil.rmtree("./" + gm_fldr)

def GenUniqRndmNo():
    while True:
        vno = random.randint(1,90)
        if vno not in st.session_state.board_gen_no_lst:
            st.session_state.board_gen_no_lst.append(vno)
            break
    return vno

def GameAborted():
    ReduceGapFromPageTop()
    st.subheader(f"👾 Game Ref. No. (GRN): :blue[{st.session_state.GameDetails[0]}]:")
    st.markdown(horizontal_bar, True)
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    for i in range(2):
        st.write("")    # vertical filler

    sc1, sc2, sc3 = st.columns((3,3,6))

    with sc1.container():
        st.markdown(f"<img src='data:png;base64,{ReadPictureFile('GameAborted.png')}'>", unsafe_allow_html=True)

    with sc2.container():
        st.write("")
        st.subheader("🙋🏻‍♂️ Game Aborted:")

        st.markdown("The Admin. 👨🏼‍⚖️ has been aborted <br>in the game, please take note 📝.", True)
        st.write("Be a sport 🤸🏻‍♂️, don't be a goat 🐐.")
        st.write("")

        if sc2.button("🔙 Return to Main Page"):
            st.session_state.player_nos = {}

            tmp_player_nos = GeneratePlayerNos()
            for vkey in tmp_player_nos:
                st.session_state.player_nos[vkey] = False

            st.session_state.runpage = Main
            st.experimental_rerun()

    for i in range(3):
        st.write("")    # vertical filler 
    st.markdown(horizontal_bar, True)

def GameOver():
    ReduceGapFromPageTop()
    st.subheader(f"👾 Game Ref. No. (GRN): :blue[{st.session_state.GameDetails[0]}]:")
    st.markdown(horizontal_bar, True)

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

    for i in range(3):
        st.write("")    # vertical filler

    sc1, sc2, sc3 = st.columns((1,2,3))

    with sc2.container():
        st.markdown(f"<img src='data:png;base64,{ReadPictureFile('GameOver.png')}'>", unsafe_allow_html=True)

    with sc3.container():
        st.subheader("🏆 Win Status:")

        st.markdown(ptxt.replace('|fill_variable|', "5️⃣ Early 5 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ") + wtxt.replace('|fill_variable|', st.session_state.WinStatus[0]), True)
        st.markdown(ptxt.replace('|fill_variable|', "1️⃣ Line #1 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ") + wtxt.replace('|fill_variable|', st.session_state.WinStatus[1]), True)
        st.markdown(ptxt.replace('|fill_variable|', "2️⃣ Line #2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ") + wtxt.replace('|fill_variable|', st.session_state.WinStatus[2]), True)
        st.markdown(ptxt.replace('|fill_variable|', "3️⃣ Line #3 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;: ") + wtxt.replace('|fill_variable|', st.session_state.WinStatus[3]), True)
        st.markdown(ptxt.replace('|fill_variable|', "🏚️ Full House: ") + wtxt.replace('|fill_variable|', st.session_state.WinStatus[4]), True)

    for i in range(3):
        st.write("")    # vertical filler 
    st.markdown(horizontal_bar, True)

def GetPlayerNo():
    if os.path.isfile(st.session_state.GameDetails[2] + 'previous_board_number.txt'):
        mdttm = os.path.getmtime(st.session_state.GameDetails[2] + 'previous_board_number.txt')
        mdttm = dt.fromtimestamp(mdttm)
        if mdttm > st.session_state.lst_tkt_no_read_dttm:
            with open(st.session_state.GameDetails[2] + 'previous_board_number.txt', 'r') as f:   # write gen no into txt file
                fc = int(f.read())
            st.session_state.lst_tkt_no_read_dttm = mdttm
        
        else:
            return 0
    
    else:
        return 0

def GeneratePlayerNos():
    tkt_nos = []
    ntkt_nos = []
    for i in range(1, 91, 10):
        tkt_nos = tkt_nos + random.sample(range(i,i+10), random.randint(1,3))   # upto 3 nos for each batch of 10 from 1 to 90

    if len(tkt_nos) > 15:
        while len(ntkt_nos) < 15:
            tno = random.choice(tkt_nos)
            if tno not in ntkt_nos:
                ntkt_nos.append(tno)
        
        tkt_nos = ntkt_nos
    
    else:
        while len(tkt_nos) < 15:
            tno = random.randint(1,90)
            st.warning(f"tno: {tno} | {tno not in tkt_nos}")

            if tno not in tkt_nos:
                tkt_nos.append(tno)
    
    tkt_nos.sort()
    return tkt_nos

def PlayerBtnPress(vkey):
    if vkey in st.session_state.board_gen_no_lst:
        st.session_state.player_nos[vkey] = not st.session_state.player_nos[vkey] # btn_clicked
    
    else:
        st.toast(f"✋ :red[{vkey} is not yet part of the Game Board Numbers generated...]")

def ResetPlayerBtnColour():
    find_code = """<script>var elements = window.parent.document.querySelectorAll('button'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == '"""
    
    add_colour_code = """') elements[i].style.background = '#AED581'; } </script> """ 
    rmv_colour_code = """') elements[i].style.background = ''; } </script> """

    for key, clkd in st.session_state.player_nos.items():
        colour_code = add_colour_code if clkd == True else rmv_colour_code
        components.html(f"{find_code}{str(key).zfill(2)}{colour_code}", height=0, width=0)

def Jaldi5():
    knt = len([key for key, clkd in st.session_state.player_nos.items() if clkd == True])
    if knt < 5:
        st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no First 5 win]")
    
    else:
        st.session_state.WinStatus[0] = st.session_state.GameDetails[1]
        with open(st.session_state.GameDetails[2] + 'jaldi5.txt', 'w') as f:   # write gen no into txt file
            f.write(st.session_state.GameDetails[1])
        st.balloons()

def Line1():
    knt = len([key for key, clkd in st.session_state.player_nos.items() if clkd == True])
    if knt < 5:
        st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 1 win.]")
    
    else:
        line1_values = list(st.session_state.player_nos.values())[0:5]
        if set(line1_values).issubset(st.session_state.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            st.session_state.WinStatus[1] = st.session_state.GameDetails[1]
            with open(st.session_state.GameDetails[2] + 'line1.txt', 'w') as f:   # write gen no into txt file
                f.write(st.session_state.GameDetails[1])
            st.balloons()
        
        else:
            st.toast(f"Your line #1 numbers are not part of the board numbers... :red[So no Line 1 win.]")

def Line2():
    knt = len([key for key, clkd in st.session_state.player_nos.items() if clkd == True])
    if knt < 5:
        st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 2 win.]")
    
    else:
        line1_values = list(st.session_state.player_nos.values())[5:10]
        if set(line1_values).issubset(st.session_state.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            st.session_state.WinStatus[2] = st.session_state.GameDetails[1]
            with open(st.session_state.GameDetails[2] + 'line2.txt', 'w') as f:   # write gen no into txt file
                f.write(st.session_state.GameDetails[1])
            st.balloons()
        
        else:
            st.toast(f"Your line #2 numbers are not part of the board numbers... :red[So no Line 2 win.]")

def Line3():
    knt = len([key for key, clkd in st.session_state.player_nos.items() if clkd == True])
    if knt < 5:
        st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no Line 3 win.]")
    
    else:
        line1_values = list(st.session_state.player_nos.values())[10:15]
        if set(line1_values).issubset(st.session_state.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            st.session_state.WinStatus[3] = st.session_state.GameDetails[1]
            with open(st.session_state.GameDetails[2] + 'line3.txt', 'w') as f:   # write gen no into txt file
                f.write(st.session_state.GameDetails[1])
            st.balloons()
        
        else:
            st.toast(f"Your line #3 numbers are not part of the board numbers... :red[So no Line 3 win.]")

def FullHouse():
    knt = len([key for key, clkd in st.session_state.player_nos.items() if clkd == True])
    if knt < 15:
        st.toast(f"Your ticket has only :red[{knt}] numbers selected so far... :red[So no fullhouse win.]")
    
    else:
        line1_values = list(st.session_state.player_nos.values())[10:15]
        if set(line1_values).issubset(st.session_state.board_gen_no_lst) == True: # all elements of list 1 are contained in list 2
            st.session_state.WinStatus[4] = st.session_state.GameDetails[1]
            with open(st.session_state.GameDetails[2] + 'fullhouse.txt', 'w') as f:   # write gen no into txt file
                f.write(st.session_state.GameDetails[1])
            st.balloons()
            tm.sleep(0.75)
            st.session_state.runpage = GameOver
            st.experimental_rerun()
        
        else:
            st.toast(f"Your line #3 numbers are not part of the board numbers... :red[So no fullhouse win.]")

def CreateNewTicket():
    ReduceGapFromPageTop()
    st.subheader(f"Game Ref. No. (GRN): :blue[{st.session_state.GameDetails[0]}] Ticket | Player: :blue[{st.session_state.GameDetails[1]}]:")
    st.markdown(horizontal_bar, True)

    tmp_player_nos = list(st.session_state.player_nos.keys())

    sc1, sc2, sc3, sc4 = st.columns((4,3,1,3))
    with sc4.container():
        st.markdown(f"<img src='data:png;base64,{ReadPictureFile('TicketImg.png')}'>", unsafe_allow_html=True)

    with sc1.container():
        for i in range(3):
            st.write('') # vertical filler

        bn_ptr = -1
        for vrow in range(1,4):
            cols = st.columns((1,1,1,1,1,1))
            for vcol in range(1,6):
                bn_ptr += 1
                vkey = tmp_player_nos[bn_ptr]
                cols[vcol-1].button(str(vkey).zfill(2), key=str(vkey), on_click=PlayerBtnPress, args=(vkey,))

    fc = 0
    with sc2.container():
        aftimer = st_autorefresh(interval=2000, key="aftmr")
        if aftimer > 0:
            if os.path.isfile(st.session_state.GameDetails[2] + 'previous_board_number.txt'):
                mdttm = os.path.getmtime(st.session_state.GameDetails[2] + 'previous_board_number.txt')
                mdttm = dt.fromtimestamp(mdttm)
                if mdttm > st.session_state.lst_tkt_no_read_dttm or fc == 0:
                    with open(st.session_state.GameDetails[2] + 'previous_board_number.txt', 'r') as f:   # write gen no into txt file
                        fc = int(f.read())
                        if fc != st.session_state.disp_player_no:
                            st.session_state.disp_player_no = fc
                            if st.session_state.GameDetails[6] == True:
                                try:
                                    vndesc = st.session_state.mydf['Description'].where(st.session_state.mydf['No'] == fc).dropna().tolist()[0]
                                    
                                    notification.message = vndesc
                                    notification.audio = vpth + f"{fc}.wav"
                                    notification.icon = vpth + random.choice(["Speak1.png", "Speak2.png", "Speak3.png", "Speak4.png", "Speak5.png"])
                                    notification.send(block=False)
                                
                                except:
                                    pass

        if len(st.session_state.board_gen_no_lst) > 0:
            st.markdown(last_gen_no_colour.replace('|fill_variable|', str(st.session_state.disp_player_no).zfill(2)), True)
        else:
            st.markdown(last_gen_no_colour.replace('|fill_variable|', str(0).zfill(2)), True)
        
        sc21, sc22, sc23, sc24, sc25, sc26 = st.columns(6)
        
        j5dsbld = True if st.session_state.WinStatus[0]  != '' else False    # if file exists, someone has won jaldi5
        sc21.button('5️⃣', help="First 5", disabled=j5dsbld, on_click=Jaldi5)

        l1dsbld = True if st.session_state.WinStatus[1]  != '' else False    # if file exists, someone has won line1
        sc22.button('1️⃣', help="Line 1", disabled=l1dsbld, on_click=Line1)

        l2dsbld = True if st.session_state.WinStatus[2]  != '' else False    # if file exists, someone has won line2
        sc23.button('2️⃣', help="Line 2", disabled=l2dsbld, on_click=Line2)

        l3dsbld = True if st.session_state.WinStatus[3]  != '' else False    # if file exists, someone has won line3
        sc24.button('3️⃣', help="Line 3", disabled=l3dsbld, on_click=Line3)

        fhdsbld = True if st.session_state.WinStatus[4]  != '' else False    # if file exists, someone has won FullHouse
        sc25.button('🏚️', help="Full House", disabled=fhdsbld, on_click=FullHouse)

        if sc26.button('🔙', help="Terminate Play and Return"):
            st.session_state.runpage = Main
            st.experimental_rerun()

    if len(st.session_state.board_gen_no_lst) >= 1:
        st.markdown(horizontal_dashed_bar, True)

    if st.session_state.WinStatus[0] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'jaldi5.txt'):  # F5 won by some other player
        with open(st.session_state.GameDetails[2] + 'jaldi5.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[0] = f.read().strip()

    if st.session_state.WinStatus[1] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line1.txt'):  # L1 won by some other player
        with open(st.session_state.GameDetails[2] + 'line1.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[1] = f.read().strip()

    if st.session_state.WinStatus[2] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line2.txt'):  # L2 won by some other player
        with open(st.session_state.GameDetails[2] + 'line2.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[2] = f.read().strip()

    if st.session_state.WinStatus[3] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line3.txt'):  # L3 won by some other player
        with open(st.session_state.GameDetails[2] + 'line3.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[3] = f.read().strip()

    if st.session_state.WinStatus[4] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'fullhouse.txt'):  # FH won by some other player
        with open(st.session_state.GameDetails[2] + 'fullhouse.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[4] = f.read().strip()
        st.session_state.runpage = GameOver
        st.experimental_rerun()
    
    if os.path.isfile(st.session_state.GameDetails[2] + 'abortgame.txt'): 
        st.session_state.runpage = GameAborted
        st.experimental_rerun()

    ws = UpdtWinStatus()
    if ws != '':
        st.markdown(win_txt.replace('|fill_variable|', ws), True)

    if os.path.isfile(st.session_state.GameDetails[2] + 'board_number_list.txt'):
        with open(st.session_state.GameDetails[2] + 'board_number_list.txt', 'r') as f:   # write gen no into txt file
            tlst = f.read().strip().split(", ")
            tlst.sort()
            st.info(f"Board Numbers: {tlst}")

            st.session_state.board_gen_no_lst = tlst
            st.session_state.board_gen_no_lst = [int(x) for x in tlst]
    
    st.markdown(horizontal_bar, True)
    ResetPlayerBtnColour()
    
def PlayPause():
    st.session_state.GameDetails[5] = not st.session_state.GameDetails[5]

def NewGeneratedNumber():
    vno = GenUniqRndmNo()
    st.session_state.board_nos[vno].markdown(selected_no_colour.replace('|fill_variable|', str(vno).zfill(2)), True)

    with open(st.session_state.GameDetails[2] + 'previous_board_number.txt', 'w') as f:   # write gen no into txt file
        f.write(str(vno))

    if len(st.session_state.board_gen_no_lst) > 0:
        with open(st.session_state.GameDetails[2] + 'board_number_list.txt', 'w') as f:   # write gen no into txt file
            f.write(', '.join(str(x).zfill(2) for x in st.session_state.board_gen_no_lst))

def UpdtWinStatus():
    winstr = ''

    winstr += f"5️⃣: {st.session_state.WinStatus[0]} | " if st.session_state.WinStatus[0] != '' else ''
    winstr += f"1️⃣: {st.session_state.WinStatus[1]} | " if st.session_state.WinStatus[1] != '' else ''
    winstr += f"2️⃣: {st.session_state.WinStatus[2]} | " if st.session_state.WinStatus[2] != '' else ''
    winstr += f"3️⃣: {st.session_state.WinStatus[3]} | " if st.session_state.WinStatus[3] != '' else ''
    winstr += f"🏚️: {st.session_state.WinStatus[4]} | " if st.session_state.WinStatus[4] != '' else ''

    if len(winstr) > 0:
        winstr = 'Win Status: ' + winstr


    return winstr

def DeleteTmpFiles():
    try:
        os.remove(st.session_state.GameDetails[2] + 'board_number_list.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'previous_board_number.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'jaldi5.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'line1.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'line2.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'line3.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'fullhouse.txt')
    except:
        pass

    try:
        os.remove(st.session_state.GameDetails[2] + 'abortgame.txt')
    except:
        pass

def CreateNewBoard():
    ReduceGapFromPageTop()
    st.subheader(f"Game Ref. No. (GRN): :blue[{st.session_state.GameDetails[0]}]:")

    sc1, sc2 = st.columns((2,1))
    with sc2.container():
        st.markdown(f"<img src='data:png;base64,{ReadPictureFile('MainBoard.png')}'>", unsafe_allow_html=True)

    with sc1.container():
        bn_ptr = 0
        for vrow in range(1,10):    # dont include 91-99
            cols = st.columns((1,1,1,1,1,1,1,1,1,1,2))
            for vcol in range(1,11):
                bn_ptr += 1
                btnobj = None
                if bn_ptr not in st.session_state.board_gen_no_lst:
                    btnobj = cols[vcol].markdown(normal_no_colour.replace('|fill_variable|', str(bn_ptr).zfill(2)), True)
                else:
                    btnobj = cols[vcol].markdown(selected_no_colour.replace('|fill_variable|', str(bn_ptr).zfill(2)), True)
                st.session_state.board_nos.append(btnobj)

    st.markdown(horizontal_bar, True)
    c1, c2, c3 = st.columns((1,1,15))
    winstats = c3.empty()

    if st.session_state.WinStatus[0] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'jaldi5.txt'):  # F5 won by some other player
        with open(st.session_state.GameDetails[2] + 'jaldi5.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[0] = f.read().strip()

    if st.session_state.WinStatus[1] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line1.txt'):  # L1 won by some other player
        with open(st.session_state.GameDetails[2] + 'line1.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[1] = f.read().strip()

    if st.session_state.WinStatus[2] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line2.txt'):  # L2 won by some other player
        with open(st.session_state.GameDetails[2] + 'line2.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[2] = f.read().strip()

    if st.session_state.WinStatus[3] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'line3.txt'):  # L3 won by some other player
        with open(st.session_state.GameDetails[2] + 'line3.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[3] = f.read().strip()

    if st.session_state.WinStatus[4] == '' and os.path.isfile(st.session_state.GameDetails[2] + 'fullhouse.txt'):  # FH won by some other player
        with open(st.session_state.GameDetails[2] + 'fullhouse.txt', 'r') as f:   # write gen no into txt file
            st.session_state.WinStatus[4] = f.read().strip()
    
    ws = UpdtWinStatus()
    if ws != '':
        winstats.markdown(win_txt.replace('|fill_variable|', ws), True)

    mbtn_dsble = True if len(st.session_state.board_gen_no_lst) >= 90 else False
    if st.session_state.GameDetails[3] == "manual":
        c1.button("🔄", help="Generate another board number", key='gan', on_click=NewGeneratedNumber, disabled=mbtn_dsble)

    else: # auto mode
        c1.button("⏯", help="Play / pause auto number generation.", on_click=PlayPause)
        if st.session_state.GameDetails[5] == True:
            if mbtn_dsble == False:
                gentimer = st_autorefresh(interval=st.session_state.GameDetails[4] * 1000, limit=91, key="gentmr")
                if gentimer > 0:
                    NewGeneratedNumber()
            
    if c2.button("🔙", help="Return to Main Menu"):
        if len(st.session_state.board_gen_no_lst) < 92:
            with open(st.session_state.GameDetails[2] + 'abortgame.txt', 'w') as f:   # write gen no into txt file
                f.write('Board aborted during mid-play')

        st.session_state.runpage = Main
        st.experimental_rerun()

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
    vsnd = st.radio("Sounds for new number generation", ('No', 'Yes'), horizontal=True, help=w3hlp)
    st.markdown(horizontal_bar, True)

    sc1, sc2, sc3 = st.columns((2,3,10))

    if sc1.button("💾 Save Settings", disabled=btn_dsbld):
        st.session_state.GameDetails[3] = vbr
        st.session_state.GameDetails[4] = vam
        st.session_state.GameDetails[5] = True if vbr == "auto" else False
        st.session_state.GameDetails[6] = False if vsnd == 'No' else True
        st.info("☑️ Settings update completed.")

        tm.sleep(0.75)
        st.session_state.runpage = Main
        st.experimental_rerun()

    if sc2.button("🔙 Return to Main Page"):
        st.session_state.runpage = Main
        st.experimental_rerun()

def NewTicketCallback(gm_ref, plyr_nme):
    st.session_state.GameDetails[0] = gm_ref
    st.session_state.GameDetails[1] = plyr_nme
    st.session_state.GameDetails[2] = vpth + gm_ref + '/'  # Game Path

    if "lst_tkt_no_read_dttm" not in st.session_state:
        st.session_state.lst_tkt_no_read_dttm = dt.now()

    if "player_nos" not in st.session_state:
        st.session_state.player_nos = {}

    tmp_player_nos = GeneratePlayerNos()
    for vkey in tmp_player_nos:
        st.session_state.player_nos[vkey] = False

    st.session_state.disp_player_no = 0
    st.session_state.WinStatus = [''] * 5

    st.session_state.mydf = load_csv()

@st.cache_data
def load_csv():
    st.session_state.mydf = pd.read_csv(vpth + 'NumberDescription.csv')
    st.session_state.mydf['No'] = st.session_state.mydf['No'].astype(int)
    return st.session_state.mydf

def Main():
    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 290px;}</style>', unsafe_allow_html=True,)

    main_page_image = Image.open('MainPage.png').resize((1000, 650))
    st.image(main_page_image, use_column_width='auto')

    with st.sidebar:
        ticket_icon = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
                         <i class="fa-solid fa-ticket">&nbsp;&nbsp;
                         </i> <span style="font-size: 18px; font-weight: bold;">Housie | Tambola | Bingo:</span>'''

        st.markdown(ticket_icon, unsafe_allow_html=True)

        st.markdown(horizontal_bar, True)
        sc01, sc02 = st.columns(2)
        game_rules = sc01.button("📚 Rules &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        game_settings = sc02.button("🛠️ Settings &nbsp;&nbsp;&nbsp;")
        new_game = st.button("🎲 New Game Board &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;")
        new_tkt = False
        sc1, sc2 = st.columns((3,1))
        sc1.markdown("", True)
        sc1.markdown("🎟️ New Game Ticket", True)
        if sc2.button("🔄", help="Refresh Games List / GRNs"):
            st.experimental_rerun()

        # new ticket for an existing game
        with st.expander("Player Options", True):
            files_in_path = os.listdir(".")     # current workspace
            gm_fldr_lst = [x for x in files_in_path if not os.path.isfile(x) and x.startswith('HG')] # chk if folders in dir; only ones that start w/HG

            if len(gm_fldr_lst) > 0:
                gm_fldr_lst.insert(0, '')
                gm_ref = st.selectbox("👇 Choose Game Ref. No. (GRN): :red[*]", gm_fldr_lst, index=0, help="Choose a game for which a ticket needs to be created")
                plyr_nme = st.text_input("👨🏻‍💼 Player Name: :red[*]")
                ntdsbld = True if gm_ref == '' or plyr_nme == '' else False
                new_tkt = st.button("⚙️ Generate Game Ticket", on_click=NewTicketCallback, args=(gm_ref, plyr_nme), disabled=ntdsbld)
                if new_tkt:
                    st.session_state.runpage = CreateNewTicket
                    st.experimental_rerun()

        if game_settings == True:
            st.session_state.runpage = GameSettings
            st.experimental_rerun()

        elif game_rules == True:
            st.session_state.runpage = ViewHelp
            st.experimental_rerun()

        elif new_game == True:
            gm_fldr_nme = f"HG{dt.now():%d%m%Y%H%M%S%f}"  # Game project folder

            subdircreated = CreateSubDir(gm_fldr_nme)
            if not subdircreated:
                st.session_state.GameDetails[0] = gm_fldr_nme
                st.session_state.GameDetails[2] = vpth + gm_fldr_nme + '/'  # Game Path

                if "board_nos" not in st.session_state:
                    st.session_state.board_nos = []

                st.session_state.board_gen_no_lst = []
                st.session_state.board_nos = [0]   # dummy 1st pstn to start next no at 1

                with open(st.session_state.GameDetails[2] + 'previous_board_number.txt', 'w') as f:   # write gen no into txt file
                    f.write('0')

                DeleteTmpFiles()

                st.session_state.WinStatus = [''] * 5
                st.session_state.GameDetails[5] = False

                st.session_state.runpage = CreateNewBoard
                st.experimental_rerun()
        
            else:
                st.error("😲 Couldnt create game folder. Unknown Error.")

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

    hlp_dtl = [''] * 6
    hlp_dtl[1] = """<span style="font-size: 20px;">
    <strong>New Game Board:<br></strong>
    <ol>
    <li style="font-size:18px";>Admin to open browser tab.</li>
    <li style="font-size:18px";>Load game.</li>
    <li style="font-size:18px";>Choose New Game Board.</li>
    <li style="font-size:18px";>Inform players about Game Reference Number (GRN).</li>
    <li style="font-size:18px";>Click on Play/Pause to start (play) board number generation, after all players have connected to the game.</li>
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

    hlp_dtl[2] = """<span style="font-size: 20px;">
    You can use this section to do the following:<br><ul>
    <li style="font-size:18px";>Set the numbers to be randomly generated on the board, to be automatic or manual. <i>Default: Automatic</i>.</li>
    <li style="font-size:18px";>For automatic, you will need to specify the time interval (seconds) between the generation of two numbers. <i>Default: 6.0 seconds</i>.</li>
    <li style="font-size:18px";>You can activate sounds to provide feedback after each number is generated. (Temporarily deactivated.)</li>
    </ul></span>
    """

    hlp_dtl[3] = """<span style="font-size: 20px;">
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

    hlp_dtl[4] = """<span style="font-size: 20px;">
    <ul>
    <li style="font-size:18px";>A New Game Board must be created before any tickets (for that game) can be created.</li>
    <li style="font-size:18px";>The newly created game board is assigned a unique Game Reference Number (GRN). Eg. HG26082023121607217203.</li>
    <li style="font-size:18px";>This GRN must be communicated to all players, so that they can create tickets against that particular game.</li>
    <li style="font-size:18px";>The new game board will consist of numbers between 1-90. Random numbers will be generated between these number limits, for the players to match against their individual tickets. </li>
    <li style="font-size:18px";>The Play/Pause button will need to be clicked to start the game board number run. Thereafter, the next numbers will generate by either (a) repeated clicks of this button (manual mode) or (b) automatically, as per the time interval (seconds) as defined in the game settings (Default: 6 seconds).</li>
    <li style="font-size:18px";>If the back button is pressed during game play, the game will be aborted and game play for all players will terminate thereafter.</li>
    </ul></span>
    """

    hlp_dtl[5] = """<span style="font-size: 20px;">
    <ul>
    <li style="font-size:18px";>Before creating a new ticket, a player must choose a game to play in and provide his/her name.</li>
    <li style="font-size:18px";>It is suggested that all players have unique names to differentiate between them during wins.</li>
    <li style="font-size:18px";>If a player wrongly chooses a game that has already started, or has joined in late, he/she will need to catch up on all the numbers generated during that game run until that point of entry.</li>
    <li style="font-size:18px";>Each player ticket will consist of a random set of 15 numbers, set in 3 rows of 5 numbers each.</li>
    <li style="font-size:18px";>The player will sequentially see all the numbers generated on the board after either the (a) time interval set in the games setting in the automatic mode, or after the (b) button press on the game board in the manual mode.</li>
    <li style="font-size:18px";>All the board numbers can be seen at the bottom of the ticket, sorted ascendingly.</li>
    <li style="font-size:18px";>If the player presses a number on his/her ticket, that is not generated by the game board, a warning message will display at the bottom right of the player’s screen.</li>
    <li style="font-size:18px";>Only board generated numbers can be clicked by each player. Clicking such numbers will turn them green on the ticket.</li>
    <li style="font-size:18px";>Please refer to the Prizes / Wins section for how to declare a win.</li>
    </ul></span>
    """

    icon_optns = ('',
                  '<i class="fa-solid fa-hands-asl-interpreting fa-xl"></i>', 
                  '<i class="fa-solid fa-screwdriver-wrench fa-xl"></i>', 
                  '<i class="fa-solid fa-gifts fa-xl"></i>', 
                  '<i class="fa-solid fa-table-cells fa-xl"></i>', 
                  '<i class="fa-solid fa-ticket fa-xl"></i>')
    hlp_optns = ('', 'Game Overview', 'Game Settings', 'Prizes | Wins', 'New Game Board', 'New Game Ticket')
    vhradio = st.sidebar.radio("Help Topic:", options=hlp_optns)
    
    if vhradio != '':
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
        st.session_state.runpage = Main        
        st.experimental_rerun()

def LandingPage():
    ReduceGapFromPageTop()
    st.markdown(purple_btn_colour, unsafe_allow_html=True)

    bkgrnd_img = f"{vpth}/LandingPage.jpg"
    bkgrnd_img_ext = bkgrnd_img[-4:-1]
    img_code = f"""<style>
                        .stApp {{
                            background: url(data:image/{bkgrnd_img_ext};base64,{base64.b64encode(open(bkgrnd_img, 'rb').read()).decode()});
                            background-size: cover;
                            background-size: 1800px 800px;
                        }}
                   </style>"""

    st.markdown(img_code, unsafe_allow_html=True)
    c1, c2 = st.columns((6,3))
    for i in range(34):
        c2.write("")    # vertical filler

    if c2.button("Press a key to continue..."): # bypass time delay
        st.session_state.runpage = Main
        st.experimental_rerun()

    tm.sleep(10)
    st.session_state.runpage = Main
    st.experimental_rerun()

if 'runpage' not in st.session_state:
    ClearExpiredGameFolders()
    st.session_state.runpage = LandingPage

st.session_state.runpage()