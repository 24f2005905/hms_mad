-- Slots with sorted days MON-SAT

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS Slots (
    Doctor_ID varchar(15) PRIMARY KEY ,
    Days_Available TEXT NOT NULL,
    Start_Date DATE NOT NULL,
    End_Date DATE NOT NULL,
    FOREIGN KEY (Doctor_ID) REFERENCES Users(User_ID)
);
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-03-006', '["MON", "TUE", "WED", "THU", "FRI"]', '2025-12-08', '2025-12-19');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-03-007', '["TUE", "WED", "THU", "FRI", "SAT"]', '2026-01-03', '2026-01-13');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-03-008', '["MON", "TUE", "WED", "THU", "FRI", "SAT"]', '2025-11-21', '2026-01-07');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-03-009', '["TUE", "THU"]', '2025-12-11', '2025-12-31');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-03-010', '["TUE", "SAT"]', '2025-11-16', '2025-12-18');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-04-001', '["MON", "TUE", "THU", "FRI"]', '2025-12-10', '2026-01-07');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-04-002', '["TUE", "FRI"]', '2025-11-26', '2025-12-31');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-05-001', '["TUE", "WED", "THU", "FRI"]', '2025-12-05', '2026-01-11');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-05-002', '["TUE", "WED", "THU", "FRI", "SAT"]', '2025-12-05', '2025-12-17');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-05-003', '["TUE", "WED", "THU", "SAT"]', '2025-12-22', '2026-01-06');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-05-004', '["MON", "FRI"]', '2025-11-23', '2025-12-16');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-06-001', '["MON", "TUE", "WED", "FRI", "SAT"]', '2026-01-02', '2026-01-12');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-07-001', '["WED", "THU"]', '2025-12-24', '2026-01-13');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-07-002', '["TUE", "WED", "THU", "FRI", "SAT"]', '2025-12-08', '2026-01-14');
INSERT OR REPLACE INTO Slots (Doctor_ID, Days_Available, Start_Date, End_Date) VALUES ('D-2023-01-07-003', '["TUE", "WED", "THU", "FRI", "SAT"]', '2025-12-12', '2025-12-28');
COMMIT;