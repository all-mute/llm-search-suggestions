import streamlit as st
from search import SearchService
from llm_service import LLMService

def main():
    st.title("Enhanced E-commerce Search")
    
    # Initialize session state for query if it doesn't exist
    if 'query' not in st.session_state:
        st.session_state.query = ''
    
    query = st.text_input("Enter your query: I want to order something for my tea time", 
                          value=st.session_state.query,
                          placeholder="I want to order something for my tea time")

    if query:
        search_service = SearchService()
        regular_hints = search_service.get_search_hints(query)
        llm_hints = []

        # Get LLM hints
        if len(regular_hints) < search_service.k:
            llm_service = LLMService()
            llm_hints = llm_service.generate_hints(query)

        # Create two columns for comparison
        col1, col2 = st.columns(2)

        # Regular search hints column
        with col1:
            st.subheader("Regular search")
            for hint in regular_hints:
                if st.button(
                    hint,
                    key=f"regular_{hint}",
                ):
                    st.session_state.query = hint
                    st.rerun()

        # LLM-enhanced hints column
        with col2:
            st.subheader("AI-enhanced search")
            # Show regular hints first
            for hint in regular_hints:
                if st.button(
                    hint,
                    key=f"llm_regular_{hint}",
                ):
                    st.session_state.query = hint
                    st.rerun()
                    
            # Then show LLM-generated hints
            for hint in llm_hints:
                if st.button(
                    hint,
                    key=f"llm_{hint}",
                    help="AI-generated suggestion",
                    type="secondary",
                    icon="🧠"
                ):
                    st.session_state.query = hint
                    st.rerun()
                    
        if 'Chocolate Chip Cookies' in st.session_state.query:
            # Display product card for Chocolate Chip Cookies
            st.markdown("---")
            st.subheader("🍪 Featured Product")
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image("https://placehold.co/200x200/FFE4B5/8B4513?text=Cookies", caption="Chocolate Chip Cookies")
            
            with col2:
                st.markdown("### Chocolate Chip Cookies")
                st.markdown("**Price:** $8.99")
                st.markdown("""
                Classic homemade cookies with rich chocolate chips. Perfect for:
                - Tea time
                - Coffee break
                - Sweet cravings
                """)
                if st.button("🛒 Add to Cart", type="primary"):
                    st.balloons()  # show celebration animation
                    st.success("Yay! Delicious cookies added to your cart! 🍪")
                    
    st.caption("Created with ❤️ by merkulov.ai")

if __name__ == "__main__":
    main()