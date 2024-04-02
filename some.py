response = client.images.generate(
    prompt="space robots",
    model="stabilityai/stable-diffusion-xl-base-1.0",
    steps=10,
    n=4,
)
print(response.data[0].b64_json)
