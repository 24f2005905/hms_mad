--  User_ID ,First_name ,Last_name ,User_Type,Phone_Number ,User_Profile  --
/* 
INSERT INTO Users VALUES
    ('A202511151','Sudharshan','Srinivasan','ADMIN','9999999999',NULL),
    ('P202511151','Varshitha','Muralidharan','PATIENT','8888888888',NULL),
    ('P202511152','Anitha','Kumar','PATIENT','7777777777',NULL),
    ('P202511153','Ramesh','Gupta','PATIENT','4444444444',NULL),
    ('D202511151','Dr. Karthik','Rajan','DOCTOR','6666666666',NULL),
    ('D202511152','Dr. Meena','Sharma','DOCTOR','5555555555',NULL),
    ('D202511153','Dr. Anil','Verma','DOCTOR','3333333333',NULL);
     

-- Dept_ID ,Dept_Name ,Details  --

INSERT INTO Departments VALUES
    ('CARDIO','Cardiology','Handles heart-related issues'),
    ('GASTRO','Gastroenterology','Deals with digestive system disorders'),
    ('GYNECO','Gynecology','Focuses on women health'),
    ('NEURO','Neurology','Treats nervous system disorders'),
    ('PEDIA','Pediatrics','Cares for infants, children, and adolescents'),
    ('DERMA','Dermatology','Manages skin-related conditions');

-- Doctor_ID ,Dept_ID  -- 

INSERT INTO Doctor_Dept VALUES
    ('D202511151','CARDIO'),
    ('D202511151','GASTRO'),
    ('D202511152','GASTRO'),
    ('D202511153','DERMA');
    

-- Doctor_ID, Days_Available, Time_Slots --

TRUNCATE TABLE SLOTS;
INSERT INTO SLOTS VALUES
('D202511151','["MON","TUE","THU","SAT"]','["09:00","09:15","09:30","09:45","10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00"),
('D202511152','["TUE","WED","SAT","SUN"]','["10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00"),
('D202511153','["TUE","WED","THU","FRI","SUN"]','["11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00");


-- Appointment_ID, Patient_ID, Doctor_ID, Appointment_Date, Appointment_Time, Appointment_Status --
INSERT INTO Appointments VALUES
('APPT202511151','P202511151','D202511151','2024-12-01','09:30','SCHEDULED'),
('APPT202511152','P202511152','D202511152','2024-12-02','10:15','CANCELLED'),
('APPT202511153','P202511153','D202511153','2024-12-03','11:00','COMPLETED');


-- Appointment_ID, Diagnosis, Prescription, Notes --
INSERT INTO Treatments VALUES
('APPT202511153','Acne and Dry Skin','Medicine : (Acne Gel, MoizXL)','Patient advised to rest and stay hydrated.'),
('APPT202511151','Hypertension','Medicine : (Telma, Atenolol)','Regular monitoring of blood pressure recommended.');
;
*/

-- EXCEPTIONS -- 

/*
INSERT INTO Users VALUES
('A202511156','Sudhu','Budhu','USER','9999999199',NULL); --- Invalid User_Type --


INSERT INTO Users VALUES
('A202511151','Sudharshan','Srinivasan','ADMIN','9999999999',NULL); --- Duplicate User_ID --


INSERT INTO Appointments VALUES
('APPT202511151','P202511151','D202511151','2024-12-01','09:30','RESCHEDULED'); --- Invalid Appointment_Status --


INSERT INTO Appointments VALUES
('APPT202511157','P202511151','P202511151','2024-12-01','09:30','SCHEDULED'); --- Patient_ID and Doctor_ID are same --


INSERT INTO Doctor_Dept VALUES
('D202511153','ORTHO'); --- Dept_ID does not exist --


INSERT INTO Doctor_Dept VALUES
('D202511157','CARDIO'); --- Doctor_ID does not exist --

INSERT INTO Appointments VALUES
('APPT202511154','P202511152','D202511151','2024-12-02','19:15','SCHEDULED'); --- Time_Slot not available for the doctor --

INSERT INTO Appointments VALUES
('APPT202511154','P202511152','D202511151','2024-12-01','09:30','SCHEDULED'); --- Duplicate Appointment for the same Doctor at same Date and Time --
*/

-- Doctor_ID, Days_Available, Time_Slots --

TRUNCATE TABLE SLOTS;
INSERT INTO SLOTS VALUES
('D202511151','["MON","TUE","THU","SAT"]','["09:00","09:15","09:30","09:45","10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00"]'),
('D202511152','["TUE","WED","SAT","SUN"]','["10:00","10:15","10:30","10:45","11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00"]'),
('D202511153','["TUE","WED","THU","FRI","SUN"]','["11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00"]');














