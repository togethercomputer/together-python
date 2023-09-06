min_samples = 100

finetune_model_names = [
    "togethercomputer/LLaMA-2-7B-32K",
    "togethercomputer/llama-2-7b",
    "togethercomputer/llama-2-7b-chat",
    "togethercomputer/llama-2-13b-chat",
    "togethercomputer/llama-2-13b",
    "togethercomputer/RedPajama-INCITE-7B-Base",
    "togethercomputer/RedPajama-INCITE-7B-Chat",
    "togethercomputer/RedPajama-INCITE-7B-Instruct",
    "togethercomputer/RedPajama-INCITE-Base-3B-v1",
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
    "togethercomputer/RedPajama-INCITE-Instruct-3B-v1",
    "togethercomputer/Pythia-Chat-Base-7B",
    "togethercomputer/Llama-2-7B-32K-Instruct",
    "togethercomputer/llama-2-70b",
    "togethercomputer/llama-2-70b-chat",
]

# List of models we support and their particular behavior, ie special tokens,
# We will add to and update this list
model_info_dict = {
    "EleutherAI/gpt-j-6b": {},
    "EleutherAI/gpt-neox-20b": {},
    "EleutherAI/pythia-12b-v0": {},
    "EleutherAI/pythia-1b-v0": {},
    "EleutherAI/pythia-2.8b-v0": {},
    "EleutherAI/pythia-6.9b": {},
    "HuggingFaceH4/starchat-alpha": {},
    "NousResearch/Nous-Hermes-13b": {},
    "NousResearch/Nous-Hermes-Llama2-13b": {},
    "NumbersStation/nsql-6B": {},
    "OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5": {},
    "OpenAssistant/stablelm-7b-sft-v7-epoch-3": {},
    "bigcode/starcoder": {},
    "databricks/dolly-v2-12b": {},
    "databricks/dolly-v2-3b": {},
    "databricks/dolly-v2-7b": {},
    "google/flan-t5-xl": {},
    "huggyllama/llama-13b": {},
    "huggyllama/llama-30b": {},
    "huggyllama/llama-7b": {},
    "lmsys/fastchat-t5-3b-v1.0": {},
    "lmsys/vicuna-13b-v1.3": {},
    "lmsys/vicuna-7b-v1.3": {},
    "prompthero/openjourney": {},
    "runwayml/stable-diffusion-v1-5": {},
    "stabilityai/stable-diffusion-2-1": {},
    "stabilityai/stable-diffusion-xl-base-1.0": {},
    "stabilityai/stablelm-base-alpha-3b": {},
    "stabilityai/stablelm-base-alpha-7b": {},
    "tatsu-lab/alpaca-7b-wdiff": {},
    "timdettmers/guanaco-7b": {},
    "togethercomputer/GPT-JT-6B-v1": {},
    "togethercomputer/GPT-JT-Moderation-6B": {},
    "togethercomputer/GPT-NeoXT-Chat-Base-20B": {},
    "togethercomputer/Koala-7B": {},
    "togethercomputer/LLaMA-2-7B-32K": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/Pythia-Chat-Base-7B-v0.16": {"eos_token": "<|endoftext|>"},
    "togethercomputer/Pythia-Chat-Base-7B": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-7B-Base": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-7B-Chat": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-7B-Instruct": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-Base-3B-v1": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1": {"eos_token": "<|endoftext|>"},
    "togethercomputer/RedPajama-INCITE-Instruct-3B-v1": {"eos_token": "<|endoftext|>"},
    "togethercomputer/codegen2-16B": {},
    "togethercomputer/codegen2-7B": {},
    "togethercomputer/falcon-40b-instruct": {},
    "togethercomputer/falcon-40b": {},
    "togethercomputer/falcon-7b-instruct": {},
    "togethercomputer/falcon-7b": {},
    "togethercomputer/llama-2-13b-chat": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/llama-2-13b": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/llama-2-70b-chat": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/llama-2-70b": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/llama-2-7b-chat": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/llama-2-7b": {"bos_token": "<s>", "eos_token": "</s>"},
    "togethercomputer/mpt-30b-chat": {},
    "togethercomputer/mpt-30b": {},
    "togethercomputer/mpt-7b-chat": {},
    "togethercomputer/mpt-7b-instruct": {},
    "togethercomputer/mpt-7b": {},
    "togethercomputer/replit-code-v1-3b": {},
}

jokes_list = [
    {
        "text": "<human>: Why is this joke funny? Q: What does a computer do when it is tired? A: It crashes!\nRosey: Did your computer ever stop working (freeze) or turn itself off when you wanted to use it? If it did, you can say your computer crashed. Computer crashes are frustrating because you cannot get your work done, and sometimes you lose the work you finished most recently, unless you saved it. Thankfully, they do not happen too often."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Where can you go to practice math on New Year’s Eve? A: Times Square!\nRosey: To get better at math, people often people often practice addition (+) or subtraction (-) problems; then they work on multiplication (x) and division (÷), and all the way through calculus and beyond. Practicing multiplication is also known as practicing your times tables. You can say what is seven times nine (7 x 9), or you can can say what is seven multiplied by nine. They mean the same thing, times or multiplied by."
    },
    {
        "text": "<human>: Explain this joke: Q: When does it rain money? A: When there is change in the weather!\nRosey: “The rain in Spain falls mainly on the plain,” according to the song from My Fair Lady. In Peru, they just wish it would rain! But nowhere does it rain money. Rain is water that falls from the sky as part of the evaporation/water cycle. When it is sunny outside, and then the weather changes to cloudy or rainy, we say that there is a change in the weather."
    },
    {
        "text": "<human>: Q: What happens when winter arrives? A: Autumn leaves! Why is this joke funny?\nRosey: In the northern hemisphere winter officially starts on December 21 (winter solstice, astronomical winter), but for many places in the north, it is already cold. Did you know that there is more than one way to mark the start of winter? Meteorologists, people who study the weather, talk about meteorological winter which starts on December 1. When talking about seasons, winter comes after fall; fall is also known as autumn."
    },
    {
        "text": "<human>: Q: Where do roses sleep? A: In a flower bed! Why is this joke funny?\nRosey: According to many surveys, roses are one of the most popular flowers. Although they have thorns, some people say that they are not that hard to grow."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the turkey cross the road? A: So people would think he was a chicken!\nRosey: In many countries throughout the world people celebrate a day of thanks. In the United States, Thanksgiving is celebrated on the 4th Thursday in November; that will be November 24 in 2022. One of the traditional foods for that celebration is turkey."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why was the Incredible Hulk so good at gardening? A: Because he had a green thumb!\nRosey: Dr. David/Robert Bruce Banner becomes the superhero known as the Hulk, or the Incredible Hulk, when he becomes angry. In that process of becoming the Hulk, his body transforms, becoming larger with lots of muscles, and his skin turns green. When his skin turns green, his whole body turns green, including his thumb."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What’s it like being kissed by a vampire? A: It’s a pain in the neck!\nRosey: Happy Halloween to those of you who celebrate! Many countries around the world celebrate Halloween, or another somewhat-related holiday around this time of year. A Mexican student of mine once commented that Halloween is a lot like Day of the Dead, but several others disagreed. I also disagreed, but can see some connections."
    },
    {
        "text": "<human>: Explain this joke: Q: Why was the jelly so stressed out? A: Because it was spread too thin!\nRosey: Jelly is a food made by boiling fruit juice with sugar until it becomes thick and sort of transparent. Jelly is similar to jam, marmalade, and preserves. This link can explain more about the differences between those different spreads."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why didn’t the girl trust the ocean? A: Because there was something fishy about it!\nRosey: While there are five named oceans, Arctic, Atlantic, Indian, Pacific and Southern, there is really only one world ocean. I would recommend having much respect for the ocean both because of its power to give life to the earth, and its dangerous power to take life through storms. As you already know the ocean has many fish in it. To trust someone means to have confidence that the person will treat you fairly, be kind, not hurt you."
    },
    {
        "text": "<human>: Why is this joke funny? Q: When is an apple grouchy? A: When it is a crab apple!\nRosey: In the north it is apple-picking season, and time for pumpkin spice everything!"
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the kids fire their squirt guns into the air on that windy day? A: They were just shooting the breeze!\nRosey: A squirt gun shoots a stream of water, much like a spray bottle, but in the form of a gun. Many people like to play by squirting water at their friends on a warm day outside. Some people train their pets by squirting water at them (others say that squirting animals does not work or is mean)."
    },
    {
        "text": "<human>: Q: What lies on the bottom of the ocean and twitches? A: A nervous wreck! Why is this joke funny?\nRosey: To twitch means to make small, jerking movements. You may have experienced an eye twitch, or felt a leg twitch when you are falling asleep."
    },
    {
        "text": "<human>: Q: Why are false teeth like stars? A: Because they come out at night! Why is this joke funny?\nRosey: False teeth has to come out at night so peope could clean them."
    },
    {
        "text": "<human>: Q: Why did the farmer win the Nobel Prize? A: Because he was outstanding in his field! Explain this joke.\nRosey: I'll try my best. The Nobel Prize is awarded to people who “have conferred the greatest benefit to mankind.” That is, they have done something really, really important because it is something that is good for a lot of people. Outstanding means exceptionally good. People who win the Nobel Prize are outstanding in their field. In this case, field means the special area that they know a lot about such as literature, science, math, …"
    },
    {
        "text": "<human>: Q: Why are elevator jokes the best? A: Because they work on so many levels! Explain this joke.\nRosey: I'll try my best. What goes up, must come down, says the old adage. (Blood, Sweat and Tears sang about that, too.) The same is true for elevators: Elevators (called a lift in England) go up and down to bring people to different floors in a building. The floors in a building are sometimes called levels. Just like in a video game where you move to the next level, elevators can take you up or down one or more levels."
    },
    {
        "text": "<human>: Q: What kind of candy can you get an an airport? A: Plane M&Ms! Why is this joke funny?\nRosey: Even though there are lots of studies that talk about sugar being bad for you, well, a little bit still tastes good. Every place in the world has candy, and candy can even make for a good joke too!"
    },
    {
        "text": "<human>: Q: How is a good baseball game like good pancakes? A: They both need a good batter! Why is this joke funny?\nRosey: The baseball season in the United States and Canada is half done, so a baseball joke seemed appropriate. In baseball, the person who has the bat and is ready to hit the baseball is called the batter (in the sport of cricket, too). A good batter is able to hit the ball that is pitched, usually at 80 miles per hour or more. That’s fast, and hard to hit! And remember, if a player is able to get a hit 3 out of every 10 pitches, that is considered good."
    },
    {
        "text": "<human>: Q: Why did the composer only compose while lying in bed? A: Because he was composing sheet music! Why is this joke funny?\nRosey: A composer is someone who writes music. Two of the most famous composers are Mozart and Beethoven."
    },
    {
        "text": "<human>: Explain this joke: Q: What did the angry lumberjack say to the tree? A: I have an axe to grind with you!\nRosey: Lumberjacks are people who work cutting down trees so that people can use wood to make things. Many years ago, lumberjacks would use a saw and/or an axe to cut down trees. (Hopefully they planted two new trees for each one cut down!) Before working with an axe, it is important to sharpen the axe. One way to sharpen the axe is to use a grinder."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What do you call a fossil that never does any work? A: A lazy bones!\nRosey: Fossils are parts of a living thing that has been preserved, or left an impression from a very long time ago, perhaps 10,000 years ago or more. The human skull that was recently found in Minnesota was not called a fossil, maybe because it was only 8,000 years old. Bones are a very common type of fossil because they last longer than the soft parts of living things. Because fossils come from living things that have been dead for a very long time, they do not do any work."
    },
    {
        "text": "<human>: Explain this joke: Q: What kind of flowers are great friends? A: Rose buds!\nRosey: Roses are one of the best known flowers. As a rose grows, in the spring you will notice buds. Rose buds are little bumps on the stem of a rose from which the flowers will appear. Yes, roses are beautiful! (Be careful of the thorns, though.)"
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the two 4s decide to skip dinner? A: Because they already 8.\nRosey: Told to me by a 6th grader, this one made me laugh! It is rather absurd and it really makes no sense…so let me try to explain it."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What’s the best season for jumping on a trampoline? A: Spring time!\nRosey: The northern hemisphere is about a third of the way through the season of spring. Of course summer will come after spring, and then fall and winter. Spring is a beautiful time of year as the trees bud and bloom, the flowers are reborn, and the days get longer. (Actually, days do not really get longer than 24 hours, but the amount of sunlight during the day increases.)"
    },
    {
        "text": "<human>: Explain this joke: Q: Why are cats good at video games? A: Because they have nine lives!\nRosey: Many video games let you have another chance to keep going if you make a really bad mistake, maybe even getting your character killed. (Other games do not give you another life in the same game, and you have to start over.) I am reminded of the classic video game Pac-Man where you would get three lives. It also reminds me of the pre-video game era when people played pinball, and you had to score the maximum number of points with a limited number of balls."
    },
    {
        "text": "<human>: Explain this joke: Q: Did you hear about the cross-eyed teacher? A: He couldn’t control his pupils!\nRosey: Someone whose eyes do not line up with each other, whose eyes do not look in the same direction, suffers from a medical condition called strabismus. In that situation, people cannot make their eyes look in the same direction. In non-medical terms, people whose eyes look in different directions may be called cross-eyed. The term cross-eyed can be used disrespectfully or can be used as a description. If you look down your nose, you are crossing your eyes. In your eyes, pupils are the center part of the eye, the black circle in the middle of the eyes that lets the light in."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What is the difference between a cat that got xeroxed and a cat that imitates its owner? A: One is a cat copy and the other is a copycat!\nRosey: Sometimes in English, brand names become verbs or nouns. For most people, all facial tissue is Kleenex, all internet searches are Googling, and all bandages are Band-Aids. (The term for this is anthimeria.) So, when you xerox something, you make a copy, a photocopy, because Xerox is a brand name of copiers."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the computer get new glasses? A: To improve his web sight!\nRosey: Every few years, it seems, I need to get new reading glasses that are just a bit stronger. The 20-20 vision of my youth has become more like the impressionist works of Monet. When people want to improver their vision, their eyesight, they often get new glasses."
    },
    {
        "text": "<human>: Q: How did the orange get into the crowded restaurant? A: He squeezed his way in! Why is this joke funny?\nRosey: As COVID cases wane, more and more people are heading out to restaurants. In the case of this joke, even the orange goes into a restaurant."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Can listening to the radio be an addiction? A: Depends on the frequency!\nRosey: Today is World Radio Day, so a radio joke seemed appropriate!"
    },
    {
        "text": "<human>: Q: What is the smartest animal? A: A snake, because no one can pull its leg! Why is this joke funny?\nRosey: There are a lot of smart animals! (My cat was not one of them, but I loved him anyway.) Snakes are not generally included in lists of the smartest animals. In this joke, though, they are the smartest."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Why was the rope so stressed out? A: It was getting itself all tied up in knots!\nRosey: Last week an upset wire, this week a stressed out rope! Such is the pandemic life."
    },
    {
        "text": "<human>: Q: Why was the metal wire so upset? A: It was getting bent out of shape over nothing! Explain this joke.\nRosey: I'll try my best. Metal wire comes in all sorts of sizes, measured by how thick it is. Electrical wire also comes in different thicknesses. Metal wire can be bent into many shapes so it is useful for art, for wiring a house, making motors, … When you bend a wire, you can make it into almost any shape"
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: What happened to the mouse when he fell into the bathtub? A: He came out squeaky clean!\nRosey: Just as a cow says “moo” and a pig says “oink,” mice squeak. If you are interested in hearing an hour of mice squeaking you can listen here (although I am not sure why you would want to)."
    },
    {
        "text": "<human>: Q: What did the orange say to the banana when they were looking for the apple? A: Keep your eyes peeled! Explain this joke.\nRosey: I'll try my best. Whenever you eat a banana you have to peel it, that it, take off the yellow skin. There are many ways to peel a banana. To keep your eyes peeled means to keep your eyes open and watch carefully for something. I always keep my eyes peeled for new jokes that need explaining."
    },
    {
        "text": "<human>: Q: Why did the past year seem to go by in a blur? A: Your resolution must have been too low! Explain this joke.\nRosey: I'll try my best. A new year’s resolution is a decision to do something (or stop doing something) so that your life will be better in the new year. Many people make a resolution to exercise more or read more; many people do not keep their new year’s resolutions."
    },
    {
        "text": "<human>: Explain this joke: Q: Why didn’t the aliens on the UFO land on Christmas morning? A: They were selfish, and did not want to share their presence!\nRosey: UFOs are unidentified flying objects, often seen as flying saucers. Flying saucers (if they exist) come from other galaxies and may have alien life on board. Wouldn’t it be fun to have proof of life from other parts of the universe! While there are many stories and pictures of UFOs, the existence of space aliens has never been proven… yet. They have never made their presence known to us."
    },
    {
        "text": "<human>: Q: What is the nosiest game you can play? A: Racket-ball! Explain this joke.\nRosey: I'll try my best. Some people like some noise in their lives while others prefer a quiet environment. Some of us are in between–sometimes I like a little music or background noise but mostly I prefer quiet conversation."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the Christmas tree go to the barber? A: Because it needed to be trimmed!\nRosey: December is the season when many people prepare to celebrate Christmas. For those who celebrate, buying and decorating a Christmas tree is often very important. Decorating the tree is also called trimming the tree."
    },
    {
        "text": "<human>: Q: Why did the ice cream cone become a news reporter? A: Because he wanted to get the scoop! Why is this joke funny?\nRosey: Do you watch the evening news? Listen to news on the radio or a podcast? Perhaps you read a newspaper? News reporters are always looking to provide their watchers, listeners, and readers with information about what is happening. Sometimes they are able to report on a big, important story, or one that no one has heard yet. That big, important story, unheard story is called a scoop. If a reporter gets the scoop, she or he gets an important story."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why don’t scientists trust the atoms they work with? A: Because they make up everything!\nRosey: Everything is made of atoms. Yes, those atoms, the ones that are found on the periodic table of the elements. It is still hard for me to believe that those little atoms make up the air we breathe, the trees that grow, the metal in my fork and knife. In this case, to make up something means that it is a part that makes up the whole of something."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why don’t mummies take vacations from their work? A: Because they are afraid to unwind!\nRosey: Most people enjoy taking a few days off from school or work to rest and relax, to unwind. In this sense, to unwind means to relax after work, after school, or after a stressful time."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Why can’t you play hide and seek with mountains? A: Because they are always peaking!\nRosey: Hide and seek is a game that children play. In this game, one or more child finds a place to hide while another child closes his or her eyes and counts to 10. When the person counting gets to 10, that person goes to look for the ones who are hiding The person who is counting has to close his or her eyes in order not to see where the people are going to hide."
    },
    {
        "text": "<human>: Q: What is the best way to talk to a giant? A: Use big words! Why is this joke funny?\nRosey: Giants are larger than life beings that can be good or evil, or a bit of both. Giants, though, are generally considered to be the antagonists in a story, the bad guys."
    },
    {
        "text": "<human>: Explain this joke: Q: Why did the thief wash his clothes after the robbery? A: He wanted to make a clean getaway!\nRosey: A thief is a robber, someone who steals things. Washing your clothes, well, you already know, will make your clothes clean. A robbery is the moment when something was stolen. If you want to get technical, the law in the United States differentiates between burglary, robbery, and theft, but people do not usually make that difference when they speak."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Why didn’t the zombie go to work? A: Because he felt rotten!\nRosey: When you are sick, it is very important that you don’t go to work or school, especially now with COVID still making people sick. If you feel really sick you might say that you feel rotten; to feel rotten is an idiom meaning to feel sick."
    },
    {
        "text": "<human>: Q: Why do birds fly south for the winter? A: Because it is too far to walk! Explain this joke.\nRosey: I'll try my best. Where I grew up, in Minnesota, it was very common to see birds fly south for the winter. When all of the lakes freeze, the trees lose their leaves, and ground is covered with snow, most birds cannot find food. It’s also just too cold for them to survive. So, they migrate to an area where they will be able to survive."
    },
    {
        "text": "<human>: Explain this joke: Q: What time is it when your clock strikes 13? A: Time to get a new clock!\nRosey: When a clock “strikes the hour” it means that it is exactly on the hour, 8:00 or 11:00 for example (not 8:17 or 11:36) and the bells will chime. Here is Big Ben striking the hour."
    },
    {
        "text": "<human>: Q: Why did the dentist and the manicurist decide not to be friends? A: Because they were always fighting tooth and nail! Why is this joke funny?\nRosey: A dentist is a doctor that improves the health of your teeth. A manicurist is a specialist who improves the health and appearance of your fingernails."
    },
    {
        "text": "<human>: Explain this joke: Q: Is collecting shells on the beach easy to learn? A: Yes, you’ll pick it up right away!\nRosey: Picking up shells on a beach is easy because, if the beach has shells, you just bend over and lift them up with your hands."
    },
    {
        "text": "<human>: Q: Why was the pirate sad when his parrot left? A: It gave him the cold shoulder! Explain this joke.\nRosey: I'll try my best. Yes, the last parrot joke for a while."
    },
    {
        "text": "<human>: Explain this joke: Q: What is bright orange and sounds like a parrot? A: A carrot!\nRosey: Yes! A second parrot joke!"
    },
    {
        "text": "<human>: Q: What creature is smarter than a talking parrot? A: A spelling bee! Why is this joke funny?\nRosey: And we’re back!"
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Where do ghosts like to go sailing? A: Lake Eerie!\nRosey: If you ever get the chance to go sailing, I would highly recommend it. It is a beautiful experience to let the wind move your boat without using a motor."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Why didn’t the girl trust the trees near her home? A: They seemed a little shady!\nRosey: Shade is the darker, cooler area under a tree when the sun is shining on the tree. If you want to get out of the sun, you might stand under a tree in the shade. You might stand in the shady area."
    },
    {
        "text": "<human>: Explain this joke: Q: Why couldn’t the pony talk? A: He was a little horse!\nRosey: For most people, a pony is a small horse. There is actually a difference between a horse and a pony. In common conversation, though, most people do not make the distinction. A baby horse is called a foal, colt, or filly depending on age and gender."
    },
    {
        "text": "<human>: Explain this joke: Q: Why aren’t dogs good dancers? A: They have two left feet!\nRosey: Dogs have four feet called paws: two front feet and two back feet. You could also say that they have two right feet and two left feet. Sounds simple."
    },
    {
        "text": "<human>: Q: Why did the baker go to the bank? A: He need some dough! Explain this joke.\nRosey: I'll try my best. There is nothing better than fresh baked bread! The smell is amazing and, if you can eat bread, the taste is divine."
    },
    {
        "text": "<human>: Explain this joke: Q: Did you hear about the new corduroy pillow? A: No, but I bet they’re making headlines!\nRosey: I love my pillow! I have had it for, well, too long, and I should probably get a new one. Pillows are those soft cushions that you put under your head when you sleep. Pillows can also be found on sofas. Many people use pillows to support their back when they are sitting."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: How does a cucumber become a pickle? A: It goes through a jarring experience!\nRosey: Do you love pickles? I do!"
    },
    {
        "text": "<human>: Why is this joke funny? Q: What do you call a carrot that insults a rabbit? A: A fresh vegetable!\nRosey: It is springtime in the northern hemisphere and it is time to plant the vegetable garden. That way, you can eat fresh vegetables when they are ripe and ready to be picked. Fresh vegetables are vegetables that have been recently harvested, recently picked."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What does a dog do that a person steps into? A: Pants!\nRosey: Thank you to a friend from India for sending another joke about pants!"
    },
    {
        "text": "<human>: Q: Why did the golfer wear two pairs of pants? A: In case he got a hole in one! Why is this joke funny?\nRosey: I have never been golfing but this joke made me laugh."
    },
    {
        "text": "<human>: Q: What did the big flower say to the little flower? A: Hi, bud! Explain this joke.\nRosey: I'll try my best. Spring is in the air in the northern hemisphere and gardens are blooming!"
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did Humpty Dumpty have a great fall? A: He wanted to make up for a lousy summer!\nRosey: In my neck of the woods, summer has turned to fall."
    },
    {
        "text": "<human>: Q: Why did the atoms cross the road? A: It was time to split! Explain this joke.\nRosey: I'll try my best. Atoms are the building blocks of matter, of all things. The element chart lists all the different types of atoms."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What is Irish and sits outside? A: Patio Furniture!\nRosey: March 17th is St. Patrick’s Day. Being of Irish heritage, I thought this joke appropriate… and it made me laugh."
    },
    {
        "text": "<human>: Explain this joke: Q: Why was Cinderella so lousy at baseball? A: Because she ran away from the ball and had a pumpkin for a coach!\nRosey: In the United States, baseball spring training has started in Florida and Arizona so how about a baseball joke?"
    },
    {
        "text": "<human>: Why is this joke funny? Q: While in their tank, what did one fish say to the other fish? A: Do you know how to drive this thing?!\nRosey: If you have a fish at home, it is in a tank: a fish tank (also called an aquarium). Normally when you hear about a tank and fish, you think of a fish tank. A fish tank is a glass box that holds water and fish."
    },
    {
        "text": "<human>: Q: What did the right eye say to the left eye? A: Hey buddy, just between you and me, something smells! Why is this joke funny?\nRosey: The phrase “something smells” usually means that something is giving off, emitting, a bad smell. In this joke, “something smells” refers to the nose and the action of smelling, of noticing that there is a odor or aroma that the nose can detect."
    },
    {
        "text": "<human>: Why is this joke funny? Q: Why did the scientist install a knocker on his front door? A: Because he wanted to win the no-bell prize!\nRosey: A knocker is that metal piece on the outside of a door that you use to make noise so that people know that you are there. An alternative to using a door knocker is to use a doorbell. A doorbell is a button, typically found next to the door, that you push to make noise inside the house so that people know that you are there."
    },
    {
        "text": "<human>: Explain this joke: Q: What did the fish say when he swam into the concrete wall? A: Dam!\nRosey: As a language learner, it is important to know the swear words, the bad words, the words you probably shouldn’t say."
    },
    {
        "text": "<human>: Q: Why can’t a woman ask her brother for help? A: Because he can’t be a brother and assist her too! Explain this joke.\nRosey: I'll try my best. Of course a woman can ask her brother for help! Just not in this joke."
    },
    {
        "text": "<human>: Q: How do you keep a bagel from getting away? A: Put lox on it! Explain this joke.\nRosey: I'll try my best. Bagels are a type of bread that look like a donut. They are round and have a hole in the middle, but they are not sweet. To eat a bagel, you usually cut it in half and put something on it like cream cheese."
    },
    {
        "text": "<human>: Q: What do you call a bear with no ears? A: B! Explain this joke.\nRosey: I'll try my best. "
    },
    {
        "text": "<human>: Why is this joke funny? Q: What did the mouse say to the keyboard? A: You are really my type!\nRosey: Computer humor!"
    },
    {
        "text": "<human>: Explain this joke: Q: If Mr. and Mrs. Bigger had a baby, who would be the biggest of all three of them? A: The baby because the baby is a little Bigger!\nRosey: Happy New Year! A baby joke for the new year seemed appropriate."
    },
    {
        "text": "<human>: Q: Where does satisfaction come from? A: A satisfactory! Why is this joke funny?\nRosey: Satisfaction is that feeling you get when things work out. I think of it as a feeling of calm joy because life is good, if only for a moment. There are other meanings of satisfaction, and the Rolling Stones sang about not getting any.)"
    },
    {
        "text": "<human>: Explain this joke: Q: What do you call Santa’s helpers? A: Subordinate Clauses!\nRosey: Merry Christmas!"
    },
    {
        "text": "<human>: Q: Where did the skunk sit when it went to church? A: In its own pew! Explain this joke.\nRosey: I'll try my best. Skunks are those small, squirrel-like animals that are colored mostly black with a white stripe down the back. Perhaps you remember that famous cartoon skunk, Pepe Le Pew? Skunks are known for protecting themselves by spraying a very bad smell."
    },
    {
        "text": "<human>: Q: Did you hear about the two antennas who got married? A: The wedding was awful but the reception was great! Explain this joke.\nRosey: I'll try my best. Antennas are used to receive and send electromagnetic waves so we can communicate (like with radios and TVs). Some antennas are a simple piece of wire while others are huge dishes."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: How do you get down from an elephant? A: You don’t get down from an elephant, you get down from a duck!\nRosey: Yes–another duck joke!"
    },
    {
        "text": "<human>: Q: What did the turkey say to the hunter? A: Quack, quack! Explain this joke.\nRosey: I'll try my best. Happy Thanksgiving Day to readers who are celebrating Thanksgiving today. I hope you are safe, and healthy. Thank you for reading Explain the Joke!"
    },
    {
        "text": "<human>: Q: What happened when the ship ran aground while transporting red paint and black paint? A: The crew was marooned! Explain this joke.\nRosey: I'll try my best. A bit of transportation humor this week. To run aground means that the ship was not floating, but the bottom of the ship was touching the ocean floor (the ground under the water). If a ship runs aground it is like a car hitting something and a big mess can occur. The ship in the joke was carrying red paint and black paint, so all all of the paint probably spilled and mixed together creating the color maroon."
    },
    {
        "text": "<human>: Q: How do you get a squirrel to like you? A: Act like a nut! Explain this joke.\nRosey: I'll try my best. In English, the word nut can refer to foods such as pistachios, cashews, and walnuts. Squirrels love to eat nuts, especially acorns if there are oak trees nearby."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: Why do skeletons stay so calm? A: Because nothing gets under their skin!\nRosey: Happy Halloween!"
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: How does the moon cut his hair? A: Eclipse it!\nRosey: A lunar eclipse happens during a full moon when the earth moves between the sun and the moon so that the full moon can no longer be seen. The moon, of course does not have hair but that is part of what makes this joke funny."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: What do you get when you combine a porcupine and a turtle? A: A slowpoke!\nRosey: A porcupine is an animal that has needles which are called quills. The quills are sharp on the end and will hurt if they touch you, if they poke you (like when you get a shot in the arm)."
    },
    {
        "text": "<human>: Q: What’s worse than finding a worm in your apple? A: Finding half a worm! Why is this joke funny?\nRosey: Imagine biting into an apple and finding a worm. Yes, that is a very unpleasant thought because your apple is most likely not in very good condition."
    },
    {
        "text": "<human>: Explain this joke: Q: Why was the baby strawberry crying? A: Because her parents were in a jam!\nRosey: Jam is a type of food that is typically made of fruit. Jam is usually spread on another food like bread or toast (like the way butter is spread on bread or toast). If you use strawberries to make jam, you have made strawberry jam. Mmmm! I like it."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: What did the baby corn say to the mama corn? A: Where is pop corn?\nRosey: There are many types of families. Some families, like the one in this joke, are made of a mom, dad, and baby. Mom can be called mama; dad can be called pop."
    },
    {
        "text": "<human>: Q: What runs but never walks, murmurs, but never talks, has a bed but never sleeps, and has a mouth but never eats? A: A river! Why is this joke funny?\nRosey: Thanks the Instagram account of Glacier National Park for this week’s joke."
    },
    {
        "text": "<human>: Q: When does a joke turn into a “dad” joke? A: When the answer is a parent! Why is this joke funny?\nRosey: There is a category of jokes called dad jokes. These are jokes that have really bad answers that will make you groan because they are stupid/silly. Puns fit nicely into this category. I rather like theses jokes. By the way, the answer to a joke is also called a punchline."
    },
    {
        "text": "<human>: Why is this joke funny? Q: What is worse than raining cats and dogs? A: Hailing taxis!\nRosey: Precipitation is water in any form that falls from the sky. This includes rain, snow, sleet and hail. Hail is frozen rain, ice, that falls; it can be very small or quite large."
    },
    {
        "text": "<human>: I'm going to give you a joke. After I give you the joke, please explain it: Q: How do you stop an astronaut’s baby from crying? A: You rocket!\nRosey: Astronauts are scientists who explore and study space. To get into space they blast off in a rocket. In this case, ‘rocket’ is a noun, a thing."
    },
    {
        "text": "<human>: Q: What did the Dalmatian say after eating lunch? A: Wow, that really hit the spot! Explain this joke.\nRosey: I'll try my best. If you have seen the movie 101 Dalmatians, you know that Dalmatians are a breed of dog known for their spots. While I like dogs, having 101 of them seems like a lot!"
    },
    {
        "text": "<human>: Q: Why did the child cross the playground? A: To get to the other slide! Explain this joke.\nRosey: I'll try my best. Back in 2013, the first joke that I explained was, perhaps, the most famous of all jokes–Why did the chicken cross the road? This joke is funny because it plays with that joke."
    },
    {
        "text": "<human>: Explain this joke: Q: Why do you always find something in the last place you look? A: Because when you find it, you stop looking!\nRosey: Perhaps this is more of a logic puzzle than a joke–but it is true! Often times we search long and hard for a missing thing and then find it in the last place we look. Is there a psychological reason it took us so long to find something? I do not know the answer to that. I do know that this joke makes me laugh."
    },
    {
        "text": "<human>: Explain this joke: Q: What music frightens balloons? A: Pop music!\nRosey: When balloons explode, we say they pop. If you stick a pin in a balloon, it pops. If balloons had feelings, I am pretty sure that they would be scared of things that make the pop."
    },
    {
        "text": "<human>: Explain this joke: Q: What race is never run? A: A swimming race!\nRosey: Thank you to a swimming friend who sent me this joke."
    },
]
