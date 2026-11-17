import os

from flask import Flask, render_template, url_for

app = Flask(__name__)

AUDIO_EXTS = (".mp3", ".wav", ".ogg", ".m4a")

# Labels and emojis for the bundled clips, in display order.
# Any other audio file dropped into static/ shows up automatically,
# labelled from its filename.
KNOWN_SOUNDS = {
    "getout.mp3": ("Get Out!!", "🚪"),
    "brain_fart.mp3": ("Brain Fart", "🧠"),
    "alarm.mp3": ("Alarm", "🚨"),
    "boy_wth.mp3": ("WTH Bruh", "😳"),
    "bell.mp3": ("Uncanny", "👁️"),
    "omg.mp3": ("What The Hell", "😱"),
    "boom.mp3": ("Boom", "💥"),
    "screaming.mp3": ("Scream", "🙀"),
    "fart.mp3": ("Fart", "💨"),
    "ough.mp3": ("Roblox", "🧱"),
    "linga.mp3": ("Lingangule", "🕺"),
    "wait.mp3": ("Wait Wait Wait", "✋"),
    "vine_boom.mp3": ("Vine Boom", "🗿"),
    "bruh.mp3": ("Bruh", "😐"),
    "emotional_damage.mp3": ("Emotional Damage", "💔"),
    "fbi_open_up.mp3": ("FBI Open Up", "🚔"),
    "metal_pipe.mp3": ("Metal Pipe", "🔩"),
    "taco_bell.mp3": ("Taco Bell Bong", "🌮"),
    "mlg_airhorn.mp3": ("MLG Airhorn", "📯"),
    "windows_error.mp3": ("Windows Error", "🪟"),
    "anime_wow.mp3": ("Anime Wow", "🤩"),
    "among_us.mp3": ("Among Us", "📮"),
    "huh_cat.mp3": ("Huh Cat", "🐱"),
    "to_be_continued.mp3": ("To Be Continued", "➡️"),
    "rizz.mp3": ("Rizz", "😏"),
    "spongebob_fail.mp3": ("SpongeBob Fail", "🧽"),
    "sad_violin.mp3": ("Sad Violin", "🎻"),
    "directed_by.mp3": ("Directed By Robert B. Weide", "🎬"),
    "rock_eyebrow.mp3": ("The Rock Eyebrow", "🤨"),
    "bonk.mp3": ("Bonk", "🔨"),
    "nope.mp3": ("Nope", "🙅"),
    "aughhh.mp3": ("Aughhh", "😩"),
    "galaxy_brain.mp3": ("Galaxy Brain", "🌌"),
    "hello_there.mp3": ("Hello There", "👋"),
    "right_back.mp3": ("We'll Be Right Back", "📺"),
    "chipi_chipi.mp3": ("Chipi Chipi Chapa", "🐈"),
    "mission_failed.mp3": ("Mission Failed", "🎖️"),
    "x_files.mp3": ("X-Files", "👽"),
    "curb.mp3": ("Curb Your Enthusiasm", "🎷"),
    "coffin_dance.mp3": ("Coffin Dance", "⚰️"),
    "yeet.mp3": ("Yeet", "🚀"),
    "goofy_horn.mp3": ("Goofy Ahh Horn", "🚗"),
    "oh_hell_nah.mp3": ("Oh Hell Nah", "😤"),
    "dun_dun_dun.mp3": ("Dun Dun Dun", "😨"),
    "owen_wow.mp3": ("Owen Wilson Wow", "😮"),
    "oh_no_laugh.mp3": ("Oh No No No Laugh", "🤣"),
    "xp_startup.mp3": ("Windows XP Startup", "💻"),
    "minecraft_hurt.mp3": ("Minecraft Oof", "⛏️"),
    "discord_ping.mp3": ("Discord Ping", "💬"),
    "kids_yay.mp3": ("Kids Yay", "🥳"),
    "nani.mp3": ("Nani?!", "😲"),
    "here_we_go_again.mp3": ("Here We Go Again", "🔁"),
    "sparta.mp3": ("This Is Sparta", "🛡️"),
    "john_cena.mp3": ("John Cena", "🤼"),
    "rickroll.mp3": ("Rickroll", "🎤"),
    "wilhelm.mp3": ("Wilhelm Scream", "🤠"),
    "ba_dum_tss.mp3": ("Ba Dum Tss", "🥁"),
    "sad_trombone.mp3": ("Sad Trombone", "🎺"),
    "crickets.mp3": ("Crickets", "🦗"),
    "reverb_fart.mp3": ("Reverb Fart", "🌬️"),
    "mario_death.mp3": ("Mario Death", "🍄"),
    "tuturu.mp3": ("Tuturu", "🎀"),
    "nyan_cat.mp3": ("Nyan Cat", "🌈"),
    "hehe_boi.mp3": ("Hehe Boi", "🌶️"),
    "why_running.mp3": ("Why Are You Running", "🏃"),
    "noice.mp3": ("Noice", "👌"),
    "omae_wa_mou.mp3": ("Omae Wa Mou", "👊"),
    "boowomp.mp3": ("Boowomp", "😔"),
    "law_order.mp3": ("Law & Order", "⚖️"),
    "dog_doin.mp3": ("What Da Dog Doin", "🐶"),
    "spiderman.mp3": ("Spider-Man Meme", "🕷️"),
    "careless_whisper.mp3": ("Careless Whisper", "🎷"),
    "run_vine.mp3": ("Run!", "🏃‍♂️"),
    "nokia.mp3": ("Nokia Ringtone", "📱"),
    "lets_go.mp3": ("Let's Go", "🙌"),
    "fein.mp3": ("FE!N", "🔥"),
    "peter_laugh.mp3": ("Peter Griffin Laugh", "🍺"),
    "squidward_walk.mp3": ("Squidward Walk", "🦑"),
    "hitmarker.mp3": ("Hitmarker", "🎯"),
    "snore.mp3": ("Mimimimi Snore", "😴"),
    "wasted.mp3": ("Wasted", "💀"),
    "hog_rider.mp3": ("Hog Riderrr", "🐗"),
    "giga_chad.mp3": ("Giga Chad", "🗿"),
    "speed_shocked.mp3": ("Speed Shocked", "⚡"),
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
        label, emoji = KNOWN_SOUNDS.get(
            filename, (stem.replace("_", " ").replace("-", " ").title(), "🔊")
        )
        sounds.append({
            "id": "f_" + stem,
            "label": label,
            "emoji": emoji,
            "cat": "memes",
            "url": url_for("static", filename=filename),
        })
    return sounds


@app.route("/")
def index():
    return render_template("index.html", sounds=file_sounds())


if __name__ == "__main__":
    app.run(debug=True)
