-- Departments table and inserts generated from doctor specialities

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS Departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Dept_ID VARCHAR(15) UNIQUE NOT NULL,
    Speciality Varchar(50) UNIQUE NOT NULL,
    Details TEXT NULL
);
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-001', 'Cardiology', 'Department focusing on diagnosis and treatment of heart conditions.');
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-002', 'Neurology', 'Department dealing with disorders of the nervous system and brain.');
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-003', 'Orthopedics', 'Department specializing in musculoskeletal system and bone surgery.');
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-004', 'Pediatrics', 'Department providing medical care for infants, children, and adolescents.');
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-005', 'Dermatology', 'Department treating skin-related conditions and cosmetic concerns.');
INSERT INTO Departments (Dept_ID, Speciality, Details) VALUES ('Dept-006', 'Gynecology', 'Department specializing in female reproductive health and obstetrics.');
COMMIT;