import streamlit as st
from deep_translator import GoogleTranslator

# Page configuration
st.set_page_config(page_title="Global AI Translator", page_icon="🌐")

@st.cache_data
def get_supported_languages():
    """Fetch and cache the supported languages."""
    return GoogleTranslator().get_supported_languages(as_dict=True)

def main():
    st.title("🌐 AI Language Translator")
    st.markdown("Translate text between over 100 languages using AI.")

    # Fetch supported languages dynamically
    try:
        langs_dict = get_supported_languages()
        # Standardize keys to lowercase for reliable lookups and create display names
        name_to_code = {name.lower(): code for name, code in langs_dict.items()}
        display_names = sorted([name.capitalize() for name in name_to_code.keys()])
    except Exception as e:
        st.error("Failed to fetch languages. Please check your internet connection.")
        return

    # Sidebar for configuration
    st.sidebar.header("Settings")
    
    # Layout: Two columns for source and target selection
    col1, col2 = st.columns(2)

    with col1:
        # We add 'auto' to the source list so the AI can detect the language
        source_lang_name = st.selectbox("From (Source):", ["Auto-detect"] + display_names)

    with col2:
        # Default target to English if available
        default_index = display_names.index("English") if "English" in display_names else 0
        target_lang_name = st.selectbox("To (Target):", display_names, index=default_index)

    # Text input area
    source_text = st.text_area("Enter text to translate:", placeholder="Type something...", height=200)

    # Translation logic
    if st.button("Translate Now"):
        cleaned_text = source_text.strip()
        if not cleaned_text:
            st.warning("Please enter some text to translate.")
        elif len(cleaned_text) > 5000:
            st.error("Text is too long. Please limit to 5000 characters.")
        else:
            with st.spinner("Translating..."):
                try:
                    # Map display names back to codes
                    source_code = "auto" if source_lang_name == "Auto-detect" else name_to_code.get(source_lang_name.lower())
                    target_code = name_to_code.get(target_lang_name.lower())

                    if not target_code:
                        raise ValueError(f"Invalid target language selected: {target_lang_name}")

                    translator = GoogleTranslator(source=source_code, target=target_code)
                    translated_text = translator.translate(cleaned_text)

                    if not translated_text:
                        st.error("Translation returned no result. Try again with different text.")
                        return

                    st.subheader("Translation:")
                    st.success(translated_text)
                    
                    # Add a feature to copy result
                    st.text_area("Translated output (raw):", value=translated_text, height=150, help="You can copy the text from here.")
                    
                except Exception as e:
                    st.error(f"An error occurred during translation: {e}")

    # Footer
    st.markdown("---")
    st.caption("Powered by Streamlit and Deep-Translator (Google Translate Engine)")

if __name__ == "__main__":
    main()
