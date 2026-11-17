import os

from flask import Flask, render_template, url_for

app = Flask(__name__)

AUDIO_EXTS = (".mp3", ".wav", ".ogg", ".m4a")

# Labels and Tabler icon names (https://tabler.io/icons) for the bundled clips, in display order.
# Any other audio file dropped into static/ shows up automatically,
# labelled from its filename.
KNOWN_SOUNDS = {
    "getout.mp3": ("Get Out!!", "door-exit"),
    "brain_fart.mp3": ("Brain Fart", "brain"),
    "alarm.mp3": ("Alarm", "urgent"),
    "boy_wth.mp3": ("WTH Bruh", "mood-confuzed"),
    "bell.mp3": ("Uncanny", "eye"),
    "omg.mp3": ("What The Hell", "alert-triangle"),
    "boom.mp3": ("Boom", "bomb"),
    "screaming.mp3": ("Scream", "mood-wrrr"),
    "fart.mp3": ("Fart", "wind"),
    "ough.mp3": ("Roblox", "cube"),
    "linga.mp3": ("Lingangule", "music"),
    "wait.mp3": ("Wait Wait Wait", "hand-stop"),
    "vine_boom.mp3": ("Vine Boom", "volume"),
    "bruh.mp3": ("Bruh", "mood-empty"),
    "emotional_damage.mp3": ("Emotional Damage", "heart-broken"),
    "fbi_open_up.mp3": ("FBI Open Up", "shield-lock"),
    "metal_pipe.mp3": ("Metal Pipe", "tool"),
    "taco_bell.mp3": ("Taco Bell Bong", "bell"),
    "mlg_airhorn.mp3": ("MLG Airhorn", "speakerphone"),
    "windows_error.mp3": ("Windows Error", "brand-windows"),
    "anime_wow.mp3": ("Anime Wow", "sparkles"),
    "among_us.mp3": ("Among Us", "brand-among-us"),
    "huh_cat.mp3": ("Huh Cat", "cat"),
    "to_be_continued.mp3": ("To Be Continued", "arrow-big-right"),
    "rizz.mp3": ("Rizz", "mood-wink"),
    "spongebob_fail.mp3": ("SpongeBob Fail", "mood-sad-dizzy"),
    "sad_violin.mp3": ("Sad Violin", "mood-sad-2"),
    "directed_by.mp3": ("Directed By Robert B. Weide", "movie"),
    "rock_eyebrow.mp3": ("The Rock Eyebrow", "eye-question"),
    "bonk.mp3": ("Bonk", "hammer"),
    "nope.mp3": ("Nope", "ban"),
    "aughhh.mp3": ("Aughhh", "mood-cry"),
    "galaxy_brain.mp3": ("Galaxy Brain", "planet"),
    "hello_there.mp3": ("Hello There", "hand-love-you"),
    "right_back.mp3": ("We'll Be Right Back", "device-tv"),
    "chipi_chipi.mp3": ("Chipi Chipi Chapa", "paw"),
    "mission_failed.mp3": ("Mission Failed", "medal"),
    "x_files.mp3": ("X-Files", "ufo"),
    "curb.mp3": ("Curb Your Enthusiasm", "mood-unamused"),
    "coffin_dance.mp3": ("Coffin Dance", "coffin"),
    "yeet.mp3": ("Yeet", "rocket"),
    "goofy_horn.mp3": ("Goofy Ahh Horn", "car"),
    "oh_hell_nah.mp3": ("Oh Hell Nah", "mood-angry"),
    "dun_dun_dun.mp3": ("Dun Dun Dun", "mood-nervous"),
    "owen_wow.mp3": ("Owen Wilson Wow", "mood-surprised"),
    "oh_no_laugh.mp3": ("Oh No No No Laugh", "mood-crazy-happy"),
    "xp_startup.mp3": ("Windows XP Startup", "device-desktop"),
    "minecraft_hurt.mp3": ("Minecraft Oof", "brand-minecraft"),
    "discord_ping.mp3": ("Discord Ping", "brand-discord"),
    "kids_yay.mp3": ("Kids Yay", "balloon"),
    "nani.mp3": ("Nani?!", "question-mark"),
    "here_we_go_again.mp3": ("Here We Go Again", "repeat"),
    "sparta.mp3": ("This Is Sparta", "shield"),
    "john_cena.mp3": ("John Cena", "eye-off"),
    "rickroll.mp3": ("Rickroll", "microphone-2"),
    "wilhelm.mp3": ("Wilhelm Scream", "arrow-big-down-lines"),
    "ba_dum_tss.mp3": ("Ba Dum Tss", "mood-xd"),
    "sad_trombone.mp3": ("Sad Trombone", "mood-sad"),
    "crickets.mp3": ("Crickets", "bug"),
    "reverb_fart.mp3": ("Reverb Fart", "cloud"),
    "mario_death.mp3": ("Mario Death", "mushroom"),
    "tuturu.mp3": ("Tuturu", "heart"),
    "nyan_cat.mp3": ("Nyan Cat", "rainbow"),
    "hehe_boi.mp3": ("Hehe Boi", "pepper"),
    "why_running.mp3": ("Why Are You Running", "run"),
    "noice.mp3": ("Noice", "thumb-up"),
    "omae_wa_mou.mp3": ("Omae Wa Mou", "hand-rock"),
    "boowomp.mp3": ("Boowomp", "mood-sad-squint"),
    "law_order.mp3": ("Law & Order", "scale"),
    "dog_doin.mp3": ("What Da Dog Doin", "dog"),
    "spiderman.mp3": ("Spider-Man Meme", "spider"),
    "careless_whisper.mp3": ("Careless Whisper", "music-heart"),
    "run_vine.mp3": ("Run!", "alert-octagon"),
    "nokia.mp3": ("Nokia Ringtone", "device-mobile"),
    "lets_go.mp3": ("Let's Go", "arrow-big-up-lines"),
    "fein.mp3": ("FE!N", "flame"),
    "peter_laugh.mp3": ("Peter Griffin Laugh", "beer"),
    "squidward_walk.mp3": ("Squidward Walk", "shoe"),
    "hitmarker.mp3": ("Hitmarker", "crosshair"),
    "snore.mp3": ("Mimimimi Snore", "zzz"),
    "wasted.mp3": ("Wasted", "skull"),
    "hog_rider.mp3": ("Hog Riderrr", "pig"),
    "giga_chad.mp3": ("Giga Chad", "barbell"),
    "speed_shocked.mp3": ("Speed Shocked", "bolt"),
}


def file_sounds():
    static_dir = os.path.join(app.root_path, "static")
    try:
        on_disk = {f for f in os.listdir(static_dir) if f.lower().endswith(AUDIO_EXTS)}
    except OSError:
        on_disk = set(KNOWN_SOUNDS)

    ordered = [f for f in KNOWN_SOUNDS if f in on_disk]
    ordered += sorted(on_disk - set(KNOWN_SOUNDS))

    sounds = []
    for filename in ordered:
        stem = os.path.splitext(filename)[0]
        label, icon = KNOWN_SOUNDS.get(
            filename, (stem.replace("_", " ").replace("-", " ").title(), "music")
        )
        sounds.append({
            "id": "f_" + stem,
            "label": label,
            "icon": icon,
            "cat": "memes",
            "url": url_for("static", filename=filename),
            "img": url_for("static", filename=f"img/{stem}.jpg")
            if os.path.exists(os.path.join(static_dir, "img", stem + ".jpg")) else None,
        })
    return sounds


@app.route("/")
def index():
    return render_template("index.html", sounds=file_sounds())


if __name__ == "__main__":
    app.run(debug=True)
