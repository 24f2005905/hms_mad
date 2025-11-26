-- Doctor_Dept inserts linking doctors to their departments

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS Doctor_Dept (
    Doctor_ID varchar(15) NOT NULL,
    Dept_ID varchar(15) NOT NULL,
    Dept_Position Varchar(50) NOT NULL,
    PRIMARY KEY (Doctor_ID, Dept_ID),
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Dept_ID) REFERENCES Departments(Dept_ID)
    CHECK (Dept_Position IN ('HOD','CONSULTANT','RESIDENT'))
);
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-03-006', 'Dept-001', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-03-007', 'Dept-001', 'CONSULTANT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-03-008', 'Dept-001', 'CONSULTANT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-04-001', 'Dept-002', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-03-009', 'Dept-002', 'CONSULTANT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-03-010', 'Dept-002', 'CONSULTANT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-04-002', 'Dept-003', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-05-001', 'Dept-003', 'RESIDENT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-05-002', 'Dept-003', 'RESIDENT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-05-004', 'Dept-004', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-05-003', 'Dept-004', 'RESIDENT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-06-001', 'Dept-005', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-07-001', 'Dept-005', 'CONSULTANT');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-07-002', 'Dept-006', 'HOD');
INSERT INTO Doctor_Dept (Doctor_ID, Dept_ID, Dept_Position) VALUES ('D-2023-01-07-003', 'Dept-006', 'RESIDENT');
COMMIT;