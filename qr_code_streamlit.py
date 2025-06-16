import streamlit as st
import qrcode
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="QR Code Maker by Suren", page_icon="🧩")

st.title("🧩 QR Code Maker by Suren")
st.write("Generate QR codes with optional logo or from a list (batch).")

tab1, tab2 = st.tabs(["🎯 Single QR", "📄 Batch Generator"])

# ------------------- Tab 1: Single QR Code ----------------------
with tab1:
    text = st.text_input("🔤 Enter text or URL:")
    logo_file = st.file_uploader("📎 Optional: Upload a logo (PNG)", type=["png"])

    if st.button("Generate QR") and text:
        qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

        if logo_file is not None:
            logo = Image.open(logo_file)
            box_size = min(img.size) // 4
            logo = logo.resize((box_size, box_size), Image.ANTIALIAS)
            pos = ((img.size[0] - box_size) // 2, (img.size[1] - box_size) // 2)
            img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

        st.image(img, caption="Your QR Code", use_container_width=False)

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        st.download_button("📥 Download QR", data=buf, file_name="qr_code.png", mime="image/png")

# ------------------- Tab 2: Batch QR Generation ----------------------
with tab2:
    st.write("Upload a `.txt` file with one line of text or URL per line.")
    uploaded_file = st.file_uploader("📄 Upload text file", type=["txt"], key="batch")

    batch_logo_file = st.file_uploader("📎 Optional: Logo for all (PNG)", type=["png"], key="logo2")

    if uploaded_file is not None:
        lines = uploaded_file.read().decode("utf-8").splitlines()
        qr_images = []

        for i, line in enumerate(lines):
            if line.strip() == "":
                continue
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.add_data(line.strip())
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

            if batch_logo_file is not None:
                logo = Image.open(batch_logo_file)
                box_size = min(img.size) // 4
                logo = logo.resize((box_size, box_size), Image.ANTIALIAS)
                pos = ((img.size[0] - box_size) // 2, (img.size[1] - box_size) // 2)
                img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            qr_images.append((f"qr_{i+1}.png", buf.getvalue()))

        zip_buf = io.BytesIO()
        with zipfile.ZipFile(zip_buf, "w") as zip_file:
            for name, data in qr_images:
                zip_file.writestr(name, data)
        zip_buf.seek(0)
        st.download_button("📦 Download All as ZIP", data=zip_buf, file_name="qr_codes.zip", mime="application/zip")
