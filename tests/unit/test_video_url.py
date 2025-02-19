from together.types.chat_completions import (
    ChatCompletionMessage,
    ChatCompletionMessageContent,
    ChatCompletionMessageContentType,
    ChatCompletionMessageContentVideoURL,
    MessageRole,
)


def test_video_url_message():
    # Test creating a message with video_url content
    message = ChatCompletionMessage(
        role=MessageRole.USER,
        content=[
            ChatCompletionMessageContent(
                type=ChatCompletionMessageContentType.TEXT, text="What's in this video?"
            ),
            ChatCompletionMessageContent(
                type=ChatCompletionMessageContentType.VIDEO_URL,
                video_url=ChatCompletionMessageContentVideoURL(
                    url="https://example.com/video.mp4"
                ),
            ),
        ],
    )

    # Verify the message structure
    assert message.role == MessageRole.USER
    assert isinstance(message.content, list)
    assert len(message.content) == 2

    # Verify text content
    assert message.content[0].type == ChatCompletionMessageContentType.TEXT
    assert message.content[0].text == "What's in this video?"
    assert message.content[0].video_url is None

    # Verify video_url content
    assert message.content[1].type == ChatCompletionMessageContentType.VIDEO_URL
    assert message.content[1].text is None
    assert message.content[1].video_url.url == "https://example.com/video.mp4"
