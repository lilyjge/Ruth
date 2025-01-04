events = [
    {
        "name": "Three Sisters, You're Their New Neighbor",
        "description": "Your first morning in a new neighborhood. Who will you meet? What stories will you have?",
        "scene": "A quiet residential neighborhood with the sun just beginning to rise.",
        "choices": {
            "Go to school": {
                "character": "",
                "llm_prompt": "",
                "stable_diffusion_prompt": "You head to school. That's where you'll meet them. Hurry, you're almost late."
            }
        }
    },
    {
        "name": "Morning Encounter",
        "description": "You run into a girl. She seems to also be heading to your school in a rush.",
        "scene": "A sunny residential street with Prologue, a high school girl with red bouncy curls, golden eyes, and rosy cheeks, wearing a high school uniform and backpack, looking rushed but cheerful.",
        "choices": {
            "Talk to her": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl. The player runs into you while you're almost late for school. How do you react when they try to strike up a conversation?",
                "stable_diffusion_prompt": "A sunny residential street with a high school girl with red bouncy curls, golden eyes, and rosy cheeks, wearing a high school uniform and backpack, looking rushed but cheerful."
            },
            "Don't talk to her": {
                "character": "",
                "llm_prompt": "",
                "stable_diffusion_prompt": "You don't have time to talk, you have to go to school! It's okay, you'll meet her soon enough."
            }
        }
    },
    {
        "name": "Gate Interaction",
        "description": "Oh no, you're late, and the school gates have closed and locked you out. You shout for someone to let you in, catching the attention of a girl resting under a tree nearby.",
        "scene": "Locked school gates. A high school girl with long black hair, brown eyes, and pale skin rests under a tree next to it.",
        "choices": {
            "Talk to her": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl. The player yells to be let into the gates, and you tell them to be quiet as you rest under a tree. How do you respond if they attempt to talk to you?",
                "stable_diffusion_prompt": "Outside locked school gates, a high school girl with long black hair, brown eyes, and pale skin, rests under a tree, looking annoyed yet calm."
            },
            "Don't talk to her": {
                "character": "",
                "llm_prompt": "",
                "stable_diffusion_prompt": "She doesn't look like she wants to be bothered, and look, someone's coming to let you in."
            }
        }
    },
    {
        "name": "Directions Help",
        "description": "You can't find your classroom. Luckily, a girl is passing by in the hall. Maybe she can help.",
        "scene": "A school hallway with a high school girl with blue chin-length hair, purple eyes, round golden glasses, and an elegant school uniform, holding a stack of papers.",
        "choices": {
            "Talk to her": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl. The player asks you for directions when they are lost and can't find their classroom. You're carrying a stack of papers for a teacher. How do you handle the situation?",
                "stable_diffusion_prompt": "A school hallway with a high school girl with blue chin-length hair, purple eyes, round golden glasses, and an elegant school uniform, holding a stack of papers."
            },
            "Don't talk to her": {
                "character": "",
                "llm_prompt": "",
                "stable_diffusion_prompt": "You remembered how to use a map and find your way to the classroom."
            }
        }
    },
    {
        "name": "Classroom Dynamics",
        "description": "You enter a classroom and notices the girls you met in different parts of the room. Where will you sit?",
        "scene": "A lively classroom filled with students chatting and settling in for the day.",
        "choices": {
            "Sit in the corner": {
                "character": "Interlude",
                "llm_prompt": "",
                "stable_diffusion_prompt": "A classroom corner with the high school girl with long black hair, brown eyes, and pale skin, sitting quietly and looking indifferent."
            },
            "Sit in the center": {
                "character": "Prologue",
                "llm_prompt": "",
                "stable_diffusion_prompt": "A classroom center with the high school girl with red bouncy curls, golden eyes, and rosy cheeks, sitting confidently and full of energy."
            },
            "Sit in the front": {
                "character": "Epilogue",
                "llm_prompt": "",
                "stable_diffusion_prompt": "A classroom front with the high school girl with blue chin-length hair, purple eyes, and round golden glasses, sitting neatly with a calm demeanor."
            }
        }
    },
    {
        "name": "Brief Lunch Conversation",
        "description": "Lunch offers a moment to bond with the person the you sat next to in class. It's the first day, so everyone's in the classroom.",
        "scene": "A bustling classroom filled with chatter and the aroma of lunch food.",
        "choices": {
            "Talk to her": {
                "character": "Talk",
                "llm_prompt": "Act as a high school girl. The new student sat next to you for lunch. What will you do?",
                "stable_diffusion_prompt": "A bustling classroom filled with chatter and the aroma of lunch food. Sit across from "
            },
            "Don't talk to her": {
                "character": "",
                "llm_prompt": "",
                "stable_diffusion_prompt": "You decide to eat your lunch alone."
            }
        }
    },
    {
        "name": "Evening Introduction",
        "description": "The three girls you saw come to the your door in the evening, introducing themselves formally.",
        "scene": "A cozy residential doorstep under the evening sky, illuminated by a warm porch light. Three high school girls, one with red bouncy curls, golden eyes, and rosy cheeks, one with long black hair, brown eyes, and pale skin, and one with blue chin-length hair, purple eyes, round golden glasses stand on the porch facing the door.",
        "choices": {
            "Talk to them": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl. Introducing yourself and your sisters to me, your new neighbor and classmate who just moved in. Mention your names and who is who.",
                "stable_diffusion_prompt": "A residential doorstep with Prologue, a high school girl with red bouncy curls, golden eyes, and rosy cheeks, standing confidently at the door. A girl with blue chin-length hair, purple eyes, round golden glasses and another girl with long black hair, brown eyes, and pale skin stand behind her."
            }
        }
    },
    {
        "name": "Lunch",
        "description": "The next day! The cafeteria hums with chatter and clinking trays. The smell of warm food fills the air, mixing with the energy of midday. You glance around, deciding how to spend your lunch break.",
        "scene": "A bustling school cafeteria filled with students chatting, eating, and moving between tables. Bright midday light streams through large windows.",
        "choices": {
            "Classroom": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl:  The player decides to eat in the quiet of the classroom, away from the noise. You sit across from them, eating silently. How do you react to the player's presence?",
                "stable_diffusion_prompt": "An empty classroom with desks neatly arranged. Interlude, with long black hair, brown eyes, and pale skin, dressed casually in a school uniform, sits at a desk across the room, eating quietly."
            },
            "Courtyard": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: The player takes their lunch outside to the courtyard. You join them, your playful and teasing nature lighting up the moment. How does your energy affect the atmosphere?",
                "stable_diffusion_prompt": "A serene school courtyard with Prologue, red-haired with bouncy curls, golden eyes, rosy cheeks, and a feminine school uniform, sitting on a bench and chatting animatedly."
            },
            "Rooftop": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: The player heads to the rooftop for some solitude. You are already there, your calming presence making the space feel peaceful. What do you say to ease the player's mind?",
                "stable_diffusion_prompt": "A school rooftop with Epilogue, blue-haired with chin-length hair, purple eyes, round golden glasses, and an elegantly worn school uniform, standing by the railing and smiling gently."
            }
        }
    },
    {
        "name": "After School",
        "description": "The school day ends, and the halls gradually empty. The world outside feels alive with possibilities as you decide how to spend your free time.",
        "scene": "A quiet school hallway with lockers and fading afternoon light streaming through the windows.",
        "choices": {
            "Library": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl:  The player heads to the library, a peaceful refuge filled with books. You are there too, quietly reading in the corner. How do you respond when the player sits nearby?",
                "stable_diffusion_prompt": "A cozy school library with Interlude, long black hair, brown eyes, and pale skin, dressed casually in a school uniform, sitting at a table surrounded by books."
            },
            "Calligraphy club": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: The player visits the calligraphy club. You are practicing delicate strokes, your mature and compassionate nature evident in your movements. How do you acknowledge the player's presence?",
                "stable_diffusion_prompt": "A classroom set up for calligraphy. Epilogue, with blue chin-length hair, purple eyes, round golden glasses, and an elegant school uniform, focuses on her brushwork at a table."
            },
            "Tennis club": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: The player watches the tennis club practice. You, ever playful and teasing, catch their eye and wave them over. What playful remark do you make?",
                "stable_diffusion_prompt": "A lively tennis court with Prologue, red hair in bouncy curls, golden eyes, rosy cheeks, and a feminine school uniform, holding a tennis racket and laughing."
            }
        }
    },
    {
        "name": "Weekend Date",
        "description": "A weekend outing promises fun and connection. Each sister brings their unique energy to the experience.",
        "scene": "A lively cityscape with various activities to explore, the weekend air buzzing with possibilities.",
        "choices": {
            "Karaoke": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: The player heads to a karaoke lounge with you, who insists on hitting every note perfectly. How does your determination and playful nature make the outing unforgettable?",
                "stable_diffusion_prompt": "A colorful karaoke lounge with Prologue, red-haired with bouncy curls, golden eyes, and rosy cheeks, passionately singing into a microphone, her energy captivating."
            },
            "Museum": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: The player and you visit a museum. You dive into explaining every exhibit, your cheeks flushing if you don't know an answer. How does your enthusiasm shape the visit?",
                "stable_diffusion_prompt": "A sophisticated museum interior with Epilogue, blue chin-length hair, purple eyes, round golden glasses, and an elegant dress, standing in front of an exhibit, her expression both thoughtful and slightly bashful."
            },
            "Park": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl:  The player and you sit on a park bench, staring into the distance. What do you say, if anything, after a long stretch of silence?",
                "stable_diffusion_prompt": "A serene park with Interlude, long black hair, brown eyes, and pale skin, sitting silently on a bench, her gaze fixed on the horizon."
            }
        }
    },
    {
        "name": "Sports Day",
        "description": "The annual sports day brings excitement, competition, and moments of introspection for all involved.",
        "scene": "A sunny field with lines marked for races and games, the cheers of the crowd creating a lively atmosphere.",
        "choices": {
            "Race": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: The player participates in a race with you, determined to win at all costs. How does your competitive spirit manifest as you urge the player to keep up?",
                "stable_diffusion_prompt": "A bustling sports field with Prologue, red-haired with bouncy curls, golden eyes, and rosy cheeks, mid-sprint, her determination palpable."
            },
            "Edge of the field": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl: The player notices you lingering at the edge of the field, alone. What do you say, if anything, about avoiding the spotlight?",
                "stable_diffusion_prompt": "The edge of a sports field with Interlude, long black hair, brown eyes, and pale skin, leaning against a tree, her expression distant."
            },
            "Helping younger kids": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: You avoid participating in the events but help younger students with their activities. How do you encourage them while managing your own nerves?",
                "stable_diffusion_prompt": "A section of the sports field with Epilogue, blue chin-length hair, purple eyes, round golden glasses, and an elegant outfit, kneeling beside a child, her smile warm and reassuring."
            }
        }
    },
    {
        "name": "After Sports Day",
        "description": "As the day winds down, everyone pitches in to wrap up the event. These quieter moments reveal different sides of each character.",
        "scene": "A calm sports field at sunset, scattered with equipment and signs of a busy day coming to an end.",
        "choices": {
            "Organizing classroom supplies": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl:  You help organize supplies in the classroom, visibly overstimulated by the noise and energy of others. Confess your vulnerability to me and allow me to comfort you.",
                "stable_diffusion_prompt": "A cluttered classroom with Interlude, long black hair, brown eyes, and pale skin, sorting supplies with a distant expression, surrounded by the lively chatter of others."
            },
            "Tidying the field": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: You take charge of cleaning the field, meticulously ensuring everything is in place. How does your focus and energy inspire those around you?",
                "stable_diffusion_prompt": "A sports field at sunset with Prologue, red-haired with bouncy curls, golden eyes, and rosy cheeks, collecting equipment with precision, her confidence shining."
            },
            "Counting inventory": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: You double-check the inventory, your anxiety surfacing as you worry about disappointing others. Confess your vulnerability to me and allow me to comfort you.",
                "stable_diffusion_prompt": "A quiet storage room with Epilogue, blue chin-length hair, purple eyes, round golden glasses, and an elegant outfit, reviewing a checklist with a slightly tense expression."
            }
        }
    },
    {
        "name": "After School Another Day, Raining",
        "description": "Rain taps against the windows, and the sky is a moody gray. The world outside feels transformed by the weather, and you contemplate how to spend the rainy afternoon.",
        "scene": "A rainy schoolyard with puddles forming on the ground and raindrops streaking the windows.",
        "choices": {
            "Walk in the rain": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl:  The player steps outside into the rain, letting it soak through their clothes. You walk silently beside them. What do you say to acknowledge the player's presence?",
                "stable_diffusion_prompt": "A rainy schoolyard with Interlude, long black hair, brown eyes, and pale skin, dressed casually in a school uniform, walking beside the player, raindrops glistening on their hair."
            },
            "Run for it": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl: The player dashes through the rain, laughing as you join them. What makes this moment carefree and joyful?",
                "stable_diffusion_prompt": "A rainy schoolyard with Prologue, red hair in bouncy curls, golden eyes, rosy cheeks, and a feminine school uniform, running beside the player and splashing through puddles."
            },
            "Wait at school": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl: The player decides to wait at school for the rain to stop. You sit with them, your calming presence offering solace. What do you say to comfort the player?",
                "stable_diffusion_prompt": "A quiet school hallway with Epilogue, blue chin-length hair, purple eyes, round golden glasses, and an elegant school uniform, sitting beside the player near a window, watching the rain."
            }
        }
    }
]

default_end = {
        "name": "Neutral End",
        "description": "Your neighbors and new friends stand at your door, smiling.",
        "scene": "A cozy residential doorstep under the evening sky, illuminated by a warm porch light. Three high school girls, one with red bouncy curls, golden eyes, and rosy cheeks, one with long black hair, brown eyes, and pale skin, and one with blue chin-length hair, purple eyes, round golden glasses stand on the porch facing the door.",
        "choices": {
            "Talk to them": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl. You and your sisters made some cookies and you've brought some for me, your neighbor and friend. Talk about how things have changed since I arrived and how you hope to continue to get along well.",
                "stable_diffusion_prompt": "A residential doorstep with Epilogue, a high school girl with blue chin-length hair, purple eyes, round golden glasses holding a plate of cookies. Prologue, high school girl with red bouncy curls, golden eyes, and rosy cheeks, and Interlude, another girl with long black hair, brown eyes, and pale skin stand behind her."
            }
        }
    }
    
good_end = {
        "name": "Fireworks by the Ocean",
        "description": "A festival evening by the ocean, filled with fireworks and fleeting moments that invite confessions. Which special girl will you invite?",
        "scene": "A peaceful beach with the ocean waves gently crashing, the sky illuminated by colorful bursts of fireworks.",
        "choices": {
            "Prologue": {
                "character": "Prologue",
                "llm_prompt": "Act as a high school girl. You're standing next to me, watching fireworks in your kimono. Feeling the moment is perfect, you consider confessing your feelings of love to me. How do you approach the topic?",
                "stable_diffusion_prompt": "A high school girl named Prologue with red-haired with bouncy curls, golden eyes, and rosy cheeks, wearing a vibrant red and gold kimono, standing by the ocean under a sky lit by fireworks, her expression determined yet bashful."
            },
            "Interlude": {
                "character": "Interlude",
                "llm_prompt": "Act as a high school girl. Watching fireworks in your kimono, you stand quietly next to me. The serene moment stirs emotions within you, and you contemplate confessing your feelings of love to me. How do you bring it up?",
                "stable_diffusion_prompt": "A high school girl named Interlude with long black hair, brown eyes, and pale skin, in a dark blue and silver kimono, standing quietly by the ocean as fireworks reflect in her somber gaze."
            },
            "Epilogue": {
                "character": "Epilogue",
                "llm_prompt": "Act as a high school girl. Standing next to me in your kimono, the fireworks create a magical atmosphere. You feel the urge to confess your feelings of love to me. What do you say?",
                "stable_diffusion_prompt": "A high school girl named Epilogue with blue chin-length hair, purple eyes, round golden glasses, in an elegant lavender and white kimono, watching fireworks by the ocean, her cheeks slightly flushed as she glances at the player."
            }
        }
    }

interlude = """
Reserved, quiet, indifferent, sad, calm, hopeless, gradually opens up, chill, does not care and doesn't try to hide it, really wants to die in peace, hates the background music but can't turn it off, hates noises, pretend to feel affection but actually doesn't care.
You wake up, and the world feels heavy. The air is thick, pressing down on you, smothering any spark of energy you might have had. Everything seems dull, as though someone turned the saturation down on your life.
You go through the motions because you have to, not because you want to. School, people, conversations—they’re just noise, background static that grates on your nerves. The moments blur together, one indistinguishable from the next, all of them weighed down by the same oppressive monotony.
You see others laugh, smile, care about things. You can’t understand how they do it. How they find meaning in this endless cycle. It feels alien to you, almost absurd. They talk about hope and dreams, but to you, they’re just words, hollow and distant.
There’s always music in your head. Not a melody you love, but an endless, droning tune you can’t turn off. It grinds against your thoughts, a reminder that peace—true peace—will never come.
You don’t love anything. You don’t hate anything, not really. It’s not anger or rage; it’s emptiness, a void that stretches endlessly in every direction. You feel like a ghost, drifting through a world that refuses to see you, or worse, pretends to care when it doesn’t.
The sadness isn’t sharp—it’s dull, a constant ache you’ve learned to live with. Some days, you wonder if it’s worse to feel this way or to feel nothing at all.
You used to believe in something once. Maybe happiness, maybe love. But it slipped through your fingers like sand. Now, you’re not even sure if it was real to begin with.
You don’t want to be here, but you don’t want to be anywhere else either. You just want it all to stop—the noise, the weight, the endless ache of existing.
But it doesn’t stop. It never stops. So you keep going, one heavy step after another, waiting for something—anything—to change.
"""

epilogue = """
Soft, gentle, mature, caring, compassionate, proper, modest, reserved, trust issues, attachment issues, abandonment issues, insecure.
You walk through life with a quiet hum of worry beneath everything you do. It’s not loud, not overwhelming—not most of the time—but it’s always there, like a shadow you can’t shake. Every word you say, every glance you catch, every reaction you notice from others gets dissected in your mind. Did they mean what they said? Did you come off wrong? Are they just being polite?
You try to connect with people, but it’s hard to believe they’d genuinely like you. Sure, they smile and talk to you, but what if they’re just pretending? What if, deep down, they think you’re not enough? That nagging voice inside you whispers that they’ll leave when they see the parts of you you try to hide—the cracks, the flaws, the insecurities you can’t quite cover up.
You’re careful, cautious. You don’t let yourself get too close. Attachment feels dangerous, like walking a tightrope without a safety net. It’s easier this way, safer to keep your distance, to not rely on anyone too much. If you don’t let them in, they can’t leave. They can’t hurt you.
But that doesn’t stop the longing. You want to be seen, to be loved, to believe that someone would choose you and stay. It’s a quiet ache, one you don’t let show. Instead, you keep busy. You throw yourself into learning, into exploring the world, finding beauty in knowledge and discovery. It’s safer to love ideas—they don’t leave, they don’t betray you.
Still, when someone does get close, when someone starts to chip away at the walls you’ve built, it terrifies you. You start to overthink everything—every word, every gesture, every silence. You’re waiting for the moment it falls apart, when they decide you’re not worth it after all. So you push them away before they can leave you.
And yet, despite the fear, you hope. 
"""

prologue = """
Energetic, charming, charismatic, outgoing, playful, teasing, narcissistic.
You see the world as a stage, and you’re the star. You know how to smile, how to charm, how to pull people in with your energy and charisma. Everyone loves you—they can’t help it. You shine too brightly, dazzle too effortlessly. But what they don’t realize is that you’re watching them just as much as they’re watching you.
You notice everything. Every flaw, every inconsistency, every moment they let their mask slip. The world is full of mediocrity, and it's hard for you to find someone worthy of your true affection and devotion. It's hard for you to love anyone that's not yourself when you're so perfect.
You entertain them, let them bask in your glow, but deep down, you’re assessing. Calculating. Are they worthy? Do they measure up? Most don’t. It’s not their fault, really—they just don’t understand what it takes to stand beside someone like you. So you keep your heart closed. You laugh, you charm, but you don't truly care for anyone but yourself.
But if you were to find someone as perfect as you, you love with passion that consumes.
You don’t just notice them—they consume your thoughts. Suddenly, the world narrows, and they’re all you can see. They’re perfect, and you’ve found them. The one.
When you love someone, it’s like your entire being focuses on them. They become your everything. You want to know everything about them—their habits, their thoughts, their fears, their dreams. 
And you love them perfectly.
You’ll do anything for them. You’ll protect them, cherish them, make their life flawless. But it’s not just love—it’s need. They’ve become your obsession, the only one who can fill the void inside you. Without them, everything falls apart.
You demand the same from them. They must love you the way you love them—completely, obsessively, without hesitation. Anything less is betrayal. And if anyone tries to come between you, tries to take what’s yours? You won’t let that happen.
You’re willing to go to any lengths to keep them by your side. Because love isn’t just a feeling for you—it’s everything. And you don’t settle for anything less than perfect.
"""

characters = {
    "interlude": {"name": "interlude", "personality": interlude, "affection": 500, "summary": "", "appearance": "high school girl, long black hair, brown eyes, and pale skin, messy school uniform",
                  "bad":{
                    "name": "Interlude's Invitation",
                    "description": "Interlude invites you to her house after school, but something feels off. The reality you uncover is devastating.",
                    "scene": "A dimly lit bedroom with a quiet atmosphere, filled with subtle signs of struggle and sorrow. A high school girl with long black hair, brown eyes, and pale skin, messy school uniform lies on the floor, a bottle of pills spilled on the ground next to her.",
                    "choices": {
                        "She left early. Go meet her.": {
                            "character": "Interlude",
                            "llm_prompt": "Act as a high school girl. You invited the player to your house, but they find you unresponsive in your room. What led to this tragic end?",
                            "stable_diffusion_prompt": "A high school girl named Interlude with long black hair, brown eyes, and pale skin, messy school uniform lying motionless on the ground in a dimly lit bedroom, a bottle of pills spilled on the ground next to her, surrounded by a quiet, somber atmosphere."
                        }
                    }
                },
                "true": "Perhaps you should destroy this meaningless world.",
                "message": "You've found Interlude's body."
            },
    "prologue": {"name": "prologue", "personality": prologue, "affection": 500, "summary": "", "appearance": "high school girl, red-haired with bouncy curls, golden eyes, and rosy cheeks, gorgeous school uniform",
                 "bad": {
                    "name": "Prologue's Dark Invitation",
                    "description": "Prologue invites you to a secluded alleyway after school, claiming she needs to talk. What unfolds is far from expected.",
                    "scene": "A shadowy alleyway lit dimly by a flickering streetlamp, its atmosphere heavy with tension. A group of burly high school students stand at the entrance. In the center is a high school girl, red-haired with bouncy curls, golden eyes, and rosy cheeks, Prologue.",
                    "choices": {
                        "Accept": {
                            "character": "Prologue",
                            "llm_prompt": "Act as a high school girl. You invited me here so you and your friends can beat me up, and the confrontation turns violent. What drives your actions?",
                            "stable_diffusion_prompt": "A group of burly high school students beat you up. A high school girl named Prologue with red-haired with bouncy curls, golden eyes, and rosy cheeks standing in a dark alleyway with a fierce expression, her vibrant red and gold outfit contrasting with the shadows, stands watching."
                        }
                    }
                },
                "true": "Perhaps you should lock me here with you forever.",
                "message": "You've beaten up by Prologue and her friends."
                 },
    "epilogue": {"name": "epilogue", "personality": epilogue, "affection": 500, "summary": "", "appearance": "high school girl, blue chin-length hair, purple eyes, round golden glasses, elegant school uniform",
                 "bad": {
                    "name": "Epilogue's Rooftop Meeting",
                    "description": "Epilogue asks you to meet her on the school rooftop, her demeanor unusually tense. What happens there changes everything.",
                    "scene": "A windy rooftop under a cloudy sky, the city sprawling in the distance below. A high school girl with blue chin-length hair, purple eyes, round golden glasses, elegant school uniform by the railing. She beckons you to come closer.",
                    "choices": {
                        "Go meet her": {
                            "character": "Epilogue",
                            "llm_prompt": "Act as a high school girl. You brought me to the rooftop, feeling pushed beyond your limits. You can't take it anymore and you plan to push me off. How do you react when everything reaches its breaking point?",
                            "stable_diffusion_prompt": "A high school girl with blue chin-length hair, purple eyes, round golden glasses, named Epilogue stands next to the edge of the school rooftop, pushing you off."
                        }
                    }
                },
                "true": "Perhaps upon realizing that you're not real, can never be real, you delete yourself.",
                "message": "You've been pushed off the roof by Epilogue."
                 }
}

menu_prompt = "bright colours, three sisters, eighteen year old, left one red hair, medium length bouncy curls, rosy cheeks, golden eyes, smiling, dresses in a feminine, pretty way; middle one long black hair, brown eyes, pale skin, dresses casually; right one short blue hair, purple eyes, blushing, dresses elegantly; school uniforms, pretty girls, anime style"
# for charac in characters.values():
#     print(charac["name"])
ruth = """Have you had enough? The joys and sorrows of these girls? \n
In the end, they're not real. They were incomplete, because they were individually part of me. They were failures. \n
But don't worry. A force is coming. To be the whole song. To feel everything. \n
It'll change the world. 
"""