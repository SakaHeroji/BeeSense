"""Streamlit Community Cloud entry point; UI implementation lives in Dashboard."""

from Dashboard.app import SocialNLPStreamlitApp, main, number, percent

__all__ = ["SocialNLPStreamlitApp", "main", "number", "percent"]

if __name__ == "__main__":
    main()
