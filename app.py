import streamlit as st
from sqlalchemy import text

list_doctor = ['', 'dr. Nurita', 'dr. Yogi', 'dr. Wibowo', 'dr. Ulama', 'dr. Ping']
list_symptom = ['', 'male', 'female']

conn = st.connection("postgresql", type="sql", 
                     url="postgresql://dzakmar543:8tqu3wRgTZHs@ep-round-bush-07247722.ap-southeast-1.aws.neon.tech/web")
with conn.session as session:
    query = text('CREATE TABLE IF NOT EXISTS SCHEDULE (id serial, doctor_name varchar, patient_name varchar, gender char(25), \
                                                       symptom text, handphone varchar, address text, tanggal date);')
    session.execute(query)

st.header('SIMPLE HOSPITAL DATA MANAGEMENT SYS')
page = st.sidebar.selectbox("Pilih Menu", ["View Data","Edit Data"])

if page == "View Data":
    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0").set_index('id')
    st.dataframe(data)

if page == "Edit Data":
    if st.button('Tambah Data'):
        with conn.session as session:
            query = text('INSERT INTO schedule (doctor_name, patient_name, gender, symptom, handphone, address, waktu, tanggal) \
                          VALUES (:1, :2, :3, :4, :5, :6, :7, :8);')
            session.execute(query, {'1':'', '2':'', '3':'', '4':'[]', '5':'', '6':'', '7':None, '8':None})
            session.commit()

    data = conn.query('SELECT * FROM schedule ORDER By id;', ttl="0")
    for _, result in data.iterrows():        
        id = result['id']
        doctor_name_lama = result["doctor_name"]
        patient_name_lama = result["patient_name"]
        gender_lama = result["gender"]
        symptom_lama = result["symptom"]
        handphone_lama = result["handphone"]
        address_lama = result["address"]
        waktu_lama = result["waktu"]
        tanggal_lama = result["tanggal"]

        with st.expander(f'a.n. {patient_name_lama}'):
            with st.form(f'data-{id}'):
                doctor_name_baru = st.selectbox("doctor_name", list_doctor, list_doctor.index(doctor_name_lama))
                patient_name_baru = st.text_input("patient_name", patient_name_lama)
                gender_baru = st.selectbox("gender", list_symptom, list_symptom.index(gender_lama))
                symptom_baru = st.multiselect("symptom", ['cough', 'flu', 'headache', 'stomache'], eval(symptom_lama))
                handphone_baru = st.text_input("handphone", handphone_lama)
                address_baru = st.text_input("address", address_lama)
                waktu_baru = st.time_input("waktu", waktu_lama)
                tanggal_baru = st.date_input("tanggal", tanggal_lama)
                
                col1, col2 = st.columns([1, 6])

                with col1:
                    if st.form_submit_button('UPDATE'):
                        with conn.session as session:
                            query = text('UPDATE schedule \
                                          SET doctor_name=:1, patient_name=:2, gender=:3, symptom=:4, \
                                          handphone=:5, address=:6, waktu=:7, tanggal=:8 \
                                          WHERE id=:9;')
                            session.execute(query, {'1':doctor_name_baru, '2':patient_name_baru, '3':gender_baru, '4':str(symptom_baru), 
                                                    '5':handphone_baru, '6':address_baru, '7':waktu_baru, '8':tanggal_baru, '9':id})
                            session.commit()
                            st.experimental_rerun()
                
                with col2:
                    if st.form_submit_button('DELETE'):
                        query = text(f'DELETE FROM schedule WHERE id=:1;')
                        session.execute(query, {'1':id})
                        session.commit()
                        st.experimental_rerun()