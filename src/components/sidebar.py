import streamlit as st

def side_info():
    with st.sidebar:
        # Display logo and images
        # st.logo("assets/gitrepo.png", icon_image="assets/title.png", link="https://github.com/jackabald/TiDB-Hack-NL-repo-search")
        st.image("assets/gitrepo_pilot.png")

        # Display an informational card
        card_html = """
        <div style="background-color: #0E1117; border: 2px solid #DE834D; border-radius: 10px; padding: 0px 8px; width: 100%; box-sizing: border-box; color: white; text-align: center; font-family: 'Arial', sans-serif; font-size: 14px; color: #FAFAFA;">
            <p>🌟 Your GitRepoPilot AI assistant! Just ask, and watch as it finds exactly what you need, like magic!</p>
        </div>
        """
        st.components.v1.html(card_html, height=100, scrolling=False)

        # Check and input Ollama Server URL
        if "OLLAMA_SERVER_URL" not in st.secrets:
            st.text_input(
                "Ollama Server Url",
                placeholder="Paste your url here",
                value="http://localhost:11434",
                key="ollama_server_url",
                help="Checkout [Ollama setup](https://github.com/blob/main/docs/OLLAMA.md)"
            )

        # Check and input GitHub Token
        if "GITHUB_TOKEN" not in st.secrets:
            st.text_input(
                "GitHub Token",
                type="password",
                placeholder="Enter your GitHub token",
                help="Provide your GitHub token for accessing repositories",
                key="github_token"
            )

        # Check and input TiDB URL
        if "TIDB_URL" not in st.secrets:
            st.text_input(
                "TiDB URL",
                placeholder="Enter your TiDB connection URL",
                help="Provide your TiDB connection URL",
                key="tidb_url"
            )

        # Check and input Jina AI API Key
        if "JINA_API_KEY" not in st.secrets:
            st.text_input(
                "Jina AI API Key",
                type="password",
                placeholder="Enter your Jina AI API key",
                help="Provide your Jina AI API key for embedding models",
                key="jina_api_key"
            )

        # Additional settings in a popover
        with st.popover("More settings", use_container_width=True):
            st.slider(
                "Temperature", min_value=0.0, max_value=2.0, step=0.1, value=0.1, key="temperature"
            )
            st.slider(
                "Max Tokens", min_value=0, max_value=8000, value=2500, key="max_tokens"
            )

        # Divider and link button
        st.markdown("---")
        st.link_button("🔗 Source Code", "https://github.com/jackabald/TiDB-Hack-NL-repo-search", use_container_width=True)

