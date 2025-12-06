import sys, os


sys.path.append(os.path.dirname(os.path.dirname(__file__)))



from main import main as parse_main
import streamlit as st
import tempfile
import os


st.title("Bank Statement Parser")

uploaded = st.file_uploader("Upload a PDF statement", type=["pdf"])

out_dir = "output"

if uploaded is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded.getvalue())
        tmp_path = tmp.name

    st.write("Parsing...")
    parse_main(tmp_path, out_dir=out_dir)

    base = os.path.splitext(os.path.basename(tmp_path))[0]
    # we don't know exact name, so list output dir
    candidates = [f for f in os.listdir(out_dir) if f.startswith(base)]
    if candidates:
        csv_file = os.path.join(out_dir, candidates[0])
        with open(csv_file, "rb") as f:
            st.download_button("Download CSV", f, file_name=os.path.basename(csv_file))
    else:
        st.error("No CSV produced. Check logs.")
