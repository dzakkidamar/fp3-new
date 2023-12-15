import streamlit as st
from sqlalchemy import text

st.markdown('✨ Aplikasi Manajemen Basis Data version 1.0')
st.info("Silakan pilih menu di sidebar untuk melihat, mencari, atau mengedit data perpustakaan.")

image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Unicode_0x03C3.svg/1200px-Unicode_0x03C3.svg.png"
st.sidebar.image(image_url, caption='', width=100)

list_doctor = ['', 'Perpustakaan ITS', 'Perpustakaan Unair', 'Perpustakaan UNESA', 'Perpustakaan Hangtuah', 'Perpustakaan Univ. Ciputra', 'Perpustakaan UPH']
list_type_of_book = ['', 'male', 'female']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dzakmar543:8tqu3wRgTZHs@ep-round-bush-07247722.ap-southeast-1.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS perpustakaan (id serial, cabang_perpustakaan varchar, nama varchar, gender char(25), \
                                                       type_of_book text, title varchar, author text, tanggal_pinjam date);')
    session.execute(query)

st.header('DATABASE PERPUSTAKAAN PERGURUAN TINGGI DI KOTA SURABAYA')
page = st.sidebar.selectbox("Pilih Menu", ["View Data", "Search Data", "Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM perpustakaan ORDER BY id;', ttl="0").set_index('id')
    st.dataframe(data)

elif page == "Search Data":
    search_criteria = st.selectbox("Select Search Criteria", ["cabang_perpustakaan", "nama", "gender", "type_of_book", "title", "author", "tanggal_pinjam"])

    if search_criteria in ["cabang_perpustakaan", "gender", "type_of_book"]:
        unique_values = conn.query(f"SELECT DISTINCT {search_criteria} FROM perpustakaan ORDER BY {search_criteria};", ttl="0")[search_criteria].tolist()
        search_query = st.selectbox(f"Select {search_criteria.replace('_', ' ').capitalize()}", [""] + unique_values)
    else:
        search_query = st.text_input(f"Search {search_criteria.capitalize()}", "")

    if st.button("Search"):
        if search_criteria == "type_of_book" and search_query:
            data = conn.query(f"SELECT * FROM perpustakaan WHERE {search_criteria} @> ARRAY['{search_query}'] ORDER BY id;", ttl="0").set_index('id')
        elif search_query:
            data = conn.query(f"SELECT * FROM perpustakaan WHERE {search_criteria} ILIKE '%{search_query}%' ORDER BY id;", ttl="0").set_index('id')
        else:
            st.warning("Please provide a valid search query.")
            data = pd.DataFrame()
        
        st.dataframe(data)


if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO perpustakaan (cabang_perpustakaan, nama, gender, type_of_book, title, author, tanggal_pinjam) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None})
            session.commit()

    data = conn.query('SELECT * FROM perpustakaan ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        cabang_perpustakaan_lama = result["cabang_perpustakaan"]
        nama_lama = result["nama"]
        gender_lama = result["gender"]
        type_of_book_lama = result["type_of_book"]
        title_lama = result["title"]
        author_lama = result["author"]
        tanggal_pinjam_lama = result["tanggal_pinjam"]

        with st.expander(f'a.n. {nama_lama}'):
            with st.form(f'data-{id}'):
                cabang_perpustakaan_baru = st.selectbox("cabang_perpustakaan", list_doctor, list_doctor.index(cabang_perpustakaan_lama))
                nama_baru = st.text_input("nama", nama_lama)
                gender_baru = st.selectbox("gender", list_type_of_book, list_type_of_book.index(gender_lama))
                type_of_book_baru = st.multiselect("type_of_book", ['Novel', 'Buku Motivasi', 'Buku Referensi', 'Buku Sejarah', 'Buku Bisnis dan Keuangan', 'Buku Ilmiah'], eval(type_of_book_lama))
                title_baru = st.text_input("title", title_lama)
                author_baru = st.text_input("author", author_lama)
                tanggal_pinjam_baru = st.date_input("tanggal_pinjam", tanggal_pinjam_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE perpustakaan \
                                          SET cabang_perpustakaan=:1, nama=:2, gender=:3, type_of_book=:4, \
                                          title=:5, author=:6, tanggal_pinjam=:7 \
                                          WHERE id=:8;')
                            session.execute(query, {'1':cabang_perpustakaan_baru, '2':nama_baru, '3':gender_baru, '4':str(type_of_book_baru), 
                                                    '5':title_baru, '6':author_baru, '7':tanggal_pinjam_baru, '8':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM perpustakaan WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()