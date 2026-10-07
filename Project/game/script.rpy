## ทหาร 69 - เป่ายิงฉุบ Boss Rush
##
## One shared battle engine (label battle) drives every fight. Each fight is a
## plain dict in `fights`, so adding an opponent means adding data, not
## copy-pasting another 100 lines of labels.

init:

    # backgrounds
    image streetB = Image("image/street.png")
    image whB = Image("image/wh.jpg")
    image seaB = Image("image/sea.jpg")
    image sodercampB = Image("image/mb.jpg")
    image policeB = Image("image/police.png")

    # battle backgrounds
    image bCc = Image("battle/battleCc.png")
    image bFin = Image("battle/battleFin.png")
    image bPw = Image("battle/battlePw.png")
    image bTo = Image("battle/battleTo.png")
    image bTu = Image("battle/battleTu.png")

    # characters
    image soderC = Image("character/s69.png")
    image ccC = Image("character/cc.png")
    image finC = Image("character/fin.png")
    image toC = Image("character/pto.png")
    image pwC = Image("character/pw.png")
    image prayutC = Image("character/tu.png")


define soder = Character("ทหาร69", color="#9ad17a")
define cc = Character("ท่านชัชช่า", color="#ff9ecb")
define pw = Character("ดันตือ", color="#f0c36a")
define prayut = Character("ลุงตูบ", color="#e07a5f")
define fin = Character("ฟินนี่เดอะชาร์ค", color="#6ec1e4")
define to = Character("บังโต", color="#c4a5ff")

# Show/hide order: foe on the left, hero on the right, always.
transform foe_pos:
    xalign 0.15 yalign 1.0
transform hero_pos:
    xalign 0.85 yalign 1.0

default selection = "none"      # hero's move, Thai text for display
default result = "none"         # foe's move, Thai text for display
default score = 0               # rounds the hero has won this fight
default enemy = 0               # rounds the foe has won this fight
default ties = 0
default foe = None              # Character speaking for the current foe
default foe_name = ""
default total_losses = 0        # across the whole run, shown on the ending

default persistent.cheating = 0
default persistent.best_run = None   # fewest total losses on a finished run


init python:

    MOVES = ["rock", "paper", "scissors"]
    MOVE_TH = {"rock": "ค้อน", "paper": "กระดาษ", "scissors": "กรรไกร"}
    # key beats value
    BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    WIN_TARGET = 3

    def outcome(mine, theirs):
        """1 hero wins, -1 hero loses, 0 tie."""
        if mine == theirs:
            return 0
        return 1 if BEATS[mine] == theirs else -1

    def move_that_beats(move):
        for k, v in BEATS.items():
            if v == move:
                return k

    def say_line(pool):
        """Pick a random line and fill in [selection] / [result]."""
        return renpy.substitute(renpy.random.choice(pool))


define fights = {

    "to": {
        "who": to, "name": "บังโต", "bg": "bTo",
        "tie": ["ออก[result]เหมือนกันเรอะ... ใช้ได้นี่"],
        "win": ["[selection]ชนะ[result]อยู่แล้ว! เจ้ามันกากเอง",
                "บังโตแพ้แล้ว! [selection]ของข้าไม่ธรรมดา"],
        "lose": ["[result]ของข้าชนะ[selection]! ไปล้างส้วมซะ",
                 "ฮ่าๆ แค่นี้เองเหรอ ทหาร69"],
        "beat": "ไปล้างส้วมเดี๋ยวนี้!",
        "retry": "ยังไม่จบ! ขอสู้ใหม่!",
        "defeat": "อย่ามาห้าวกับพี่!",
    },

    "pw": {
        "who": pw, "name": "ดันตือ", "bg": "bPw",
        "tie": ["เสมองั้นรึ !!"],
        "win": ["[selection] ชนะ [result] เหอะ ไอ้อ้วนขาเบียด อย่างแกหน่ะแค่เดินก็แทบจะไม่ไหวอยู่แล้ว",
                "ดันตือ ลีลาเยอะ แต่ฝีมือไม่ถึง!"],
        "lose": ["[result]ของฉันชนะ[selection]ก็มาดิคร้าบบ!",
                 "วิดพื้น 100 ครั้ง เริ่ม!"],
        "beat": "วิดพื้น 100 ครั้ง เดี๋ยวนี้!",
        "retry": "อีกรอบ! คราวนี้ไม่พลาดแน่",
        "defeat": "ไม่... ไม่จริง... กองทัพเสียหน้าหมดแล้ว...",
    },

    "fin": {
        "who": fin, "name": "ฟินนี่เดอะชาร์ค", "bg": "bFin",
        "tie": ["แฮ่~! [result]"],
        "win": ["[selection]แฮ่~! [result]"],
        "lose": ["[result]แฮ่~! [selection]"],
        "beat": "แฮ่ๆๆๆ~ (ฉลามกำลังหิว)",
        "retry": "ยังไม่ตาย! ขอสู้อีกรอบ!",
        "defeat": "แฮ่ ๆๆๆๆ",
    },

    "tu": {
        "who": prayut, "name": "ลุงตูบ", "bg": "bTu",
        "tie": ["ออก[result]เหมือนกัน! ยังพอไปได้นะเนี่ย"],
        "win": ["[selection] หน่ะชนะ [result] นะไอตูบ!"],
        "lose": ["[result] ของข้าชนะ [selection] ของเจ้า เจ้าประเมินพลังข้าต่ำไป!"],
        "beat": "ไปปรับทัศนคติใหม่ซะ!",
        "retry": "ยังไม่จบ! ข้าจะไม่ยอมแพ้!",
        "defeat": "[selection] หน่ะชนะ [result]แน่นอนอิอิ ม.69ก็ทำอะไรกูไม่ได้",
    },

    # Final boss: rigged on purpose (the joke is that you cannot win).
    # The fight ends once `limit` losses are on the board.
    "cc": {
        "who": cc, "name": "ท่านชัชช่า", "bg": "bCc",
        "rigged": True, "limit": 10,
        "tie": [],
        "win": [],
        "lose": ["ไม่รู้หรอว่า [result] ชนะ [selection] ได้ หุหุ",
                 "[result] ชนะ [selection] เสมอ นี่คือกฎของข้า",
                 "ฉันเคยท้าซุปเปอร์แมนมาแล้วนะ ลองใหม่สิ"],
        "events": {
            5: "อะไรกันเนี่ยเป็นไปไม่ได้ ! แต่ข้ายังไหว",
            10: None,
        },
    },
}


## Core battle loop #############################################################
##
## call battle("to") -> returns when the hero wins (or, for rigged bosses,
## once the foe has landed `limit` wins).

label battle(key):

    $ f = fights[key]
    $ foe = f["who"]
    $ foe_name = f["name"]
    $ rigged = f.get("rigged", False)
    $ limit = f.get("limit", WIN_TARGET)
    $ score = 0
    $ enemy = 0
    $ ties = 0

    scene expression f["bg"] with fade
    show screen stats

    while True:

        menu:
            "เลือกท่าของคุณ"

            "ค้อน":
                $ pick = "rock"
            "กระดาษ":
                $ pick = "paper"
            "กรรไกร":
                $ pick = "scissors"

        python:
            if rigged:
                foe_pick = move_that_beats(pick)
            elif persistent.cheating:
                foe_pick = BEATS[pick]
            else:
                foe_pick = renpy.random.choice(MOVES)
            selection = MOVE_TH[pick]
            result = MOVE_TH[foe_pick]
            verdict = outcome(pick, foe_pick)

        if verdict == 1:
            $ score += 1
            $ line = say_line(f["win"])
            soder "[line]"
        elif verdict == -1:
            $ enemy += 1
            $ total_losses += 1
            $ line = say_line(f["lose"])
            foe "[line]"
        else:
            $ ties += 1
            $ line = say_line(f["tie"])
            foe "[line]"

        if rigged:
            if verdict == -1 and f["events"].get(enemy):
                $ line = f["events"][enemy]
                soder "[line]"
            if enemy >= limit:
                jump battle_done
        elif score >= WIN_TARGET:
            $ line = renpy.substitute(f["defeat"])
            foe "[line]"
            jump battle_done
        elif enemy >= WIN_TARGET:
            $ line = f["beat"]
            foe "[line]"
            $ line = f["retry"]
            soder "[line]"
            $ score = 0
            $ enemy = 0
            $ ties = 0

    label battle_done:

    hide screen stats
    $ score = 0
    $ enemy = 0
    $ ties = 0
    return


## Story ########################################################################

label start:

    $ total_losses = 0

    # --- Round 1: Bang To ---------------------------------------------------

    scene sodercampB with fade
    "ณ ค่ายทหาร"
    show soderC at hero_pos with moveinright

    soder "เฮ้อ... เหนื่อยเป็นบ้า ดันตือสั่งซ่อมทั้งวันเลย อาบน้ำดีกว่า"
    soder "เฮ้ย! นั่นมัน.."

    show toC at foe_pos with moveinleft
    "บังโตปรากฏตัว"

    to "ทหาร69! เรามาเล่นเป่ายิงฉุบกันเถอะ คนแพ้ต้องไปล้างส้วมทั้งค่าย"
    soder "ไม่!!"
    to "เริ่มต้นได้สวย"

    "บังโต ต้องการท้าคุณเป่ายิงฉุบ"

    call battle("to")

    # --- Round 2: Dan Tue ---------------------------------------------------

    scene sodercampB with fade
    "ณ ค่ายทหาร"

    show pwC at foe_pos with moveinleft
    "ดันตือปรากฏตัว"

    pw "เสียงดังโวยวายอะไรกัน!"
    pw "แกอีกแล้วหรอ ทหาร69! ไปวิดพื้น 100 ครั้ง!"
    show soderC at hero_pos with dissolve
    soder "ไม่ !!!"
    pw "ไม่อย่างนั้นหรอ ! มึงเจอกู !!"

    call battle("pw")

    # --- Round 3: Finny the Shark ------------------------------------------

    scene sodercampB with fade
    "ณ ค่ายทหารในเช้าวันต่อมา"

    show prayutC at foe_pos with moveinleft
    prayut "เมื่อวานใครซ้อมดันตือ !!"

    "..."

    prayut "อย่าคิดว่าข้าไม่รู้นะ ทหาร69!"

    show soderC at hero_pos with dissolve
    soder "ชิบหายละ!"

    prayut "ทหาร! ลากมันไปปรับทัศนคติกับฉลาม!"

    soder "ม่ายยยยยย!"

    scene seaB with fade
    "ณ ทะเลใกล้ๆค่ายทหาร"
    show soderC at hero_pos with dissolve
    soder "ทำไมเราต้องมาเจออะไรแบบนี้ด้วย"

    show finC at foe_pos with moveinleft
    "ฟินนี่เดอะชาร์ค ปรากฏตัว"
    fin "แฮ่~"

    call battle("fin")

    # --- Round 4: Uncle Toob ------------------------------------------------

    scene whB with fade
    "ณ ทำเนียบรัฐบาล"

    show soderC at hero_pos with dissolve
    soder "ลุงตูบ วันนี้คือวันตายของเจ้า"
    show prayutC at foe_pos with moveinleft
    prayut "โอหัง ! แน่จริงก็เข้ามา"

    call battle("tu")

    scene whB with fade
    "หลังจากนั้น ทหาร69 ก็ถูกปลดกระจำการ"

    # --- Final: Chadcha (unwinnable) ---------------------------------------

    scene streetB with fade
    "ระหว่างทหาร69 กลับบ้าน"
    show ccC at foe_pos with dissolve
    "ท่านชัชช่าปรากฏตัว"
    cc "นายเป็นคนที่ล้ม ม.69 ได้สินะ "
    cc "อยากเจอนายมาตั้งนานแล้ว มาวัดพลังกันหน่อยสิ!"
    show soderC at hero_pos with dissolve
    soder "อย่าดีกว่าท่านทำอะไรผมไม่ได้หรอก!"
    cc "เมื่อก่อนฉันเคยท้าซุปเปอร์แมนต่อย"
    cc "โดยที่ใครแพ้ให้ใส่กางเกงในไว้ข้างนอกเชียวนะ!"

    call battle("cc")

    cc "ไม่มีทางหรอกน่า เจ้าหน่ะได้ตายไปแล้ว !"
    soder "ม่ายยยยยยยยยยยยย"

    scene policeB with fade
    "หลังจากนั้น ทหาร69 ก็โดนจับเข้าคุก"
    "ทำให้เกมนี้จบลงโดยที่สุด ขอบคุณที่ทนเล่นมาได้ขนาดนี้"

    if persistent.best_run is None or total_losses < persistent.best_run:
        $ persistent.best_run = total_losses

    "แพ้ทั้งหมด [total_losses] ครั้ง  |  สถิติดีที่สุด: [persistent.best_run] ครั้ง"

    return
