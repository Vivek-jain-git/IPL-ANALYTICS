import streamlit as st
from streamlit.hashing import _CodeHasher
import hashlib

class SessionState(object):
    def __init__(self, session, **kwargs):
        self.__dict__["_state"] = {}

        self.session = session
        self._hash_funcs = _CodeHasher()
        self._hash_funcs.update(kwargs)

        for key, val in kwargs.items():
            setattr(self, key, val)

    def __setattr__(self, name, value):
        self.__dict__["_state"][name] = value

    def __getattr__(self, name):
        try:
            return self.__dict__["_state"][name]
        except KeyError:
            raise AttributeError(name)

    def __repr__(self):
        return self.__dict__["_state"].__repr__()

    def __getstate__(self):
        return self.__dict__["_state"]

    def __setstate__(self, state):
        self.__dict__["_state"] = state


def main():
    st.title("Embedded Streamlit App")

    session_state = SessionState.get(password="", inputValue="")

    received_input = st.empty()

    if st.button("Submit"):
        received_input.markdown("Received Input Value: " + session_state.inputValue)

if __name__ == "__main__":
    main()
