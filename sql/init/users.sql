INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('A-2023-01-01-001','rohit.shah1@example.com','F','Rohit','Shah','ADMIN','7117399328','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-07-15','Bangalore, Karnataka'),
('A-2023-01-02-001','ira.das1@example.com','F','Ira','Das','ADMIN','8880460588','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-11-09','Mumbai, Maharashtra'),
('A-2023-01-02-002','tanvi.singh1@example.com','M','Tanvi','Singh','ADMIN','8504756479','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1989-03-22','Hyderabad, Telangana'),
('A-2023-01-02-003','aditi.reddy1@example.com','F','Aditi','Reddy','ADMIN','6047035201','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1985-01-13','Chennai, Tamil Nadu'),
('A-2023-01-02-004','vivaan.singh1@example.com','M','Vivaan','Singh','ADMIN','6724534561','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1990-06-29','Pune, Maharashtra'),
('A-2023-01-03-001','divya.reddy1@example.com','F','Divya','Reddy','ADMIN','9632124356','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-09-17','Noida, Uttar Pradesh'),
('A-2023-01-03-002','aadhya.sharma1@example.com','M','Aadhya','Sharma','ADMIN','9805650317','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1983-05-04','Gurgaon, Haryana'),
('A-2023-01-03-003','kabir.trivedi1@example.com','M','Kabir','Trivedi','ADMIN','7985240118','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-12-07','Kolkata, West Bengal'),
('A-2023-01-03-004','diya.malhotra1@example.com','F','Diya','Malhotra','ADMIN','9829859276','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1986-02-19','Ahmedabad, Gujarat'),
('A-2023-01-03-005','ritu.sharma1@example.com','F','Ritu','Sharma','ADMIN','9658905770','{}','$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1988-10-03','Jaipur, Rajasthan');

INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('D-2023-01-03-006','rahul.das1@example.com','F','Rahul','Das','DOCTOR','7269909171',
 '{"Qualification":"MBBS, DNB","Experience":3,"Expertise":"Cardiologist (Clinical)","Bio":"Dr. Rahul Das is a dedicated cardiologist committed to preventive care and patient education. He focuses on early detection and lifestyle improvement strategies to reduce risk of heart disease."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1985-10-14','Mumbai, Maharashtra'),

('D-2023-01-03-007','krishna.joshi1@example.com','M','Krishna','Joshi','DOCTOR','9043817770',
 '{"Qualification":"MBBS, MS","Experience":9,"Expertise":"Cardiologist (Surgical)","Bio":"Dr. Krishna Joshi specializes in complex cardiothoracic procedures with a strong emphasis on minimally invasive surgery and patient recovery techniques."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1979-03-29','Pune, Maharashtra'),

('D-2023-01-03-008','pooja.mehta1@example.com','M','Pooja','Mehta','DOCTOR','7269837238',
 '{"Qualification":"MBBS, MD, DM","Experience":16,"Expertise":"Cardiologist (Clinical)","Bio":"Dr. Pooja Mehta brings over a decade of experience diagnosing high-risk cardiac conditions and offering long-term rehabilitation planning."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1982-08-21','Hyderabad, Telangana'),

('D-2023-01-03-009','tanvi.nambiar1@example.com','M','Tanvi','Nambiar','DOCTOR','8703118114',
 '{"Qualification":"MBBS, MS","Experience":6,"Expertise":"Neurologist (Clinical)","Bio":"Dr. Tanvi Nambiar specializes in neurological disorders and provides personalized treatment plans that incorporate the latest diagnostic methods."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1987-07-09','Chennai, Tamil Nadu'),

('D-2023-01-03-010','tanvi.mehta1@example.com','M','Tanvi','Mehta','DOCTOR','7375768378',
 '{"Qualification":"MBBS, MS","Experience":20,"Expertise":"Neurologist (Surgical)","Bio":"Dr. Tanvi Mehta is known for her expertise in neurological surgery and post-operative care, working closely with patients and families throughout the recovery process."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1978-01-11','Delhi, NCR'),

('D-2023-01-04-001','krishna.khan1@example.com','M','Krishna','Khan','DOCTOR','7367167153',
 '{"Qualification":"MBBS, MD, DM","Experience":20,"Expertise":"Neurologist (Clinical)","Bio":"Dr. Krishna Khan combines research-driven diagnostics with compassionate care and is actively involved in neurological case studies and publications."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1975-12-26','Bangalore, Karnataka'),

('D-2023-01-04-002','ritu.reddy1@example.com','F','Ritu','Reddy','DOCTOR','9239649208',
 '{"Qualification":"MBBS, MS","Experience":5,"Expertise":"Orthopedist (Surgical)","Bio":"Dr. Ritu Reddy offers advanced orthopedic treatments and adopts modern surgical procedures to promote faster and more effective recovery."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1990-05-18','Ahmedabad, Gujarat'),

('D-2023-01-05-001','zoya.saxena1@example.com','F','Zoya','Saxena','DOCTOR','9753406538',
 '{"Qualification":"MBBS, MD, DM","Experience":19,"Expertise":"Orthopedist (Clinical)","Bio":"Dr. Zoya Saxena provides comprehensive care for bone and joint health, with a focus on preventive medicine and rehabilitation."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1981-02-22','Lucknow, Uttar Pradesh'),

('D-2023-01-05-002','aditi.mehta1@example.com','M','Aditi','Mehta','DOCTOR','8480029925',
 '{"Qualification":"MBBS, MD","Experience":9,"Expertise":"Orthopedist (Clinical)","Bio":"Dr. Aditi Mehta is committed to research and advancement in spine and sports injury management, offering modern therapies and consultation."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1984-04-08','Noida, Uttar Pradesh'),

('D-2023-01-05-003','diya.kumar1@example.com','F','Diya','Kumar','DOCTOR','7036696798',
 '{"Qualification":"MBBS, MD","Experience":13,"Expertise":"Pediatrician (Clinical)","Bio":"Dr. Diya Kumar specializes in pediatric care and focuses on early diagnosis and long-term wellness for infants and children."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1986-11-03','Kochi, Kerala'),

('D-2023-01-05-004','sara.khan1@example.com','F','Sara','Khan','DOCTOR','9772601145',
 '{"Qualification":"MBBS","Experience":17,"Expertise":"Pediatrician (Surgical)","Bio":"Dr. Sara Khan provides advanced pediatric diagnostics and post-operative treatment for complex congenital conditions."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1979-09-07','Thane, Maharashtra'),

('D-2023-01-06-001','rakesh.saxena1@example.com','F','Rakesh','Saxena','DOCTOR','6161639072',
 '{"Qualification":"MBBS","Experience":19,"Expertise":"Dermatologist (Clinical)","Bio":"Dr. Rakesh Saxena focuses on skin-related conditions and cosmetic dermatology with a patient-first care approach."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1980-02-28','Surat, Gujarat'),

('D-2023-01-07-001','vikas.sharma1@example.com','F','Vikas','Sharma','DOCTOR','8426245956',
 '{"Qualification":"MBBS","Experience":3,"Expertise":"Dermatologist (Clinical)","Bio":"Dr. Vikas Sharma provides treatment for a wide range of skin and hair disorders and is known for detailed and structured consultation."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1993-10-30','Indore, Madhya Pradesh'),

('D-2023-01-07-002','aditya.kapoor1@example.com','M','Aditya','Kapoor','DOCTOR','6056729594',
 '{"Qualification":"MBBS, MD, DM","Experience":8,"Expertise":"Gynecologist (Surgical)","Bio":"Dr. Aditya Kapoor specializes in women’s health and offers surgical treatments with a focus on comfort and privacy."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1988-03-15','Nagpur, Maharashtra'),

('D-2023-01-07-003','shreya.kumar1@example.com','F','Shreya','Kumar','DOCTOR','6075367398',
 '{"Qualification":"MBBS","Experience":23,"Expertise":"Gynecologist (Clinical)","Bio":"Dr. Shreya Kumar provides compassionate and comprehensive women’s healthcare and has extensive experience in complex case management."}',
 '$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE',
 '1976-06-05','Patna, Bihar');

INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('P-2023-01-07-004','neha.nair1@example.com','F','Neha','Nair','PATIENT','8651228016','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-05-09','Bangalore, Karnataka'),

('P-2023-01-07-005','ishaan.kapoor1@example.com','M','Ishaan','Kapoor','PATIENT','8301549389','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1993-11-12','Mumbai, Maharashtra'),

('P-2023-01-08-001','sara.joshi1@example.com','F','Sara','Joshi','PATIENT','7560919775','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1988-07-18','Hyderabad, Telangana'),

('P-2023-01-08-002','myra.chopra1@example.com','M','Myra','Chopra','PATIENT','8408228343','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-03-02','Chennai, Tamil Nadu'),

('P-2023-01-08-003','aditi.nambiar1@example.com','F','Aditi','Nambiar','PATIENT','9123020026','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1997-09-28','Pune, Maharashtra'),

('P-2023-01-09-001','pooja.trivedi1@example.com','F','Pooja','Trivedi','PATIENT','9228827151','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1990-01-14','Noida, Uttar Pradesh'),

('P-2023-01-09-002','imran.kumar1@example.com','M','Imran','Kumar','PATIENT','9525534385','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1985-12-07','Kolkata, West Bengal'),

('P-2023-01-11-001','sunita.patel1@example.com','F','Sunita','Patel','PATIENT','8478282607','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-04-03','Ahmedabad, Gujarat'),

('P-2023-01-11-002','kabir.dutta1@example.com','F','Kabir','Dutta','PATIENT','8289444089','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-06-22','Jaipur, Rajasthan'),

('P-2023-01-11-003','amit.shah1@example.com','F','Amit','Shah','PATIENT','8611827821','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1993-08-10','Delhi, NCR'),

('P-2023-01-11-004','samir.bhatt1@example.com','M','Samir','Bhatt','PATIENT','9620716442','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1989-07-19','Bangalore, Karnataka'),

('P-2023-01-11-005','aakash.khan1@example.com','M','Aakash','Khan','PATIENT','8162431568','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-09-25','Hyderabad, Telangana'),

('P-2023-01-11-006','imran.trivedi1@example.com','F','Imran','Trivedi','PATIENT','8564049676','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1995-03-06','Mumbai, Maharashtra'),

('P-2023-01-11-007','suresh.singh1@example.com','F','Suresh','Singh','PATIENT','6390528331','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1983-11-14','Pune, Maharashtra'),

('P-2023-01-11-008','karan.roy1@example.com','M','Karan','Roy','PATIENT','8220120041','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-08-20','Gurgaon, Haryana'),

('P-2023-01-11-009','nikhil.reddy1@example.com','M','Nikhil','Reddy','PATIENT','6993510061','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-01-11','Indore, Madhya Pradesh'),

('P-2023-01-11-010','kiara.iyer1@example.com','M','Kiara','Iyer','PATIENT','9627572863','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-10-01','Surat, Gujarat'),

('P-2023-01-11-011','rakesh.ganguly1@example.com','M','Rakesh','Ganguly','PATIENT','6536075175','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1988-05-15','Noida, Uttar Pradesh'),

('P-2023-01-11-012','rohan.joshi1@example.com','F','Rohan','Joshi','PATIENT','9830165872','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1997-06-29','Kolkata, West Bengal');

INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('P-2023-01-11-013','myra.saxena1@example.com','F','Myra','Saxena','PATIENT','6021263136','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-09-23','Chennai, Tamil Nadu'),

('P-2023-01-12-001','samir.sharma1@example.com','M','Samir','Sharma','PATIENT','6685966460','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-02-09','Hyderabad, Telangana'),

('P-2023-01-13-001','ananya.agarwal1@example.com','M','Ananya','Agarwal','PATIENT','7704078187','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1995-05-14','Pune, Maharashtra'),

('P-2023-01-13-002','pooja.roy1@example.com','M','Pooja','Roy','PATIENT','9122797056','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1989-01-25','Noida, Uttar Pradesh'),

('P-2023-01-13-003','rahul.bhatt1@example.com','F','Rahul','Bhatt','PATIENT','6887456123','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-06-30','Delhi, NCR'),

('P-2023-01-13-004','suresh.nair1@example.com','M','Suresh','Nair','PATIENT','7485758485','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-10-18','Kolkata, West Bengal'),

('P-2023-01-13-005','farhan.gupta1@example.com','F','Farhan','Gupta','PATIENT','9176779363','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1997-03-08','Bangalore, Karnataka'),

('P-2023-01-13-006','naveen.mishra1@example.com','M','Naveen','Mishra','PATIENT','7756681057','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1986-12-14','Surat, Gujarat'),

('P-2023-01-13-007','liya.sharma1@example.com','M','Liya','Sharma','PATIENT','9259030468','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-05-21','Ahmedabad, Gujarat'),

('P-2023-01-13-008','rina.gupta1@example.com','M','Rina','Gupta','PATIENT','7556337033','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-09-07','Gurgaon, Haryana'),

('P-2023-01-15-001','karan.bhatt1@example.com','M','Karan','Bhatt','PATIENT','6207227859','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-08-03','Hyderabad, Telangana'),

('P-2023-01-15-002','ira.das2@example.com','M','Ira','Das','PATIENT','9221159695','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1985-01-05','Mumbai, Maharashtra'),

('P-2023-01-15-003','reema.agarwal1@example.com','F','Reema','Agarwal','PATIENT','8616373122','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-07-11','Pune, Maharashtra'),

('P-2023-01-17-001','shreya.kapoor1@example.com','M','Shreya','Kapoor','PATIENT','9425389704','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1988-04-09','Chennai, Tamil Nadu'),

('P-2023-01-17-002','sara.nair1@example.com','F','Sara','Nair','PATIENT','9588059301','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-05-28','Noida, Uttar Pradesh'),

('P-2023-01-18-001','amrita.joshi1@example.com','M','Amrita','Joshi','PATIENT','8547700819','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-02-17','Ahmedabad, Gujarat'),

('P-2023-01-19-001','tanvi.patel1@example.com','F','Tanvi','Patel','PATIENT','8965809183','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1990-03-30','Delhi, NCR'),

('P-2023-01-21-001','divya.shah1@example.com','F','Divya','Shah','PATIENT','8269375265','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-06-15','Gurgaon, Haryana');

INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('P-2023-01-21-002','reema.kumar1@example.com','F','Reema','Kumar','PATIENT','8767436136','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-10-04','Bangalore, Karnataka'),

('P-2023-01-22-001','ananya.malhotra1@example.com','M','Ananya','Malhotra','PATIENT','7470564714','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-08-29','Chennai, Tamil Nadu'),

('P-2023-01-22-002','neha.ganguly1@example.com','M','Neha','Ganguly','PATIENT','9052224681','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1993-09-12','Hyderabad, Telangana'),

('P-2023-01-23-001','ritu.roy1@example.com','M','Ritu','Roy','PATIENT','7619961182','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-06-01','Mumbai, Maharashtra'),

('P-2023-01-23-002','aditya.dutta1@example.com','M','Aditya','Dutta','PATIENT','7033893916','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1995-02-19','Pune, Maharashtra'),

('P-2023-01-24-001','kabir.prasad1@example.com','F','Kabir','Prasad','PATIENT','6410557140','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-11-02','Gurgaon, Haryana'),

('P-2023-01-24-002','aadhya.chopra1@example.com','F','Aadhya','Chopra','PATIENT','9450768708','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-12-23','Noida, Uttar Pradesh'),

('P-2023-01-24-003','rohan.patel1@example.com','M','Rohan','Patel','PATIENT','6415619561','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-01-14','Ahmedabad, Gujarat'),

('P-2023-01-25-001','neha.malhotra1@example.com','M','Neha','Malhotra','PATIENT','7036815845','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-09-09','Hyderabad, Telangana'),

('P-2023-01-25-002','naveen.dutta1@example.com','F','Naveen','Dutta','PATIENT','9720642911','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1997-04-27','Bangalore, Karnataka'),

('P-2023-01-25-003','imran.mehta1@example.com','F','Imran','Mehta','PATIENT','6068641011','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1986-02-07','Mumbai, Maharashtra'),

('P-2023-01-25-004','vikas.saxena1@example.com','M','Vikas','Saxena','PATIENT','8203325513','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1994-07-23','Hyderabad, Telangana'),

('P-2023-01-25-005','vivaan.mishra1@example.com','F','Vivaan','Mishra','PATIENT','7173487361','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1988-06-05','Surat, Gujarat'),

('P-2023-01-25-006','aadhya.nambiar1@example.com','F','Aadhya','Nambiar','PATIENT','6947365849','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1984-03-16','Noida, Uttar Pradesh'),

('P-2023-01-25-007','sunita.bose1@example.com','M','Sunita','Bose','PATIENT','9514484286','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1993-11-30','Pune, Maharashtra'),

('P-2023-01-25-008','kavita.agarwal1@example.com','F','Kavita','Agarwal','PATIENT','9644608885','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1996-01-04','Chennai, Tamil Nadu'),

('P-2023-01-26-001','anil.reddy1@example.com','M','Anil','Reddy','PATIENT','7923251533','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2n9qDUysDGT3zCy','ACTIVE','1985-09-22','Kolkata, West Bengal');

INSERT INTO Users (
  User_ID, Email_ID, Sex, First_Name, Last_Name,
  User_Type, Phone_Number, User_Profile,
  Password, User_Status,
  Date_of_Birth, Address
) VALUES
('P-2023-01-27-001','rakesh.trivedi1@example.com','M','Rakesh','Trivedi','PATIENT','7079518077','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1988-02-18','Delhi, NCR'),

('P-2023-01-27-002','sai.gupta1@example.com','F','Sai','Gupta','PATIENT','8843428721','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-10-09','Pune, Maharashtra'),

('P-2023-01-27-003','priya.patel1@example.com','M','Priya','Patel','PATIENT','8920182595','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1985-04-03','Bangalore, Karnataka'),

('P-2023-01-27-004','sai.nambiar1@example.com','M','Sai','Nambiar','PATIENT','9462747647','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-12-22','Ahmedabad, Gujarat'),

('P-2023-01-27-005','saanvi.kumar1@example.com','M','Saanvi','Kumar','PATIENT','6865660049','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1990-07-27','Mumbai, Maharashtra'),

('P-2023-01-27-006','sara.chopra1@example.com','M','Sara','Chopra','PATIENT','8666200586','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1986-05-02','Hyderabad, Telangana'),

('P-2023-01-27-007','suresh.bhatt1@example.com','F','Suresh','Bhatt','PATIENT','8384968416','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-01-13','Chennai, Tamil Nadu'),

('P-2023-01-27-008','samir.dutta1@example.com','M','Samir','Dutta','PATIENT','7918261425','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1989-09-14','Kolkata, West Bengal'),

('P-2023-01-27-009','kabir.verma1@example.com','M','Kabir','Verma','PATIENT','7436904592','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1997-01-08','Mumbai, Maharashtra'),

('P-2023-01-29-001','zoya.jain1@example.com','F','Zoya','Jain','PATIENT','6258853880','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-03-21','Delhi, NCR'),

('P-2023-01-29-002','pooja.verma1@example.com','M','Pooja','Verma','PATIENT','9246444176','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1992-10-03','Bangalore, Karnataka'),

('P-2023-01-30-001','diya.mehta1@example.com','M','Diya','Mehta','PATIENT','7082576800','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-02-27','Pune, Maharashtra'),

('P-2023-01-30-002','aadhya.patel1@example.com','F','Aadhya','Patel','PATIENT','6802701991','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1993-04-18','Hyderabad, Telangana'),

('P-2023-01-30-003','aadhya.roy1@example.com','M','Aadhya','Roy','PATIENT','6145150301','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1987-07-07','Mumbai, Maharashtra'),

('P-2023-01-30-004','rohit.mishra1@example.com','F','Rohit','Mishra','PATIENT','6209098707','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-08-16','Chennai, Tamil Nadu'),

('P-2023-01-30-005','rahul.dutta1@example.com','F','Rahul','Dutta','PATIENT','8074607188','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1991-01-03','Kolkata, West Bengal'),

('P-2023-01-31-001','aakash.trivedi1@example.com','F','Aakash','Trivedi','PATIENT','8512621755','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1989-09-01','Pune, Maharashtra'),

('P-2023-01-31-002','kavita.joshi1@example.com','F','Kavita','Joshi','PATIENT','7521324502','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1996-06-24','Chennai, Tamil Nadu'),

('P-2023-02-02-001','liya.prasad1@example.com','M','Liya','Prasad','PATIENT','7862751889','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1994-03-30','Delhi, NCR'),

('P-2023-02-02-002','naveen.sharma1@example.com','M','Naveen','Sharma','PATIENT','9640640929','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1993-11-08','Ahmedabad, Gujarat'),

('P-2023-02-03-001','yash.saxena1@example.com','M','Yash','Saxena','PATIENT','6851040334','{}',
'$2b$12$EQkahsINE66qGIra2CQvzeCbws8divyw041hH2nN9qDUysDGT3zCy','ACTIVE','1984-05-01','Hyderabad, Telangana');
