from crewai_tools import YoutubeChannelSearchTool

# Configure embedchain to use HuggingFace embeddings instead of OpenAI
config = {
    'embedder': {
        'provider': 'huggingface',
        'config': {
            'model': 'sentence-transformers/all-MiniLM-L6-v2'
        }
    }
}

# Initialize the tool with HuggingFace embeddings instead of OpenAI
yt_tool = YoutubeChannelSearchTool(
    youtube_channel_handle='@aishwaryasrinivasan',
    config=config
)
