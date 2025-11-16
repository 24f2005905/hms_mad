-- Hospital Management System DDLs --

CREATE TABLE Users (
    User_ID Varchar(15) PRIMARY KEY,
    First_name Varchar(50) NOT NULL,
    Last_name Varchar(50)  NULL,
    User_Type Varchar(10) NOT NULL ,
    Phone_Number Varchar(15) NOT NULL,
    User_Profile TEXT NULL,
    CHECK(User_Type IN ('ADMIN', 'DOCTOR', 'PATIENT'))
);

CREATE TABLE Appointments (
    Appointment_ID varchar(15) PRIMARY KEY ,
    Patient_ID varchar(15) NOT NULL,
    Doctor_ID varchar(15) NOT NULL,
    Appointment_Date DATE NOT NULL,
    Appointment_Time TIME NOT NULL,
    Appointment_Status Varchar(20) NOT NULL,
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
    Dept_ID VARCHAR(15) PRIMARY KEY ,
    Dept_Name Varchar(50) NOT NULL,
    Details TEXT NULL

);

CREATE TABLE Doctor_Dept (
    Doctor_ID varchar(15) NOT NULL,
    Dept_ID varchar(15) NOT NULL,
    PRIMARY KEY (Doctor_ID, Dept_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Departments(Dept_ID)
);

CREATE TABLE Slots (
    Doctor_ID varchar(15) PRIMARY KEY ,
    Days_Available TEXT NOT NULL,
    Time_Slots TEXT NOT NULL,
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID),
    CHECK (
        Time_Slots ~ '[0-2][0-9]:[0-5][0-9]'
    AND substr(Time_Slots, 4, 2) IN ('00', '15', '30', '45')
    )
);
