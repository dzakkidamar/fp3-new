drop table if exists schedule;
create table schedule (
	id serial,
	doctor_name text,
	patient_name text,
	gender text,
	symptom text,
	handphone text,
	address text,
	waktu time,
	tanggal date
);

insert into schedule (doctor_name, patient_name, gender, symptom, handphone, address, waktu, tanggal) 
values
	('dr. Nurita', 'Ahmad Maulana', 'male', '["headache", "stomache"]', 62838, 'address1', '08:00', '2023-10-01'),
	('dr. Yogi', 'Renata Zahab', 'female', '["cough", "flu"]', 62838, 'address2', '09:00', '2022-10-02'),
	('dr. Wibowo', 'Nunuk Reni', 'female', '["cough", "flu"]', 62838, 'address3', '10:00', '2022-10-03'),
	('dr. Yogi', 'Bro Ulil', 'male', '["cough", "headache"]', 62838, 'address4', '11:00', '2022-10-04'),
	('dr. Ulama', 'Wah Bowi', 'male', '["headache", "flu"]', 62838, 'address5', '12:00', '2022-10-05'),
	('dr. Ulama', 'Iis Mika', 'female', '["cough", "flu", "stomache", "headache"]', 62838, 'address6', '08:00', '2022-10-06'),
	('dr. Ping', 'Zizah Lana', 'female', '["flu", "stomache", "headache"]', 62838, 'address7', '09:00', '2022-10-07'),
	('dr. Nurita', 'Alif Iman', 'male', '["cough", "flu", "headache"]', 62838, 'address8', '10:00', '2022-10-08'),
	('dr. Ping', 'Zaka Zaki', 'female', '["cough", "stomache", "headache"]', 62838, 'address9', '11:00', '2022-10-09'),
	('dr. Wibowo', 'Faus Rahmi', 'male', '["cough"]', 62838, 'address10', '12:00', '2022-10-11')
	;