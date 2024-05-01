completion_test_model_list = [
    "meta-llama/Llama-2-7b-hf",
    "togethercomputer/StripedHyena-Hessian-7B",
]
chat_test_model_list = []
embedding_test_model_list = []
image_test_model_list = []
moderation_test_model_list = []

LLAMA_PROMPT = """Llamas that are well-socialized and trained to halter and lead after weaning are very friendly and pleasant to be around. They are extremely curious and most will approach people easily. However, llamas that are bottle-fed or over-socialized and over-handled as youth will become extremely difficult to handle when mature, when they will begin to treat humans as they treat each other, which is characterized by bouts of spitting, kicking and neck wrestling.
Llamas are now utilized as certified therapy animals in nursing homes and hospitals. Rojo the Llama, located in the Pacific Northwest was certified in 2008. The Mayo Clinic says animal-assisted therapy can reduce pain, depression, anxiety, and fatigue. This type of therapy is growing in popularity, and there are several organizations throughout the United States that participate.
When correctly reared, llamas spitting at a human is a rare thing. Llamas are very social herd animals, however, and do sometimes spit at each other as a way of disciplining lower-ranked llamas in the herd. A llama's social rank in a herd is never static. They can always move up or down in the social ladder by picking small fights. This is usually done between males to see which will become dominant. Their fights are visually dramatic, with spitting, ramming each other with their chests, neck wrestling and kicking, mainly to knock the other off balance. The females are usually only seen spitting as a means of controlling other herd members. One may determine how agitated the llama is by the materials in the spit. The more irritated the llama is, the further back into each of the three stomach compartments it will try to draw materials from for its spit.
While the social structure might always be changing, they live as a family and they do take care of each other. If one notices a strange noise or feels threatened, an alarm call - a loud, shrill sound which rhythmically rises and falls - is sent out and all others become alert. They will often hum to each other as a form of communication.
The sound of the llama making groaning noises or going "mwa" is often a sign of fear or anger. Unhappy or agitated llamas will lay their ears back, while ears being perked upwards is a sign of happiness or curiosity.
An "orgle" is the mating sound of a llama or alpaca, made by the sexually aroused male. The sound is reminiscent of gargling, but with a more forceful, buzzing edge. Males begin the sound when they become aroused and continue throughout copulation.
Using llamas as livestock guards in North America began in the early 1980s, and some sheep producers have used llamas successfully since then. Some would even use them to guard their smaller cousins, the alpaca. They are used most commonly in the western regions of the United States, where larger predators, such as coyotes and feral dogs, are prevalent. Typically, a single gelding (castrated male) is used."""

completion_prompt_list = [
    "The quick brown fox jumps over the lazy dog. The quick brown fox jumps over the lazy dog.",
    "hi," * 25,
    LLAMA_PROMPT,
]
