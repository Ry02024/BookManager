import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import requests
from PIL import Image
from io import BytesIO

# OpenBD APIから書籍データを取得する関数
def get_book_info_from_openbd(isbn):
    url = f'https://api.openbd.jp/v1/get?isbn={isbn}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and data[0]:
            return data[0]['summary']
    return None

# Google Books APIから書籍データを取得する関数
def get_book_info_from_google_books(isbn, api_key):
    url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            return data["items"][0]["volumeInfo"]
    return None

# 手動でISBN番号を入力する関数
def manual_isbn_input():
    isbn = st.text_input("ISBN番号を入力してください（例: 9784297108434）")
    st.write(f"入力されたISBN番号: {isbn}")  # デバッグ用
    if isbn:
        display_book_info(isbn)

# カメラでバーコードを読み取るクラス
class BarcodeScanner(VideoTransformerBase):
    def __init__(self):
        self.last_barcode = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        decoded_objects = decode(img)

        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type

            # デバッグ: 認識したバーコード情報を表示
            st.write(f"認識したバーコード: {barcode_data} (タイプ: {barcode_type})")

            # ISBNは通常 "97" で始まる
            if barcode_type in ["EAN13", "ISBN13"] and barcode_data.startswith('97') and barcode_data != self.last_barcode:
                self.last_barcode = barcode_data
                st.session_state['barcode'] = barcode_data
                break

        return img

# カメラでバーコードを読み取る関数
def camera_isbn_input():
    if 'barcode' not in st.session_state:
        st.session_state['barcode'] = None
    webrtc_ctx = webrtc_streamer(key="barcode-scanner", video_transformer_factory=BarcodeScanner)
    if st.session_state['barcode']:
        barcode = st.session_state['barcode']
        st.success(f"バーコードが読み取られました: {barcode}")
        display_book_info(barcode)
    else:
        st.write("カメラをバーコードに向けてください。")

# 画像からバーコードを読み取る関数
def image_isbn_input():
    uploaded_file = st.file_uploader("バーコードを含む画像をアップロードしてください", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='アップロードされた画像', use_column_width=True)
        img_array = np.array(image.convert('RGB'))
        decoded_objects = decode(img_array)
        st.write(f"デコードされたオブジェクト: {decoded_objects}")  # デバッグ用
        for obj in decoded_objects:
            barcode_data = obj.data.decode("utf-8")
            barcode_type = obj.type
            st.write(f"認識したバーコード: {barcode_data} (タイプ: {barcode_type})")  # デバッグ用
            if barcode_data.startswith('97'):
                st.session_state['barcode'] = barcode_data
                break
        if 'barcode' in st.session_state and st.session_state['barcode']:
            st.success(f"バーコードが読み取られました: {st.session_state['barcode']}")
            display_book_info(st.session_state['barcode'])
        else:
            st.error("バーコードが検出されませんでした。")

# 書籍情報を表示する関数
def display_book_info(isbn):
    if st.session_state['api_choice'] == 'OpenBD':
        book_info = get_book_info_from_openbd(isbn)
    else:
        book_info = get_book_info_from_google_books(isbn, st.session_state['api_key'])

    if book_info:
        st.write("書籍情報:")
        st.write(f"**タイトル**: {book_info.get('title', '不明')}")
        st.write(f"**著者**: {', '.join(book_info.get('authors', ['不明']))}")
        st.write(f"**出版社**: {book_info.get('publisher', '不明')}")
        st.write(f"**出版年**: {book_info.get('publishedDate', '不明')}")
        if 'imageLinks' in book_info and 'thumbnail' in book_info['imageLinks']:
            image_url = book_info['imageLinks']['thumbnail']
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.image(img, caption=book_info.get('title', '不明'))
    else:
        st.error("書籍情報が見つかりませんでした。")

st.title("ISBN番号で書籍データを検索するアプリ")

api_choice = st.radio("使用するAPIを選択してください:", ("OpenBD", "Google Books"))
st.session_state['api_choice'] = api_choice

if api_choice == "Google Books":
    api_key = st.text_input("Google Books APIキーを入力してください")
    st.session_state['api_key'] = api_key

option = st.radio("選択してください:", ("ISBN番号を入力", "カメラでバーコードを読み取る", "画像からバーコードを読み取る"))

if option == "ISBN番号を入力":
    manual_isbn_input()
elif option == "カメラでバーコードを読み取る":
    camera_isbn_input()
elif option == "画像からバーコードを読み取る":
    image_isbn_input()
