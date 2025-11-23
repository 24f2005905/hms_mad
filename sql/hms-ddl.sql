-- Hospital Management System DDLs --

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    User_ID Varchar(15) UNIQUE NOT NULL,
    First_Name Varchar(50) NOT NULL,
    Last_Name Varchar(50)  NULL,
    User_Type Varchar(10) NOT NULL ,
    Phone_Number Varchar(15) NOT NULL,
    User_Profile TEXT NULL,
    Password Varchar(255) NOT NULL,
    User_Status Varchar(10) DEFAULT 'ACTIVE' NOT NULL,
    CHECK(User_Type IN ('ADMIN', 'DOCTOR', 'PATIENT'))
    CHECK(User_Status IN ('ACTIVE', 'INACTIVE'))
);

CREATE TABLE Appointments (
    Appointment_ID varchar(64) PRIMARY KEY ,
    Patient_ID varchar(15) NOT NULL,
    Doctor_ID varchar(15) NOT NULL,
    Appointment_Date DATE NOT NULL,
    Appointment_Time TIME NOT NULL,
    Appointment_Status Varchar(20) NOT NULL DEFAULT 'SCHEDULED',
    FOREIGN KEY (Patient_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID),
    CHECK (Patient_ID <> Doctor_ID),
    CHECK (Appointment_Status IN ('SCHEDULED', 'COMPLETED', 'CANCELLED'))
);  

CREATE TABLE Treatments (
    Appointment_ID varchar(15) PRIMARY KEY,
    Diagnosis TEXT NOT NULL,
    Prescription TEXT NULL,
    Notes TEXT NULL,
    FOREIGN KEY (Appointment_ID) REFERENCES Appointments(Appointment_ID)
);

CREATE TABLE Departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Dept_ID VARCHAR(15) UNIQUE NOT NULL,
    Speciality Varchar(50) UNIQUE NOT NULL,
    Details TEXT NULL
);

CREATE TABLE Doctor_Dept (
    Doctor_ID varchar(15) NOT NULL,
    Dept_ID varchar(15) NOT NULL,
    Dept_Position Varchar(50) NOT NULL,
    PRIMARY KEY (Doctor_ID, Dept_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Departments(Dept_ID)
    CHECK (Dept_Position IN ('HOD','CONSULTANT','RESIDENT'))
);

CREATE TABLE Slots (
    Doctor_ID varchar(15) PRIMARY KEY ,
    Days_Available TEXT NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID)
);

CREATE VIEW Doctor_Lookup AS 
SELECT u.User_ID,
       u.First_Name,
       u.Last_Name,
       GROUP_CONCAT(d.Speciality) AS Specialities
FROM Users u 
JOIN Doctor_Dept dd ON u.User_ID = dd.Doctor_ID
JOIN Departments d ON dd.Dept_ID = d.Dept_ID
WHERE u.User_Type = 'DOCTOR' AND u.User_Status = 'ACTIVE'
GROUP BY u.User_ID, u.First_Name, u.Last_Name;

/* 
ALTER TABLE Appointments
ADD CONSTRAINT unique_appointment UNIQUE (Doctor_ID, Appointment_Date, Appointment_Time);*/

INSERT INTO Users VALUES
    (1,"ADMIN","Admin","Superuser","ADMIN","9999999999",NULL,"admin","ACTIVE")
