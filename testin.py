import os, asyncio
from together import AsyncTogether

async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
prompts = [
    "Write a Next.js component with TailwindCSS for a header component.",
    "Write a python function for the fibonacci sequence",
]


async def async_chat_completion(prompts):
    async_client = AsyncTogether(api_key=os.environ.get("TOGETHER_API_KEY"))
    tasks = [
        async_client.completions.create(
            model="codellama/CodeLlama-34b-Python-hf",
            prompt=prompt,
        )
        for prompt in prompts
    ]
    responses = await asyncio.gather(*tasks)

    for response in responses:
        print(response.choices[0].text)


asyncio.run(async_chat_completion(prompts))
