CREATE DATABASE e7gezly;
USE e7gezly;

CREATE TABLE Users (
    User_id INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(45) NOT NULL,
    Last_Name VARCHAR(45) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL,
    Gender ENUM('Male','Female') NOT NULL
);


CREATE TABLE User_Phone (
    User_id INT,
    Phone_Number INT ,

    PRIMARY KEY (User_id, Phone_Number),

    FOREIGN KEY (User_id)
    REFERENCES Users(User_id)
);


CREATE TABLE Patients (
    User_Patient_id INT PRIMARY KEY,
    Date_Of_Birth DATE NOT NULL,

    FOREIGN KEY (User_Patient_id)
    REFERENCES Users(User_id)
);



CREATE TABLE Specialization (
    Specialization_id INT PRIMARY KEY AUTO_INCREMENT,
    Specialization_Name VARCHAR(45) NOT NULL UNIQUE
);


CREATE TABLE Doctors (
    User_Doctor_id INT PRIMARY KEY,
    Consultant_Fees INT NOT NULL,
    Experience_Years INT NOT NULL,
    Specialization_id INT NOT NULL,

    FOREIGN KEY (User_Doctor_id)
    REFERENCES Users(User_id),

    FOREIGN KEY (Specialization_id)
    REFERENCES Specialization(Specialization_id)
);


CREATE TABLE Admins (
    Admin_id INT PRIMARY KEY AUTO_INCREMENT,
    First_Name VARCHAR(45) NOT NULL,
    Last_Name VARCHAR(45) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Password VARCHAR(255) NOT NULL
);


CREATE TABLE Management (
    User_id INT,
    Admin_id INT,

    PRIMARY KEY (User_id, Admin_id),

    FOREIGN KEY (User_id)
    REFERENCES Users(User_id),

    FOREIGN KEY (Admin_id)
    REFERENCES Admins(Admin_id)
);

CREATE TABLE Insurance_Company (
    Company_id INT PRIMARY KEY AUTO_INCREMENT,
    Company_Name VARCHAR(45) NOT NULL,
    Coverage_Percentage INT CHECK (Coverage_Percentage BETWEEN 0 AND 100)
);


CREATE TABLE Insurance (
    Insurance_id INT PRIMARY KEY AUTO_INCREMENT,
    Company_id INT NOT NULL,
    User_Patient_id INT NOT NULL,

    FOREIGN KEY (Company_id)
    REFERENCES Insurance_Company(Company_id),

    FOREIGN KEY (User_Patient_id)
    REFERENCES Patients(User_Patient_id)
);


CREATE TABLE Location (
    Location_id INT PRIMARY KEY AUTO_INCREMENT,
    Street VARCHAR(45) NOT NULL,
    City VARCHAR(45) NOT NULL
);


CREATE TABLE Clinics (
    Clinic_id INT PRIMARY KEY AUTO_INCREMENT,
    Clinic_Name VARCHAR(45) NOT NULL,
    Location_id INT NOT NULL,
    Building_Number INT NOT NULL,
    Floor_Level INT NOT NULL,

    FOREIGN KEY (Location_id)
    REFERENCES Location(Location_id)
);


CREATE TABLE Works_At (
    Doctor_id INT,
    Clinic_id INT,

    PRIMARY KEY (Doctor_id, Clinic_id),

    FOREIGN KEY (Doctor_id)
    REFERENCES Doctors(User_Doctor_id),

    FOREIGN KEY (Clinic_id)
    REFERENCES Clinics(Clinic_id)
);


CREATE TABLE Schedules (
    Schedule_id INT PRIMARY KEY AUTO_INCREMENT,
    Day_Name VARCHAR(20) NOT NULL,
    Start_Time TIME NOT NULL,
    End_Time TIME NOT NULL,
    User_Doctor_id INT NOT NULL,

    FOREIGN KEY (User_Doctor_id)
    REFERENCES Doctors(User_Doctor_id)
);

CREATE TABLE Take_Place_In (
    Clinic_id INT,
    Schedule_id INT,

    PRIMARY KEY (Clinic_id, Schedule_id),

    FOREIGN KEY (Clinic_id)
    REFERENCES Clinics(Clinic_id),

    FOREIGN KEY (Schedule_id)
    REFERENCES Schedules(Schedule_id)
);


CREATE TABLE Appointments (
    Appointment_id INT PRIMARY KEY AUTO_INCREMENT,
    Appointment_Date DATETIME NOT NULL,
    User_Doctor_id INT NOT NULL,
    Schedule_id INT NOT NULL,
    User_Patient_id INT NOT NULL,

    FOREIGN KEY (User_Doctor_id)
    REFERENCES Doctors(User_Doctor_id),

    FOREIGN KEY (Schedule_id)
    REFERENCES Schedules(Schedule_id),

    FOREIGN KEY (User_Patient_id)
    REFERENCES Patients(User_Patient_id)
);

CREATE TABLE Medical_Reports (
    Report_id INT PRIMARY KEY AUTO_INCREMENT,
    Report_Date DATETIME NOT NULL,
    Diagnosis VARCHAR(100) NOT NULL,
    User_Patient_id INT NOT NULL,
    User_Doctor_id INT NOT NULL,

    FOREIGN KEY (User_Patient_id)
    REFERENCES Patients(User_Patient_id),

    FOREIGN KEY (User_Doctor_id)
    REFERENCES Doctors(User_Doctor_id)
);


CREATE TABLE Medicines (
    Report_id INT,
    Medicine_Name VARCHAR(45),

    PRIMARY KEY (Report_id, Medicine_Name),

    FOREIGN KEY (Report_id)
    REFERENCES Medical_Reports(Report_id)
);


CREATE TABLE Test_Results (
    Report_id INT,
    Test_Result VARCHAR(45),

    PRIMARY KEY (Report_id, Test_Result),

    FOREIGN KEY (Report_id)
    REFERENCES Medical_Reports(Report_id)
);


CREATE TABLE Reviews (
    Review_id INT PRIMARY KEY AUTO_INCREMENT,
    Rating TINYINT CHECK (Rating BETWEEN 1 AND 5),
    Appointment_id INT NOT NULL,
    Admin_id INT NOT NULL,

    FOREIGN KEY (Appointment_id)
    REFERENCES Appointments(Appointment_id),

    FOREIGN KEY (Admin_id)
    REFERENCES Admins(Admin_id)
);

INSERT INTO Users (First_Name, Last_Name, Email, Password, Gender) VALUES
('Ahmed','Hassan','ahmed.hassan@gmail.com','ah123','Male'),
('Sara','Ali','sara.ali@gmail.com','sa123','Female'),
('Mohamed','Adel','mohamed.adel@gmail.com','mo123','Male'),
('Nour','Khaled','nour.khaled@gmail.com','no123','Female'),
('Omar','Samy','omar.samy@gmail.com','om123','Male'),
('Mariam','Yasser','mariam.yasser@gmail.com','ma123','Female'),
('Youssef','Nabil','youssef.nabil@gmail.com','yo123','Male'),
('Salma','Tarek','salma.tarek@gmail.com','st123','Female'),
('Karim','Fathy','karim.fathy@gmail.com','ka123','Male'),
('Laila','Mostafa','laila.mostafa@gmail.com','la123','Female'),
('Hany','Ibrahim','hany.ibrahim@gmail.com','ha123','Male'),
('Dina','Maher','dina.maher@gmail.com','di123','Female'),
('Amr','Gamal','dr.amr.gamal@e7gezly.com','am123','Male'),
('Reem','Ashraf','dr.reem.ashraf@e7gezly.com','re123','Female'),
('Tamer','Lotfy','dr.tamer.lotfy@e7gezly.com','ta123','Male'),
('Farah','Wael','dr.farah.wael@e7gezly.com','fa123','Female'),
('Khaled','Ragab','dr.khaled.ragab@e7gezly.com','kh123','Male'),
('Menna','Sherif','dr.menna.sherif@e7gezly.com','me123','Female'),
('Ali','Fouad','dr.ali.fouad@e7gezly.com','al123','Male'),
('Habiba','Ehab','dr.habiba.ehab@e7gezly.com','hb123','Female');


INSERT INTO User_Phone VALUES
(1,'01011111111'),
(2,'01022222222'),
(3,'01033333333'),
(4,'01044444444'),
(5,'01055555555'),
(6,'01066666666'),
(7,'01077777777'),
(8,'01088888888'),
(9,'01099999999'),
(10,'01100000000'),
(11,'01111111111'),
(12,'01122222222'),
(13,'01133333333'),
(14,'01144444444'),
(15,'01155555555'),
(16,'01166666666'),
(17,'01177777777'),
(18,'01188888888'),
(19,'01199999999'),
(20,'01200000000');


INSERT INTO Patients VALUES
(1,'1999-05-10'),
(2,'2001-03-15'),
(3,'1998-07-21'),
(4,'2000-11-30'),
(5,'1997-01-25'),
(6,'2002-08-18'),
(7,'1995-12-05'),
(8,'2003-06-09'),
(9,'1996-04-14'),
(10,'2001-09-27'),
(11,'1994-02-11'),
(12,'2000-10-19');


INSERT INTO Specialization (Specialization_Name) VALUES
('Cardiology'),
('Dermatology'),
('Neurology'),
('Pediatrics'),
('Orthopedics');


INSERT INTO Doctors VALUES
(13,500,10,1),
(14,400,7,2),
(15,650,12,3),
(16,300,5,4),
(17,550,9,5),
(18,450,6,1),
(19,350,4,2),
(20,700,15,3);


INSERT INTO Admins (First_Name, Last_Name, Email, Password) VALUES
('Admin','One','admin1@e7gzly.com','admin123'),
('Admin','Two','admin2@e7gzly.com','admin456'),
('Admin','Three','admin3@e7gzly.com','admin789');


INSERT INTO Management VALUES
(1,1),
(2,1),
(13,2),
(14,2),
(15,3);

INSERT INTO Insurance_Company (Company_Name, Coverage_Percentage) VALUES
('AXA',80),
('MetLife',70),
('Allianz',85),
('MedNet',75),
('NextCare',90);

INSERT INTO Insurance (Company_id, User_Patient_id) VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(1,6),
(2,7),
(3,8),
(4,9),
(5,10);


INSERT INTO Location (Street, City) VALUES
('Tahrir Street','Cairo'),
('Nasr Road','Cairo'),
('Corniche','Alexandria'),
('University Street','Mansoura'),
('Sea Road','Hurghada');

INSERT INTO Clinics
(Clinic_Name, Location_id, Building_Number, Floor_Level)
VALUES
('Heart Care Clinic',1,10,2),
('Skin Health Center',2,15,3),
('Brain Clinic',3,20,1),
('Kids Clinic',4,8,2),
('Bone Care Clinic',5,12,4);

INSERT INTO Works_At VALUES
(13,1),
(14,2),
(15,3),
(16,4),
(17,5),
(18,1),
(19,2),
(20,3);


INSERT INTO Schedules
(Day_Name, Start_Time, End_Time, User_Doctor_id)
VALUES
('Sunday','09:00:00','01:00:00',13),
('Monday','10:00:00','02:00:00',14),
('Tuesday','11:00:00','03:00:00',15),
('Wednesday','08:00:00','12:00:00',16),
('Thursday','01:00:00','05:00:00',17),
('Friday','09:00:00','01:00:00',18),
('Saturday','10:00:00','02:00:00',19),
('Sunday','12:00:00','04:00:00',20);


INSERT INTO Take_Place_In VALUES
(1,1),
(2,2),
(3,3),
(4,4),
(5,5),
(1,6),
(2,7),
(3,8);



INSERT INTO Appointments
(Appointment_Date, User_Doctor_id, Schedule_id, User_Patient_id)
VALUES
('2026-05-20 10:00:00',13,1,1),
('2026-05-20 11:00:00',14,2,2),
('2026-05-21 12:00:00',16,4,3),
('2026-05-22 01:00:00',17,5,4),
('2026-05-23 02:00:00',19,7,5),
('2026-05-24 03:00:00',20,8,6);


INSERT INTO Medical_Reports
(Report_Date, Diagnosis, User_Patient_id, User_Doctor_id)
VALUES
('2026-05-20 10:30:00','High Blood Pressure',1,13),
('2026-05-20 11:30:00','Skin Allergy',2,14),
('2026-05-21 12:30:00','Flu',3,16),
('2026-05-22 01:30:00','Knee Pain',4,17),
('2026-05-23 02:30:00','Migraine',5,20);


INSERT INTO Medicines VALUES
(1,'Panadol'),
(1,'Aspirin'),
(2,'Cetirizine'),
(3,'Paracetamol'),
(4,'Ibuprofen'),
(5,'Migranil');

INSERT INTO Test_Results VALUES
(1,'Blood Pressure Test'),
(2,'Skin Test'),
(3,'CBC'),
(4,'X-Ray'),
(5,'MRI');


INSERT INTO Reviews
(Rating, Appointment_id, Admin_id)
VALUES
(5,1,1),
(4,2,2),
(3,3,1),
(5,4,3),
(4,5,2),
(5,6,3);


SELECT
    User_Doctor_id,
    AVG(Rating) AS Rating_Average
FROM Reviews
JOIN Appointments
ON Reviews.Appointment_id = Appointments.Appointment_id
GROUP BY User_Doctor_id;